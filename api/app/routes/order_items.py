from datetime import datetime
from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from app.models.db import db
from app.models.order_items import OrderItem

order_item_ns = Namespace('order_items', description='Order Item operations')

# Model
order_item_model = order_item_ns.model('OrderItem', {
    'id': fields.Integer(readonly=True),
    'order_id': fields.Integer(required=True),
    'product_id': fields.Integer(required=True),
    'quantity': fields.Integer(required=True),
    'price': fields.String(required=True),
    'created_at': fields.DateTime(readonly=True),
    'updated_at': fields.DateTime(readonly=True)
})

order_item_input_model = order_item_ns.model('OrderItemInput', {
    'order_id': fields.Integer(required=True),
    'product_id': fields.Integer(required=True),
    'quantity': fields.Integer(required=True),
    'price': fields.String(required=True)
})

order_item_update_model = order_item_ns.model('OrderItemUpdate', {
    'order_id': fields.Integer(),
    'product_id': fields.Integer(),
    'quantity': fields.Integer(),
    'price': fields.String()
})

# Read (List and Retrieve) - Protected
@order_item_ns.route('/')
class OrderItemList(Resource):
    @jwt_required()
    @order_item_ns.marshal_list_with(order_item_model)
    def get(self):
        """List all order items"""
        return OrderItem.query.all()

@order_item_ns.route('/<int:id>')
class OrderItemResource(Resource):
    @jwt_required()
    @order_item_ns.marshal_with(order_item_model)
    @order_item_ns.response(404, 'Order Item not found')
    def get(self, id):
        """Retrieve an order item"""
        order_item = OrderItem.query.get_or_404(id)
        return order_item

    # Update - Protected
    @jwt_required()
    @order_item_ns.expect(order_item_update_model)
    @order_item_ns.marshal_with(order_item_model)
    @order_item_ns.response(404, 'Order Item not found')
    def put(self, id):
        """Update an order item"""
        order_item = OrderItem.query.get_or_404(id)
        data = request.json
        
        if 'order_id' in data:
            order_item.order_id = data['order_id']
        if 'product_id' in data:
            order_item.product_id = data['product_id']
        if 'quantity' in data:
            order_item.quantity = data['quantity']
        if 'price' in data:
            order_item.price = data['price']
        
        order_item.updated_at = datetime.now()
        db.session.commit()
        return order_item

    # Delete - Protected
    @jwt_required()
    @order_item_ns.response(204, 'Order Item deleted')
    @order_item_ns.response(404, 'Order Item not found')
    def delete(self, id):
        """Delete an order item"""
        order_item = OrderItem.query.get_or_404(id)
        db.session.delete(order_item)
        db.session.commit()
        return '', 204

# Create - Protected
@order_item_ns.route('/create')
class OrderItemCreate(Resource):
    @jwt_required()
    @order_item_ns.expect(order_item_input_model)
    @order_item_ns.marshal_with(order_item_model, code=201)
    def post(self):
        """Create a new order item"""
        data = request.json
        new_order_item = OrderItem(
            order_id=data['order_id'],
            product_id=data['product_id'],
            quantity=data['quantity'],
            price=data['price']
        )
        db.session.add(new_order_item)
        db.session.commit()
        return new_order_item, 201
