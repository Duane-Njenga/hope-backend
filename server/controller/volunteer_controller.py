from flask import Blueprint

volunteers_bp = Blueprint('volunteers', __name__)

@volunteers_bp.route('/volunteers')
def get_volunteers():
    return {"message": "Volunteers route working"}
