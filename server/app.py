#!/usr/bin/env python3
from flask import Flask, jsonify
from server.config import db, DATABASE_URI, migrate, bcrypt
from server.controller import blueprints
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False
db.init_app(app)
migrate.init_app(app, db)
bcrypt.init_app(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

for blueprint in blueprints:
    app.register_blueprint(blueprint)


@app.route('/')
def index():
    return jsonify({"message": "Hope Connect backend is running"}), 200



if __name__ == '__main__':
    app.run(port=5555, debug=True)