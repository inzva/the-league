# The League Backend

A Flask + Flask-SocketIO server for “The League” competitive programming pick-&-ban rooms.

## Installation

1. **Clone & create a virtual environment**

   ```bash
   git clone git@github.com:inzva/the-league.git
   cd the-league/backend
   python3 -m venv venv
   source venv/bin/activate    # macOS/Linux
   venv\Scripts\activate       # Windows
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt

   pip install -e .
   ```

3. **Configure environment variables**
   Copy the sample and fill in your values:

   ```bash
   cp .env.sample .env
   ```

   ```dotenv
   MONGO_USER=mongo_user
   MONGO_PASSWORD=mongo_password
   MONGO_HOST=theleague.ueyutny.mongodb.net
   SECRET_KEY=secret_key
   ```

## Running the Server

By default the app listens on port 5000 and allows CORS from any origin.

```bash
python app/main.py
```
