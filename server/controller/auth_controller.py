from flask import Blueprint, request, session, jsonify
from server.models import User
from server.config import db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    print(data)
    # if not data:
    #     return jsonify({"errors": "Missing signup data."}), 422

    # try:
    #     existing_user = User.query.filter_by(email=data.get("email")).first()
    #     if existing_user:
    #         return jsonify({"errors": ["User with this email already exists."]}), 422

    #     new_user = User(
    #         first_name=data.get("first_name", ""),
    #         last_name=data.get("last_name", ""),
    #         email=data["email"]
    #     )
    #     new_user.password_hash = data["password"]

    #     db.session.add(new_user)
    #     db.session.commit()

    #     session["user_id"] = new_user.id
    #     return jsonify(new_user.to_dict()), 201

    # except KeyError as e:
    #     return jsonify({"errors": [f"Missing required field: {str(e)}"]}), 422
    # except Exception as e:
    #     return jsonify({"errors": [str(e)]}), 422

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing login data"}), 422
    
    email = data.get("email")
    password = data.get("password")
    
    if not email or not password:
        return jsonify({"error": "Email and password required"}), 422
    
    user = User.query.filter_by(email=email).first()
    
    if user and user.authenticate(password):
        session["user_id"] = user.id
        return jsonify(user.to_dict()), 200
    
    return jsonify({"error": "Invalid credentials"}), 401

@auth_bp.route('/logout', methods=['DELETE'])
def logout():
    if session.get("user_id"):
        session["user_id"] = None
        return jsonify({"message": "Logged out successfully"}), 204
    
    return jsonify({"error": "User is not logged in"}), 401

@auth_bp.route('/check_session', methods=['GET'])
def check_session():
    if session.get("user_id"):
        user_id = session["user_id"]
        user = User.query.filter_by(id=user_id).first()
        
        if user:
            return jsonify(user.to_dict()), 200
        else:
            return jsonify({"error": "User not found"}), 404
    
    return jsonify({"error": "User is not logged in"}), 401