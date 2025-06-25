from flask import Blueprint, make_response, jsonify, request
from server.models import Donation
from flask_restful import Resource



class Donations(Resource):
    def get(self):
        donations = [donation.to_dict() for donation in Donation.query.all()]

        response = make_response(jsonify(donations), 200)

        return response