from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from app.models.db import db
from app.models.categories import Category
from datetime import datetime

category_ns = Namespace('categories', description='Category operations')

# Model
category_model = category_ns.model('Category', {
    'id': fields.Integer(readonly=True),
    'name': fields.String(required=True),
    'description': fields.String(),
    'created_at': fields.DateTime(readonly=True),
    'updated_at': fields.DateTime(readonly=True)
})

category_input_model = category_ns.model('CategoryInput', {
    'name': fields.String(required=True),
    'description': fields.String()
})

category_update_model = category_ns.model('CategoryUpdate', {
    'name': fields.String(),
    'description': fields.String()
})

# Read (List and Retrieve) - Protected
@category_ns.route('/')
class CategoryList(Resource):
    @category_ns.marshal_list_with(category_model)
    def get(self):
        """List all categories"""
        return Category.query.all()

@category_ns.route('/<int:id>')
class CategoryResource(Resource):
    @jwt_required()
    @category_ns.marshal_with(category_model)
    @category_ns.response(404, 'Category not found')
    def get(self, id):
        """Retrieve a category"""
        category = Category.query.get_or_404(id)
        return category

    # Update - Protected
    @jwt_required()
    @category_ns.expect(category_update_model)
    @category_ns.marshal_with(category_model)
    @category_ns.response(404, 'Category not found')
    def put(self, id):
        """Update a category"""
        category = Category.query.get_or_404(id)
        data = request.json
        
        if 'name' in data:
            category.name = data['name']
        if 'description' in data:
            category.description = data['description']
        
        category.updated_at = datetime.now()
        db.session.commit()
        return category

    # Delete - Protected
    @jwt_required()
    @category_ns.response(204, 'Category deleted')
    @category_ns.response(404, 'Category not found')
    def delete(self, id):
        """Delete a category"""
        category = Category.query.get_or_404(id)
        db.session.delete(category)
        db.session.commit()
        return '', 204

# Create - Protected
@category_ns.route('/create')
class CategoryCreate(Resource):
    @jwt_required()
    @category_ns.expect(category_input_model)
    @category_ns.marshal_with(category_model, code=201)
    def post(self):
        """Create a new category"""
        data = request.json
        new_category = Category(
            name=data['name'],
            description=data.get('description', None)
        )
        db.session.add(new_category)
        db.session.commit()
        return new_category, 201
