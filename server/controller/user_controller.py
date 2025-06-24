from flask import Blueprint, make_response, jsonify, request
from server.models.user import User

users_bp = Blueprint("users", __name__)

@users_bp.route("/users")
def get_donations():
    users = [user.to_dict() for user in User.query.all()]
    print(users)
    response = make_response(jsonify(users), 200)

    return response