from flask import Blueprint, request, jsonify
from server.models import Volunteer,User
from server.config import db
from flask_jwt_extended import jwt_required, get_jwt_identity

volunteers_bp = Blueprint('volunteers', __name__, url_prefix='/volunteers')


# Get all volunteers (Admin use)
@volunteers_bp.route('', methods=['GET'])
@jwt_required()
def get_volunteers():
    user = get_jwt_identity()

    print(user )
    volunteers = [v.to_dict() for v in Volunteer.query.all()]
    return jsonify(volunteers), 200


@volunteers_bp.route('/check', methods=['GET'])
def check_volunteer():
    user_id = request.args.get("user_id")
    event_id = request.args.get("event_id")

    exists = Volunteer.query.filter_by(user_id=user_id, event_id=event_id).first()
    return jsonify({"volunteered": bool(exists)}), 200


# Volunteer for an event
@volunteers_bp.route('', methods=['POST'])
def create_volunteer():
    data = request.get_json()
    user_id = data.get("user_id")
    event_id = data.get("event_id")
    email= data.get("email")

    if not user_id or not event_id:
        return jsonify({"error": "Missing user_id or event_id"}), 422

    if Volunteer.query.filter_by(user_id=user_id, event_id=event_id).first():
        return jsonify({"error": "Already volunteering for this event"}), 409
    
    new_volunteer = Volunteer(user_id=user_id, event_id=event_id, email=email)
    db.session.add(new_volunteer)
    db.session.commit()

    return jsonify(new_volunteer.to_dict()), 201


@volunteers_bp.route('', methods=['DELETE'])
def delete_volunteer():
    user_id = request.args.get("user_id")
    event_id = request.args.get("event_id")


    volunteer = Volunteer.query.filter_by(user_id=user_id, event_id=event_id).first()

    if not volunteer:
        return jsonify({"error": "Not volunteering for this event"}), 404

    db.session.delete(volunteer)
    db.session.commit()

    return jsonify({"message": "Unvolunteered successfully"}), 200

