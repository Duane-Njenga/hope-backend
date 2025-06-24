from flask import Blueprint, make_response, jsonify, request
from server.models.donation import Donation

donations_bp = Blueprint("donations", __name__)

@donations_bp.route("/donations")
def get_donations():
    donations = [d.to_dict() for d in Donation.query.all()]
    print(donations)
    response = make_response(jsonify(donations), 200)

    return response
