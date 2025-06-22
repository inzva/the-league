from config import SECRET_KEY
from flask import Flask
from flask_socketio import SocketIO
from routes.rooms import rooms_bp
from routes.tags import tags_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
socketio = SocketIO(app)

app.register_blueprint(rooms_bp)
app.register_blueprint(tags_bp)

if __name__ == '__main__':
    socketio.run(app)