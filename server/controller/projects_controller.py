from flask import make_response, jsonify, request
from models import Project
from flask_restful import Resource



class Projects(Resource):
    def get(self):
        projects = [project.to_dict() for project in Project.query.all()]

        response = make_response(jsonify(projects), 200)

        return response