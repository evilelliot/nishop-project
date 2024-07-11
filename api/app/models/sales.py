from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from app.models.db import db

class Sale(db.Model):
    __tablename__ = 'sales'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    sale_date = db.Column(db.TIMESTAMP, default=datetime.now)

    def __repr__(self):
        return f"<Sale(id={self.id}, order_id={self.order_id}, user_id={self.user_id}, total={self.total})>"

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'user_id': self.user_id,
            'total': str(self.total),  # Convertimos a string para evitar problemas con JSON
            'sale_date': self.sale_date.isoformat()
        }
