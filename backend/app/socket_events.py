from typing import Dict

from flask_socketio import SocketIO, emit, join_room, leave_room

from app.models.enums import ActionType
from app.models.room import Room

rooms_state: Dict[str, Room] = {}

# TODO: Find a way to handle operations without needing username as input,
# request sid should be enough and it is a much more reliable method.


class WebSocketServer:
    def __init__(self, socketio_instance: SocketIO):
        self.socketio = socketio_instance

    def _broadcast_state(self, room_id):
        room_state = rooms_state.get(room_id)

        if not room_state:
            emit("error", {"message": "Room not found"})
            return

        room_state.sync_from_db()

        emit(
            "room_state",
            {
                "room_id": room_state.room_id,
                "phase": room_state.phase,
                "team_ids": room_state.team_ids,
                "player_usernames": room_state.player_usernames,
                "active_players": room_state.active_players,
                "banned_topics": room_state.banned_topics,
                "picked_topics": room_state.picked_topics,
                "action_count": room_state.action_count,
                "game_start_time": room_state.game_start_time,
                "game_end_time": room_state.game_end_time,
            },
            to=f"room_{room_id}",
        )

    def register_events(self):
        @self.socketio.on("join_room")
        def handle_join(data):
            """
            Handle a user joining a room.

            This will add the user to the room's player list and broadcast the updated room state.

            Parameters:
            - username (str): The username of the user joining the room.
            - room_id (int): The ID of the room to join.
            """
            username = data.get("username")
            room_id = data.get("room_id")

            if not username or not room_id:
                emit(
                    "error", {"message": "You should provide both username and room_id"}
                )
                return

            room = Room(room_id)

            try:
                room.sync_from_db()
            except ValueError:
                emit("error", {"message": "Room not found"})
                return

            try:
                room.add_player(username)
            except ValueError as e:
                emit("error", {"message": str(e)})
                return

            room_key = f"room_{room_id}"
            join_room(room_key)
            rooms_state[room_id] = room
            self._broadcast_state(room_id)

        @self.socketio.on("leave_room")
        def handle_leave(data):
            """
            Handle a user leaving a room.

            This will remove the user from the room's player list and broadcast the updated room state.

            Parameters:
            - username (str): The username of the user leaving the room.
            - room_id (int): The ID of the room to leave.
            """
            room_id = data.get("room_id")
            username = data.get("username")

            if not room_id or not username:
                return

            room = Room(room_id)

            try:
                room.sync_from_db()
            except ValueError:
                emit("error", {"message": "Room not found"})
                return

            try:
                room.remove_player(username)
            except ValueError as e:
                emit("error", {"message": str(e)})
                return

            room_key = f"room_{room_id}"
            leave_room(room_key)
            self._broadcast_state(room_id)

        @self.socketio.on("pick")
        def handle_pick(data):
            """
            Handle a user picking a topic.

            This will add the topic to the room's picked topics and broadcast the updated room state.

            Parameters:
            - username (str): The username of the user picking the topic.
            - room_id (int): The ID of the room to pick the topic in.
            - topic (str): The topic being picked.
            """
            username = data.get("username")
            room_id = data.get("room_id")
            topic = data.get("topic")

            if not room_id or not username or not topic:
                return

            room = Room(room_id)

            try:
                room.sync_from_db()
            except ValueError:
                emit("error", {"message": "Room not found"})
                return

            try:
                room.handle_action(username, ActionType.PICK, topic)
            except ValueError as e:
                emit("error", {"message": str(e)})
                return

            room_key = f"room_{room_id}"
            leave_room(room_key)
            self._broadcast_state(room_id)

        @self.socketio.on("ban")
        def handle_ban(data):
            """
            Handle a user banning a topic.

            This will add the topic to the room's banned topics and broadcast the updated room state.

            Parameters:
            - username (str): The username of the user banning the topic.
            - room_id (int): The ID of the room to ban the topic in.
            - topic (str): The topic being banned.
            """
            username = data.get("username")
            room_id = data.get("room_id")
            topic = data.get("topic")

            if not room_id or not username or not topic:
                return

            room = Room(room_id)

            try:
                room.sync_from_db()
            except ValueError:
                emit("error", {"message": "Room not found"})
                return

            try:
                room.handle_action(username, ActionType.BAN, topic)
            except ValueError as e:
                emit("error", {"message": str(e)})
                return

            room_key = f"room_{room_id}"
            leave_room(room_key)
            self._broadcast_state(room_id)

        # @socketio.on("set_ready")
        # def handle_set_ready(data):
        #     room_id = data.get("room_id")
        #     username = data.get("username")
        #     ready = data.get("ready")
        #     if room_id is None or username is None or ready is None:
        #         emit("error", {"message": "room_id, username, ready gerekli"})
        #         return
        #     room = rooms_state.get(room_id)
        #     if not room or username not in room["players"]:
        #         emit("error", {"message": "Oyuncu odada değil"})
        #         return
        #     room["players"][username]["ready"] = bool(ready)
        #     _broadcast_state(room_id)

        # @socketio.on("disconnect")
        # def handle_disconnect():
        #     sid = request.sid
        #     to_update = []
        #     for room_id, room in list(rooms_state.items()):
        #         for username, info in list(room["players"].items()):
        #             if info.get("sid") == sid:
        #                 del room["players"][username]
        #                 to_update.append(room_id)
        #         if not room["players"]:
        #             del rooms_state[room_id]
        #     for rid in to_update:
        #         _broadcast_state(rid)
