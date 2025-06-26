from flask import Blueprint, request, jsonify
from server.models import User
from server.config import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    
    email = request.json.get('email')
    password = request.json.get('password')
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')

    if User.query.filter_by(email=email).first():
        return jsonify({'msg': 'User already exists'}), 409

    new_user = User(
        email=email,
        first_name=first_name,
        last_name=last_name
    )
    new_user.password_hash = password

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'msg': f'User {email} registered successfully'}), 201


@auth_bp.route('/login', methods=['POST'])
def login():

    email = request.json.get('email')
    password = request.json.get('password')

    user = User.query.filter_by(email=email).first()

    if not user or not user.authenticate(password):
        return jsonify({'msg': 'Invalid credentials'}), 401

    access_token = create_access_token(identity={
        'id': user.id,
        'email': user.email,
        'role': user.role
    })
    return jsonify(access_token=access_token)


@auth_bp.route('/check_session', methods=['GET'])
@jwt_required()
def check_session():

    current_user = get_jwt_identity()
    return jsonify(current_user), 200


@auth_bp.route('/logout', methods=['DELETE'])
@jwt_required()
def logout():

    return jsonify({"msg": "Token invalidation depends on client discarding token"}), 200
