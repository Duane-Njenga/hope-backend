from flask import Blueprint, request, jsonify
from server.models import Donation, User
from server.config import db

donations_bp = Blueprint('donations', __name__, url_prefix='/donations')

@donations_bp.route('', methods=['GET'])
def get_donations():
    """Get all donations"""
    donations = [donation.to_dict() for donation in Donation.query.all()]
    return jsonify(donations), 200

@donations_bp.route('', methods=['POST'])
def create_donation():
    """Create a new donation"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing donation data"}), 422
    
    try:
        # Validate user exists if user_id is provided
        if "user_id" in data and data["user_id"]:
            user = User.query.filter_by(id=data["user_id"]).first()
            if not user:
                return jsonify({"error": "User not found"}), 404

        new_donation = Donation(
            type=data["type"],
            group=data["group"],
            details=data.get("details", ""),
            phone_number=data.get("phone_number"),
            amount=data.get("amount"),
            user_id=data.get("user_id")
        )
        
        db.session.add(new_donation)
        db.session.commit()
        
        return jsonify(new_donation.to_dict()), 201
    
    except KeyError as e:
        return jsonify({"error": f"Missing required field: {str(e)}"}), 422
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 422

@donations_bp.route('/<int:donation_id>', methods=['GET'])
def get_donation(donation_id):
    """Get a specific donation by ID"""
    donation = Donation.query.filter_by(id=donation_id).first()
    if donation:
        return jsonify(donation.to_dict()), 200
    return jsonify({"error": "Donation not found"}), 404

@donations_bp.route('/<int:donation_id>', methods=['PUT'])
def update_donation(donation_id):
    """Update a specific donation"""
    donation = Donation.query.filter_by(id=donation_id).first()
    if not donation:
        return jsonify({"error": "Donation not found"}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing update data"}), 422
    
    try:
        if "type" in data:
            donation.type = data["type"]
        if "group" in data:
            donation.group = data["group"]
        if "details" in data:
            donation.details = data["details"]
        if "phone_number" in data:
            donation.phone_number = data["phone_number"]
        if "amount" in data:
            donation.amount = data["amount"]
        if "user_id" in data:
            # Validate user exists
            if data["user_id"]:
                user = User.query.filter_by(id=data["user_id"]).first()
                if not user:
                    return jsonify({"error": "User not found"}), 404
            donation.user_id = data["user_id"]
        
        db.session.commit()
        return jsonify(donation.to_dict()), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 422

@donations_bp.route('/<int:donation_id>', methods=['DELETE'])
def delete_donation(donation_id):
    """Delete a specific donation"""
    donation = Donation.query.filter_by(id=donation_id).first()
    if not donation:
        return jsonify({"error": "Donation not found"}), 404
    
    try:
        db.session.delete(donation)
        db.session.commit()
        return jsonify({"message": "Donation deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 422

@donations_bp.route('/by-type/<donation_type>', methods=['GET'])
def get_donations_by_type(donation_type):
    """Get donations by type"""
    donations = Donation.query.filter_by(type=donation_type).all()
    return jsonify([donation.to_dict() for donation in donations]), 200

@donations_bp.route('/by-group/<group_name>', methods=['GET'])
def get_donations_by_group(group_name):
    """Get donations by group"""
    donations = Donation.query.filter_by(group=group_name).all()
    return jsonify([donation.to_dict() for donation in donations]), 200