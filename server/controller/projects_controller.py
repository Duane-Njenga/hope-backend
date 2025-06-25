from flask import Blueprint, request, jsonify
from server.models import Project
from server.config import db

projects_bp = Blueprint('projects', __name__, url_prefix='/projects')

@projects_bp.route('', methods=['GET'])
def get_projects():
    """Get all projects"""
    projects = [project.to_dict() for project in Project.query.all()]
    return jsonify(projects), 200

@projects_bp.route('', methods=['POST'])
def create_project():
    """Create a new project"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing project data"}), 422
    
    try:
        new_project = Project(
            type=data["type"],
            description=data["description"]
        )
        
        db.session.add(new_project)
        db.session.commit()
        
        return jsonify(new_project.to_dict()), 201
    
    except KeyError as e:
        return jsonify({"error": f"Missing required field: {str(e)}"}), 422
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 422

@projects_bp.route('/<int:project_id>', methods=['GET'])
def get_project(project_id):
    """Get a specific project by ID"""
    project = Project.query.filter_by(id=project_id).first()
    if project:
        return jsonify(project.to_dict()), 200
    return jsonify({"error": "Project not found"}), 404

@projects_bp.route('/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    """Update a specific project"""
    project = Project.query.filter_by(id=project_id).first()
    if not project:
        return jsonify({"error": "Project not found"}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing update data"}), 422
    
    try:
        if "type" in data:
            project.type = data["type"]
        if "description" in data:
            project.description = data["description"]
        
        db.session.commit()
        return jsonify(project.to_dict()), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 422

@projects_bp.route('/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    """Delete a specific project"""
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

@projects_bp.route('/by-type/<project_type>', methods=['GET'])
def get_projects_by_type(project_type):
    """Get projects by type"""
    projects = Project.query.filter_by(type=project_type).all()
    return jsonify([project.to_dict() for project in projects]), 200