from flask import Blueprint, request, jsonify
from server.models import User
from server.config import db

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('', methods=['GET'])
def get_users():
    """Get all users"""
    users = [user.to_dict() for user in User.query.all()]
    return jsonify(users), 200

@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get a specific user by ID"""
    user = User.query.filter_by(id=user_id).first()
    if user:
        return jsonify(user.to_dict()), 200
    return jsonify({"error": "User not found"}), 404

@users_bp.route('/<int:user_id>/donations', methods=['GET'])
def get_user_donations(user_id):
    """Get all donations for a specific user"""
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    donations = [donation.to_dict() for donation in user.donations]
    return jsonify(donations), 200