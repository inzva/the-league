from flask import Blueprint, jsonify, request
from models.room import Room, rooms_collection

rooms_bp = Blueprint("rooms", __name__)


@rooms_bp.route("/rooms", methods=["POST"])
def create_room():
    """
    Create a new room with given team IDs and return its ID.

    Parameters:
    - team1_id (int): ID of the first team.
    - team2_id (int): ID of the second team.
    """
    team1_id = request.json.get("team1_id")
    team2_id = request.json.get("team2_id")

    max_id_doc = rooms_collection.find_one(sort=[("room_id", -1)])
    new_id = (max_id_doc["room_id"] + 1) if max_id_doc else 1

    new_room = Room(new_id, team1_id, team2_id)
    new_room.sync_to_db()

    return jsonify({"room_id": new_id}), 201


@rooms_bp.route("/rooms", methods=["GET"])
def get_rooms():
    """
    Get a list of all room IDs.
    """
    all_rooms = rooms_collection.find({}, {"room_id": 1})
    room_ids = [room["room_id"] for room in all_rooms]
    return jsonify(room_ids)
