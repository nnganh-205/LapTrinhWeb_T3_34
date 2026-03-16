import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from dotenv import load_dotenv
load_dotenv()
def create_app():
    app = Flask(__name__)
    SECRET_KEY = os.getenv('SECRET_KEY')
    DB_NAME = os.getenv('DB_NAME')
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    from .models import User
    db.init_app(app)
    if not os.path.exists(f'instance/{DB_NAME}'):
        with app.app_context():
            db.create_all()
    from .user import user_bp
    from .auth_user import auth
    app.register_blueprint(user_bp)
    app.register_blueprint(auth)
    return app