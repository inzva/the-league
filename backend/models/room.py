from enum import Enum
from pymongo import MongoClient
from config import MONGO_URI
from utils.get_problem_by_tag import get_problems_by_tag_id
from utils.get_algoleague_problem_tags import get_algoleague_problem_tags_and_ids
from utils.get_team_info import get_team_info
import random, time

client = MongoClient(MONGO_URI)
db = client.theleague
rooms_collection = db.rooms

class RoomPhase(Enum):
    WAITING = 0
    BAN = 1
    PICK = 2
    PLAYING = 3
    FINISHED = 4

class ActionType(Enum):
    BAN = 1
    PICK = 2

class Room:
    def __init__(self, room_id, team1_id=None, team2_id=None):
        self.room_id = room_id
        self.phase = RoomPhase.WAITING
        team1_info = get_team_info(team1_id)
        team2_info = get_team_info(team2_id)
        self.team_ids = {
            "team1": team1_id,
            "team2": team2_id
        }
        self.player_usernames = {
            team1_id: [team1_info["leadUser"]["username"]] + [member["username"] for member in team1_info["members"]],
            team2_id: [team2_info["leadUser"]["username"]] + [member["username"] for member in team2_info["members"]]
        }
        self.active_players = []
        self.banned_topics = []
        self.picked_topics = []
        self.action_count = 0
        # For auto-start and game duration
        self.game_start_time = None   # Timestamp when the game should auto-start (30 sec later)
        self.game_end_time = None     # Timestamp when the game ends (60 min after game starts)

    def sync_to_db(self):
        rooms_collection.update_one(
            {"room_id": self.room_id},
            {"$set": {
                "phase": self.phase.name,
                "player_usernames": self.player_usernames,
                "banned_topics": self.banned_topics,
                "picked_topics": self.picked_topics,
                "action_count": self.action_count,
                "game_start_time": self.game_start_time,
                "game_end_time": self.game_end_time,
                "active_players": self.active_players if self.active_players else []
            }},
            upsert=True
        )

    def sync_from_db(self):
        room_data = rooms_collection.find_one({"room_id": self.room_id})
        if room_data:
            self.phase = room_data["phase"]
            self.player_usernames = room_data["player_usernames"]
            self.banned_topics = room_data["banned_topics"]
            self.picked_topics = room_data["picked_topics"]
            self.action_count = room_data.get("action_count", 0)
            self.game_start_time = room_data.get("game_start_time")
            self.game_end_time = room_data.get("game_end_time")

    def get_current_action_and_team(self):
        if self.active_players < 6:
            return None, None
        # Complete action sequence: (action_type, team)
        action_sequence = [
            (ActionType.BAN, 1),   # Team 1 bans
            (ActionType.BAN, 2),   # Team 2 bans
            (ActionType.BAN, 2),   # Team 2 bans
            (ActionType.BAN, 1),   # Team 1 bans
            (ActionType.PICK, 1),  # Team 1 picks
            (ActionType.PICK, 2),  # Team 2 picks
            (ActionType.BAN, 2),   # Team 2 bans
            (ActionType.BAN, 1),   # Team 1 bans
            (ActionType.PICK, 1),  # Team 1 picks
            (ActionType.PICK, 2),  # Team 2 picks
            (ActionType.PICK, 2),  # Team 2 picks
            (ActionType.PICK, 1)   # Team 1 picks
        ]
        
        if self.action_count >= len(action_sequence):
            return None, None
        return action_sequence[self.action_count]

    def handle_action(self, player_username, action_type, topic):
        self.sync_from_db()

        # Find which team the player belongs to
        player_team = None
        for team_key, team_id in self.team_ids.items():
            if player_username in self.player_usernames[team_id]:
                player_team = team_key
                break
        
        if not player_team:
            raise ValueError("Player not found in any team")

        expected_action, expected_team = self.get_current_action_and_team()

        if expected_action is None:
            raise ValueError("No more actions allowed")
            
        if action_type != expected_action:
            raise ValueError(f"Expected {expected_action} action, got {action_type}")
            
        if player_team != expected_team:
            raise ValueError(f"Expected team {expected_team}, got team {player_team}")

        if action_type == ActionType.BAN:
            if self.phase != RoomPhase.BAN:
                raise ValueError("Room is not in BAN phase")
            
            if topic in self.banned_topics:
                raise ValueError("Topic already banned")
            
            self.banned_topics.append(topic)
            
        elif action_type == ActionType.PICK:
            if self.phase != RoomPhase.PICK:
                self.phase = RoomPhase.PICK
                
            if topic in self.picked_topics:
                raise ValueError("Topic already picked")
                
            if topic in self.banned_topics:
                raise ValueError("Cannot pick a banned topic")
                
            self.picked_topics.append(topic)
        
        self.action_count += 1
        
        # Check if we should transition to PLAYING phase
        if self.action_count >= 12:  # Total number of actions
            self.phase = RoomPhase.PLAYING
            
        self.sync_to_db()

    def get_random_problem_id(self):
        self.sync_from_db()
        if not self.picked_topics:
            raise ValueError("No topics picked yet")
        if self.phase != RoomPhase.PLAYING:
            raise ValueError("Room is not in PLAYING phase")
            
        # Get mapping of tag names to IDs
        tag_name_to_id = get_algoleague_problem_tags_and_ids()

        for topic in self.picked_topics:
            if topic in self.banned_topics:
                raise ValueError(f"Topic {topic} is banned, cannot get a problem")
            if topic not in tag_name_to_id:
                raise ValueError(f"Topic {topic} is not a valid tag")
        
        # Get all available problems from picked topics
        # NOT: Az sayıda soru içeren taglar için vb başka çözümler ileride geliştirilebilir
        available_problems = []
        for topic in self.picked_topics:
            tag_id = tag_name_to_id.get(topic)
            if tag_id:
                problems = get_problems_by_tag_id(tag_id)
                available_problems.extend(problems)
        
        if not available_problems:
            return None
            
        # Return a random problem ID
        return random.choice(available_problems)

    def check_game_end(self):
        self.sync_from_db()
        # Call this periodically (or at action points) to end the game when time is up.
        current_time = time.time()
        if self.phase == RoomPhase.PLAYING and self.game_end_time and current_time >= self.game_end_time:
            self.phase = RoomPhase.FINISHED
            self.sync_to_db()

    def check_and_update_start_status(self):
        self.sync_from_db()
        total_players = len(self.active_players)
        current_time = time.time()
        if total_players == 6 and self.action_count == 12:
            if not self.game_start_time:
                # Set game to start 30 seconds later
                self.game_start_time = current_time + 30
                self.sync_to_db()
            elif current_time >= self.game_start_time:
                # Start game by moving phase to PLAYING and set end time to 60 minutes later
                self.phase = RoomPhase.PLAYING
                self.game_end_time = current_time + 60 * 60
                self.sync_to_db()
        else:
            # If players drop below 6, cancel any pending start or reset playing state
            if total_players < 6:
                self.phase = RoomPhase.WAITING
                self.game_start_time = None
                self.game_end_time = None
                self.sync_to_db()

    def add_player(self, player_username, team_key):
        self.sync_from_db()
        if team_key not in self.team_ids:
            raise ValueError("Invalid team key")
        # Check that the player is not already in any team
        for players in self.player_usernames.values():
            if player_username in players:
                raise ValueError("Player already in a team")
        team_id = self.team_ids[team_key]
        if len(self.player_usernames[team_id]) >= 3:
            raise ValueError("Team is already full")
        self.active_players.append(player_username)
        self.sync_to_db()
        self.check_and_update_start_status()

    def remove_player(self, player_username):
        self.sync_from_db()
        removed = False
        for team_id in self.player_usernames:
            if player_username in self.player_usernames[team_id]:
                self.active_players.remove(player_username)
                removed = True
                break
        if not removed:
            raise ValueError("Player not found in any team")
        self.sync_to_db()
        self.check_and_update_start_status()