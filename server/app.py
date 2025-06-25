#!/usr/bin/env python3
from models import User
from controller import Donations, Users
from flask import request, session, make_response,jsonify
from flask_restful import Resource

from config import app, db, api

with app.app_context():
    db.create_all()

class Signup(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            return make_response(jsonify({"errors": "Missing signup data."}), 422)

        try:
            new_user = User(
                username=data["username"],
                bio=data.get("bio", ""),
                image_url=data.get("image_url", ""),
            )
            new_user.password_hash = data["password"]

            db.session.add(new_user)
            db.session.commit()

            session["user_id"] = new_user.id


            return make_response(jsonify(new_user.to_dict()), 201)

        except (KeyError, TypeError):
            return make_response(jsonify({"errors": ["Invalid input format."]}), 422)

        except AttributeError as ae:
            return make_response(jsonify({"errors": [str(ae)]}), 422)

        except Exception as e:
            return make_response(jsonify({"errors": [str(e)]}), 422)

class CheckSession(Resource):
    def get(self):

        if session.get("user_id"):
            user_id = session["user_id"]

            user = User.query.filter_by(id=user_id).first()
            response = make_response(jsonify(user.to_dict()), 200)

            return response
        
        return make_response(jsonify({"error":"User is not logged in"}), 401)


class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data["username"]
        password = data["password"]
        user = User.query.filter_by(username=username).first()

        if user and user.authenticate(password):
            response = make_response(jsonify(user.to_dict()), 200)
            session["user_id"] = user.id


            return response
        
        return make_response(jsonify({"Error":"User is not authorised"}), 401)
class Logout(Resource):
    def delete(self):
        if session.get("user_id"):
            session["user_id"] = None
            return make_response(jsonify(''), 204)
        
        return make_response(jsonify({"error":"User is not logged in"}), 401)
 


        

api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(Donations, '/donations', endpoint='donations')
api.add_resource(Users, '/users', endpoint='users')


if __name__ == '__main__':
    app.run(port=5555, debug=True)