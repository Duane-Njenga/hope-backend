from flask import Blueprint, request, jsonify
from server.models.user import User
from server.config import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('', methods=['GET'])
def get_users():

    users = [user.to_dict() for user in User.query.all()]
    return jsonify(users), 200


@users_bp.route('/<int:user_id>/donations', methods=['GET'])
def get_user_donations(user_id):

    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    donations = [donation.to_dict() for donation in user.donations]
    return jsonify(donations), 200





@users_bp.route('/super-admin', methods=['GET'])
@jwt_required()
def super_admin():
    current_user = get_jwt_identity()

    if current_user['role'] != 'admin':
        return jsonify({'msg': 'Access denied'}), 403

    return jsonify({'msg': f'Welcome, Super Admin with email {current_user["email"]}!'})

