from . import db
from datetime import datetime, timezone
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    user_name = db.Column(db.String(128), nullable = False)
    create_at = db.Column(db.DateTime(timezone=True), default = lambda: datetime.now(timezone.utc))