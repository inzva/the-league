from flask import Blueprint, jsonify
from models.room import Room, rooms_collection

rooms_bp = Blueprint('rooms', __name__)

@rooms_bp.route('/rooms', methods=['POST'])
def create_room():
    """
    Create a new room and return its ID.
    """
    max_id_doc = rooms_collection.find_one(sort=[("room_id", -1)])
    new_id = (max_id_doc['room_id'] + 1) if max_id_doc else 1
    new_room = Room(new_id)
    new_room.sync_to_db()
    return jsonify({"room_id": new_id}), 201

@rooms_bp.route('/rooms', methods=['GET'])
def get_rooms():
    """
    Get a list of all room IDs.
    """
    all_rooms = rooms_collection.find({}, {"room_id": 1})
    room_ids = [room['room_id'] for room in all_rooms]
    return jsonify(room_ids)
