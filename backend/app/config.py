import os

from dotenv import load_dotenv

from app.models.enums import ActionType

load_dotenv()

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_HOST = os.getenv("MONGO_HOST")
ALGOLEAGUE_COOKIE = os.getenv("ALGOLEAGUE_COOKIE")
SECRET_KEY = os.getenv("SECRET_KEY")

MAX_ROOM_CAPACITY = 6
ACTION_SEQUENCE = [
    (ActionType.BAN, "team1"),
    (ActionType.BAN, "team2"),
    (ActionType.BAN, "team2"),
    (ActionType.BAN, "team1"),
    (ActionType.PICK, "team1"),
    (ActionType.PICK, "team2"),
    (ActionType.BAN, "team2"),
    (ActionType.BAN, "team1"),
    (ActionType.PICK, "team1"),
    (ActionType.PICK, "team2"),
    (ActionType.PICK, "team2"),
    (ActionType.PICK, "team1"),
]

MONGO_URI = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}/?retryWrites=true&w=majority"
