"""
Modelo de Oferta para Envíos
"""
from config.database import db

class Offer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shipment_id = db.Column(db.Integer, db.ForeignKey('shipment.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # Relaciones
    shipment = db.relationship('Shipment', backref='offers')
    user = db.relationship('User', backref='offers')