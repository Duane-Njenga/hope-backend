from flask import Flask, jsonify
from server.config import db, migrate, DATABASE_URI, bcrypt
from server.models import user, donation  # Ensures models are imported
from server.controller import blueprints

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False
bcrypt.__init__(app)

db.init_app(app)
migrate.init_app(app, db)

for blueprint in blueprints:
    app.register_blueprint(blueprint)

@app.route('/')
def index():
    return jsonify({"message": "Hope Connect API"})

if __name__ == '__main__':
    app.run(port=5555, debug=True)
