from app.utils.get_algoleague_problem_tags import get_algoleague_problem_tags_and_ids
from flask import Blueprint, jsonify

tags_bp = Blueprint("tags", __name__)


@tags_bp.route("/tags", methods=["GET"])
def get_tags():
    """
    Return a list of all algoleague tags.
    """
    tags = get_algoleague_problem_tags_and_ids()
    return jsonify(tags)
