"""
Modelo de Usuario
"""
from flask_login import UserMixin
from config.database import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    profile_pic = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # Relaciones
    posts = db.relationship('Post', backref='author', lazy=True)
    shipments = db.relationship('Shipment', backref='user', lazy=True)