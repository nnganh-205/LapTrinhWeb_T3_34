import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from dotenv import load_dotenv
load_dotenv()
def create_app():
    app = Flask(__name__)
    from .user import user_bp
    app.register_blueprint(user_bp, url_prefix = '/')
    return app