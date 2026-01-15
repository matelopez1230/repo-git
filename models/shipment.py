"""
Modelo de Envío de Mercaderías
"""
from config.database import db

class Shipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    volume = db.Column(db.Float, nullable=False)  # en litros
    transport_mode = db.Column(db.String(20), nullable=False)  # 'land', 'air', 'sea'
    origin_country = db.Column(db.String(100), nullable=False)
    destination_country = db.Column(db.String(100), nullable=False)
    origin_port = db.Column(db.String(100), nullable=True)  # Aeropuerto, puerto marítimo o terrestre
    destination_port = db.Column(db.String(100), nullable=True)
    min_budget = db.Column(db.Float, nullable=False)
    max_budget = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)