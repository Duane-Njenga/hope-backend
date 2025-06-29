from flask import Blueprint, request, jsonify
from server.models import Project
from server.config import db
from flask_jwt_extended import jwt_required, get_jwt_identity
import json


projects_bp = Blueprint('projects', __name__, url_prefix='/projects')

@projects_bp.route('', methods=['GET'])
def get_projects():
    
    projects = [project.to_dict() for project in Project.query.all()]
    return jsonify(projects), 200

@projects_bp.route('', methods=['POST'])
def create_project():
     
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing project data"}), 422
    
    try:
        new_project = Project(
            type=data["type"],
            description=data["description"],
            date = data["date"],
            image_url=data["image_url"]
        )
        
        db.session.add(new_project)
        db.session.commit()
        
        return jsonify(new_project.to_dict()), 201
    
    except KeyError as e:
        return jsonify({"error": f"Missing required field: {str(e)}"}), 422
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 422


@projects_bp.route('/<int:project_id>', methods=['DELETE'])
@jwt_required()
def delete_project(project_id):

    current_user = get_jwt_identity()
    if current_user["role"] != "admin":
        return jsonify({"error": "Unauthorised User"}), 422

    project = Project.query.filter_by(id=project_id).first()
    if not project:
        return jsonify({"error": "Project not found"}), 404
    
    try:
        db.session.delete(project)
        db.session.commit()
        return jsonify({"message": "Project deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 422

