from enum import Enum
from pymongo import MongoClient
from config import MONGO_URI

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
    def __init__(self, room_id):
        self.room_id = room_id
        self.phase = RoomPhase.WAITING
        self.player_ids = {1: [], 2: []}
        self.banned_topics = []
        self.picked_topics = []

    def sync_to_db(self):
        rooms_collection.update_one(
            {"room_id": self.room_id},
            {"$set": {
                "phase": self.phase.name,
                "banned_topics": self.banned_topics,
                "picked_topics": self.picked_topics
            }},
            upsert=True
        )

    def sync_from_db(self):
        room_data = rooms_collection.find_one({"room_id": self.room_id})
        if room_data:
            self.phase = room_data["phase"]
            self.banned_topics = room_data["banned_topics"]
            self.picked_topics = room_data["picked_topics"]

    def add_player(self, player_id, team):
        # TODO: Add the player to the specified team
        # If the player is the last player, set the room phase to BAN
        pass

    def remove_player(self, player_id, team):
        # TODO: Remove the player from the specified team, delete all previous events.
        # TODO: If the room state is not WAITING, set the room phase to WAITING
        pass

    def handle_action(self, player_id, action_type):
        if action_type == ActionType.BAN:
            # TODO: Check if the room is in the BAN phase and it is the player's turn
            # TODO: Check if the topic is not already banned
            # TODO: Add the topic to the banned topics list
            # TODO: If all topics are banned, set the room phase to PICK
            pass
        elif action_type == ActionType.PICK:
            # TODO: Check if the room is in the PICK phase and it is the player's turn
            # TODO: Check if the topic is not already picked
            # TODO: Add the topic to the picked topics list
            # TODO: If all topics are picked, set the room phase to PLAYING
            pass
        else:
            raise ValueError("Invalid action type")