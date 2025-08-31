import random
import time
from enum import Enum

from app.config import ACTION_SEQUENCE, MAX_ROOM_CAPACITY, MONGO_URI
from app.models.enums import ActionType, RoomPhase
from app.utils.get_algoleague_problem_tags import \
    get_algoleague_problem_tags_and_ids
from app.utils.get_problem_by_tag import get_problems_by_tag_id
from app.utils.get_team_info import get_team_info
from pymongo import MongoClient

client = MongoClient(MONGO_URI)
db = client.theleague
rooms_collection = db.rooms


class Room:
    def __init__(self, room_id, team1_id=None, team2_id=None):
        self.room_id = room_id
        self.phase = RoomPhase.WAITING
        if (team1_id is None) != (team2_id is None):
            raise ValueError("Both team IDs must be provided or both must be None")
        if team1_id is not None and team2_id is not None:
            team1_info = get_team_info(team1_id)
            team2_info = get_team_info(team2_id)
            self.team_ids = {"team1": team1_id, "team2": team2_id}
            self.player_usernames = {
                team1_id: [team1_info["leadUser"]["username"]]
                + [member["username"] for member in team1_info["members"]],
                team2_id: [team2_info["leadUser"]["username"]]
                + [member["username"] for member in team2_info["members"]],
            }
        self.active_players = []
        self.banned_topics = []
        self.picked_topics = []
        self.action_count = 0
        # For auto-start and game duration
        self.game_start_time = (
            None  # Timestamp when the game should auto-start (30 sec later)
        )
        self.game_end_time = (
            None  # Timestamp when the game ends (60 min after game starts)
        )

    def sync_from_db(self):
        room_data = rooms_collection.find_one({"room_id": self.room_id})
        if room_data:
            self.phase = room_data["phase"]
            self.team_ids = room_data["team_ids"]
            self.player_usernames = room_data["player_usernames"]
            self.active_players = room_data["active_players"]
            self.banned_topics = room_data["banned_topics"]
            self.picked_topics = room_data["picked_topics"]
            self.action_count = room_data.get("action_count", 0)
            self.game_start_time = room_data.get("game_start_time")
            self.game_end_time = room_data.get("game_end_time")
        else:
            raise ValueError("Room not found")

    def sync_to_db(self):
        if self.team_ids is None or self.player_usernames is None:
            raise ValueError("Room is not properly initialized")

        rooms_collection.update_one(
            {"room_id": self.room_id},
            {
                "$set": {
                    "phase": self.phase.name,
                    "team_ids": self.team_ids,
                    "player_usernames": self.player_usernames,
                    "active_players": self.active_players,
                    "banned_topics": self.banned_topics,
                    "picked_topics": self.picked_topics,
                    "action_count": self.action_count,
                    "game_start_time": self.game_start_time,
                    "game_end_time": self.game_end_time,
                }
            },
            upsert=True,
        )

    def handle_room_phase(self):
        self.sync_from_db()

        total_players = len(self.active_players)

        if total_players < 6:
            self.action_count = 0
            self.banned_topics = []
            self.picked_topics = []
            self.phase = RoomPhase.WAITING
            self.game_start_time = None
            self.game_end_time = None
            self.sync_to_db()
            return

        if self.action_count < 12:
            self.phase = RoomPhase.DRAFT
            self.sync_to_db()
            return

        current_time = time.time()

        if self.phase == RoomPhase.DRAFT:
            self.phase = RoomPhase.PLAYING
            self.game_start_time = current_time + 30
            self.game_end_time = self.game_start_time + 60 * 60

        if self.phase == RoomPhase.PLAYING and current_time >= self.game_end_time:
            self.phase = RoomPhase.FINISHED

        self.sync_to_db()

    def handle_action(self, player_username, action_type, topic):
        self.sync_from_db()

        player_team = None
        for team_key, team_id in self.team_ids.items():
            if player_username in self.player_usernames[team_id]:
                player_team = team_key
                break

        if not player_team:
            raise ValueError("Player not found in any team")

        if self.action_count >= len(ACTION_SEQUENCE):
            raise ValueError("No more actions allowed")

        expected_action, expected_team = ACTION_SEQUENCE[self.action_count]

        if action_type != expected_action:
            raise ValueError(f"Expected {expected_action} action, got {action_type}")

        if player_team != expected_team:
            raise ValueError(f"Expected team {expected_team}, got team {player_team}")

        match action_type:
            case ActionType.BAN:
                if topic in self.banned_topics:
                    raise ValueError("Topic already banned")
                if topic in self.picked_topics:
                    raise ValueError("Cannot ban a picked topic")
                self.banned_topics.append(topic)
            case ActionType.PICK:
                if topic in self.picked_topics:
                    raise ValueError("Topic already picked")
                if topic in self.banned_topics:
                    raise ValueError("Cannot pick a banned topic")
                self.picked_topics.append(topic)

        self.action_count += 1

        self.sync_to_db()
        self.handle_room_phase()

    def add_player(self, player_username):
        self.sync_from_db()

        if len(self.active_players) >= MAX_ROOM_CAPACITY:
            raise ValueError("Room is full")

        if player_username in self.active_players:
            raise ValueError("Player already in the room")

        if (
            player_username not in self.player_usernames[self.team_ids["team1"]]
            and player_username not in self.player_usernames[self.team_ids["team2"]]
        ):
            raise ValueError("Player is not supposed to be in this room")

        self.active_players.append(player_username)
        self.sync_to_db()
        self.handle_room_phase()

    def remove_player(self, player_username):
        self.sync_from_db()

        if player_username not in self.active_players:
            raise ValueError("Player not in the room")

        self.active_players.remove(player_username)
        self.sync_to_db()
        self.handle_room_phase()

    def choose_problems(self):
        self.sync_from_db()

        if not self.picked_topics:
            raise ValueError("No topics picked yet")

        if self.phase != RoomPhase.PLAYING:
            raise ValueError("Room is not in PLAYING phase")
        
        if self.game_start_time is not None and time.time() < self.game_start_time:
            raise ValueError("Game has not started yet")

        tag_name_to_id = get_algoleague_problem_tags_and_ids()

        for topic in self.picked_topics:
            if topic not in tag_name_to_id:
                raise ValueError(f"Topic {topic} is not a valid tag")

        # TODO: Find a way to deal with tags with a few problems
        chosen_problems = []

        for topic in self.picked_topics:
            tag_id = tag_name_to_id.get(topic)
            if not tag_id:
                raise ValueError(f"Tag ID not found for topic {topic}")
            problems = get_problems_by_tag_id(tag_id)
            if not problems:
                raise ValueError(f"No problems found for topic {topic}")
            chosen_problems.append(random.choice(problems))

        return chosen_problems
