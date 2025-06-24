from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()
db = SQLAlchemy()
migrate = Migrate()

# App configuration values
DATABASE_URI = 'sqlite:///app.db'
