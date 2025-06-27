import os
from dotenv import load_dotenv

load_dotenv()

MONGO_USER = os.getenv('MONGO_USER')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')
MONGO_HOST = os.getenv('MONGO_HOST')
ALGOLEAGUE_COOKIE = os.getenv('ALGOLEAGUE_COOKIE')
SECRET_KEY = os.getenv('SECRET_KEY')

MONGO_URI = (
    f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}"
    f"@{MONGO_HOST}/?retryWrites=true&w=majority"
)