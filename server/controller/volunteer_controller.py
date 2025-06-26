from flask import Blueprint, request, jsonify
from server.models.volunteer import Volunteer
from server.config import db

volunteers_bp = Blueprint('volunteers', __name__, url_prefix='/volunteers')


@volunteers_bp.route('', methods=['GET'])
def get_volunteers():
    volunteers = [v.to_dict() for v in Volunteer.query.all()]
    return jsonify(volunteers), 200


@volunteers_bp.route('', methods=['POST'])
def create_volunteer():
    data = request.get_json()

    required_fields = ["name", "email", "phone_number"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 422

    if Volunteer.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Volunteer with that email already exists"}), 409

    new_volunteer = Volunteer(
        name=data["name"],
        email=data["email"],
        phone_number=data["phone_number"],
        age=data.get("age"),
        city=data.get("city")
    )

    db.session.add(new_volunteer)
    db.session.commit()

    return jsonify(new_volunteer.to_dict()), 201
