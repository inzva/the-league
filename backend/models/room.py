from enum import Enum
from pymongo import MongoClient
from config import MONGO_URI
from utils.get_problem_by_tag import get_problems_by_tag_id
from utils.get_algoleague_problem_tags import get_algoleague_problem_tags_and_ids
from utils.get_team_info import get_team_info
import random

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
        self.banned_topics = []
        self.picked_topics = []
        self.action_count = 0

    def sync_to_db(self):
        rooms_collection.update_one(
            {"room_id": self.room_id},
            {"$set": {
                "phase": self.phase.name,
                "player_usernames": self.player_usernames,
                "banned_topics": self.banned_topics,
                "picked_topics": self.picked_topics,
                "action_count": self.action_count
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

    def get_current_action_and_team(self):
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