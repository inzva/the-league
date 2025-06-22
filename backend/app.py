from config import SECRET_KEY
from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
socketio = SocketIO(app)

if __name__ == '__main__':
    socketio.run(app)