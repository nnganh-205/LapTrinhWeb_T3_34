from src import create_app
from flask import Flask
from models import db

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)