from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.db import db
from app.models.cart_items import CartItem
from datetime import datetime

cart_ns = Namespace('cart_items', description='Cart Item operations')

# Model
cart_item_model = cart_ns.model('CartItem', {
    'id': fields.Integer(readonly=True),
    'user_id': fields.Integer(required=True),
    'product_id': fields.Integer(required=True),
    'quantity': fields.Integer(required=True),
    'created_at': fields.DateTime(readonly=True),
    'updated_at': fields.DateTime(readonly=True)
})

cart_item_input_model = cart_ns.model('CartItemInput', {
    'user_id': fields.Integer(required=True),
    'product_id': fields.Integer(required=True),
    'quantity': fields.Integer(required=True)
})

cart_item_update_model = cart_ns.model('CartItemUpdate', {
    'user_id': fields.Integer(),
    'product_id': fields.Integer(),
    'quantity': fields.Integer()
})

# Read (List and Retrieve) - Protected
@cart_ns.route('/')
class CartItemList(Resource):
    @jwt_required()
    @cart_ns.marshal_list_with(cart_item_model)
    def get(self):
        """List all cart items"""
        return CartItem.query.all()

@cart_ns.route('/<int:id>')
class CartItemResource(Resource):
    @jwt_required()
    @cart_ns.marshal_with(cart_item_model)
    @cart_ns.response(404, 'Cart Item not found')
    def get(self, id):
        """Retrieve a cart item"""
        cart_item = CartItem.query.get_or_404(id)
        return cart_item

    # Update - Protected
    @jwt_required()
    @cart_ns.expect(cart_item_update_model)
    @cart_ns.marshal_with(cart_item_model)
    @cart_ns.response(404, 'Cart Item not found')
    def put(self, id):
        """Update a cart item"""
        cart_item = CartItem.query.get_or_404(id)
        data = request.json
        
        if 'user_id' in data:
            cart_item.user_id = data['user_id']
        if 'product_id' in data:
            cart_item.product_id = data['product_id']
        if 'quantity' in data:
            cart_item.quantity = data['quantity']
        
        cart_item.updated_at = datetime.now()
        db.session.commit()
        return cart_item

    # Delete - Protected
    @jwt_required()
    @cart_ns.response(204, 'Cart Item deleted')
    @cart_ns.response(404, 'Cart Item not found')
    def delete(self, id):
        """Delete a cart item"""
        cart_item = CartItem.query.get_or_404(id)
        db.session.delete(cart_item)
        db.session.commit()
        return '', 204

# Create - Protected
@cart_ns.route('/create')
class CartItemCreate(Resource):
    @jwt_required()
    @cart_ns.expect(cart_item_input_model)
    @cart_ns.marshal_with(cart_item_model, code=201)
    def post(self):
        """Create a new cart item"""
        data = request.json
        new_cart_item = CartItem(
            user_id=data['user_id'],
            product_id=data['product_id'],
            quantity=data['quantity']
        )
        db.session.add(new_cart_item)
        db.session.commit()
        return new_cart_item, 201
