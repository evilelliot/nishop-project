from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from app.models.db import db

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    status = db.Column(db.String(20), nullable=False, default='pending')
    total = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.now)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"<Order(id={self.id}, user_id={self.user_id}, status={self.status}, total={self.total})>"

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'status': self.status,
            'total': str(self.total),  # Convertimos a string para evitar problemas con JSON
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
