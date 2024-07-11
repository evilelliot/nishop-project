from flask import Blueprint, jsonify
from app.models.user import User
from app.models.product import Product
from app.models.categories import Category
from app.models.order_items import OrderItem
from app.models.sales import Sale
index_bp = Blueprint('index_bp', __name__)

@index_bp.route('/si', methods=['GET'])
def si():
    data = Sale.query.all()
    return jsonify({'data': [data.to_dict() for user in data]}), 200
