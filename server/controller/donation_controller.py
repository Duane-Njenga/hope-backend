from flask import Blueprint, request, jsonify
from server.models import Donation, User
from server.config import db
from flask_jwt_extended import jwt_required, get_jwt_identity

donations_bp = Blueprint('donations', __name__, url_prefix='/donations')

@donations_bp.route('', methods=['GET'])
def get_donations():

    donations = [donation.to_dict() for donation in Donation.query.all()]
    return jsonify(donations), 200

@donations_bp.route('', methods=['POST'])
@jwt_required()
def create_donation():
    current_user = get_jwt_identity()

    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing donation data"}), 422
    
    try:
        user_id = current_user.get("id")
        if user_id:
            user = User.query.filter_by(id=user_id).first()
            if not user:
                return jsonify({"error": "User not found"}), 404

        new_donation = Donation(
            type=data["type"],
            group=data["group"],
            details=data.get("details", ""),
            phone_number=data.get("phone_number"),
            amount=data.get("amount"),
            user_id=user_id
        )
        
        db.session.add(new_donation)
        db.session.commit()
        
        return jsonify(new_donation.to_dict()), 201
    
    except KeyError as e:
        return jsonify({"error": f"Missing required field: {str(e)}"}), 422
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 422


@donations_bp.route('/by-type/<donation_type>', methods=['GET'])
def get_donations_by_type(donation_type):

    donations = Donation.query.filter_by(type=donation_type).all()
    return jsonify([donation.to_dict() for donation in donations]), 200

@donations_bp.route('/by-group/<group_name>', methods=['GET'])
def get_donations_by_group(group_name):

    donations = Donation.query.filter_by(group=group_name).all()

    return jsonify([donation.to_dict() for donation in donations]), 200