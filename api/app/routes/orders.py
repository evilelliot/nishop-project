from datetime import datetime
from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from app.models.db import db
from app.models.orders import Order

order_ns = Namespace('orders', description='Order operations')

# Model
order_model = order_ns.model('Order', {
    'id': fields.Integer(readonly=True),
    'user_id': fields.Integer(required=True),
    'status': fields.String(required=True),
    'total': fields.String(required=True),
    'created_at': fields.DateTime(readonly=True),
    'updated_at': fields.DateTime(readonly=True)
})

order_input_model = order_ns.model('OrderInput', {
    'user_id': fields.Integer(required=True),
    'status': fields.String(required=False),
    'total': fields.String(required=True)
})

order_update_model = order_ns.model('OrderUpdate', {
    'user_id': fields.Integer(),
    'status': fields.String(),
    'total': fields.String()
})

# Read (List and Retrieve) - Protected
@order_ns.route('/')
class OrderList(Resource):
    @jwt_required()
    @order_ns.marshal_list_with(order_model)
    def get(self):
        """List all orders"""
        return Order.query.all()

@order_ns.route('/<int:id>')
class OrderResource(Resource):
    @jwt_required()
    @order_ns.marshal_with(order_model)
    @order_ns.response(404, 'Order not found')
    def get(self, id):
        """Retrieve an order"""
        order = Order.query.get_or_404(id)
        return order

    # Update - Protected
    @jwt_required()
    @order_ns.expect(order_update_model)
    @order_ns.marshal_with(order_model)
    @order_ns.response(404, 'Order not found')
    def put(self, id):
        """Update an order"""
        order = Order.query.get_or_404(id)
        data = request.json
        
        if 'user_id' in data:
            order.user_id = data['user_id']
        if 'status' in data:
            order.status = data['status']
        if 'total' in data:
            order.total = data['total']
        
        order.updated_at = datetime.now()
        db.session.commit()
        return order

    # Delete - Protected
    @jwt_required()
    @order_ns.response(204, 'Order deleted')
    @order_ns.response(404, 'Order not found')
    def delete(self, id):
        """Delete an order"""
        order = Order.query.get_or_404(id)
        db.session.delete(order)
        db.session.commit()
        return '', 204

# Create - Protected
@order_ns.route('/create')
class OrderCreate(Resource):
    @jwt_required()
    @order_ns.expect(order_input_model)
    @order_ns.marshal_with(order_model, code=201)
    def post(self):
        """Create a new order"""
        data = request.json
        new_order = Order(
            user_id=data['user_id'],
            status=data.get('status', 'pending'),
            total=data['total']
        )
        db.session.add(new_order)
        db.session.commit()
        return new_order, 201
