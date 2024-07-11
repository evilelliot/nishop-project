from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.db import db
from app.models.product import Product
from datetime import datetime

product_ns = Namespace('products', description='Product operations')

product_model = product_ns.model('Product', {
    'id': fields.Integer(readonly=True),
    'name': fields.String(required=True),
    'description': fields.String(),
    'price': fields.String(required=True),
    'stock': fields.Integer(required=True),
    'category_id': fields.Integer(),
    'user_id': fields.Integer(),  
    'created_at': fields.DateTime(readonly=True, attribute='created_at', dt_format='iso8601'),
    'updated_at': fields.DateTime(readonly=True, attribute='updated_at', dt_format='iso8601')
})

product_input_model = product_ns.model('ProductInput', {
    'name': fields.String(required=True),
    'description': fields.String(),
    'price': fields.String(required=True),
    'stock': fields.Integer(required=True),
    'category_id': fields.Integer(),
    'user_id': fields.Integer() 
})

product_update_model = product_ns.model('ProductUpdate', {
    'name': fields.String(required=False),
    'description': fields.String(),
    'price': fields.String(required=False),
    'stock': fields.Integer(required=False),
    'category_id': fields.Integer(),
    'user_id': fields.Integer()  
})

# Read (List and Retrieve) - Protected
@product_ns.route('/')
class ProductList(Resource):
    @product_ns.marshal_list_with(product_model)
    def get(self):
        """List all products"""
        return Product.query.all()

@product_ns.route('/<int:id>')
class ProductResource(Resource):
    @product_ns.marshal_with(product_model)
    @product_ns.response(404, 'Product not found')
    def get(self, id):
        """Retrieve a product"""
        product = Product.query.get_or_404(id)
        return product

    # Update - Protected
    @jwt_required()
    @product_ns.expect(product_update_model)
    @product_ns.marshal_with(product_model)
    @product_ns.response(404, 'Product not found')
    def put(self, id):
        """Update a product"""
        product = Product.query.get_or_404(id)
        data = request.json
        
        if 'name' in data:
            product.name = data['name']
        if 'description' in data:
            product.description = data['description']
        if 'price' in data:
            product.price = data['price']
        if 'stock' in data:
            product.stock = data['stock']
        if 'category_id' in data:
            product.category_id = data['category_id']
        
        product.updated_at = datetime.now()
        db.session.commit()
        return product

    # Delete - Protected
    @jwt_required()
    @product_ns.response(204, 'Product deleted')
    @product_ns.response(404, 'Product not found')
    def delete(self, id):
        """Delete a product"""
        product = Product.query.get_or_404(id)
        db.session.delete(product)
        db.session.commit()
        return '', 204

# Create - Protected
@product_ns.route('/create')
class ProductCreate(Resource):
    @jwt_required()
    @product_ns.expect(product_input_model)
    @product_ns.marshal_with(product_model, code=201)
    def post(self):
        """Create a new product"""
        data = request.json
        new_product = Product(
            name=data['name'],
            description=data.get('description'),
            price=data['price'],
            stock=data['stock'],
            category_id=data.get('category_id')
        )
        db.session.add(new_product)
        db.session.commit()
        return new_product, 201
    
# Retrieve products by user_id - Protected
@product_ns.route('/user/<int:user_id>')
class ProductByUser(Resource):
    @jwt_required()
    @product_ns.marshal_list_with(product_model)
    def get(self, user_id):
        """Retrieve products by user_id"""
        products = Product.query.filter_by(user_id=user_id).all()
        if not products:
            return {'message': 'No products found for this user'}, 404
        return products