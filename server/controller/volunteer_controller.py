from flask import Blueprint, make_response, jsonify, request
from server.models import User
from flask_restful import Resource



class Users(Resource):
    def get(self):
        users = [user.to_dict() for user in User.query.all()]

        response = make_response(jsonify(users), 200)

        return response