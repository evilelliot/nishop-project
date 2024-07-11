from datetime import datetime
from flask import abort, request, jsonify
from flask_restx import Namespace, Resource, fields, api
from flask_jwt_extended import jwt_required
from app.models.db import db
from app.models.reviews import Review

review_ns = Namespace('reviews', description='Review operations')

# Model
review_model = review_ns.model('Review', {
    'id': fields.Integer(readonly=True),
    'product_id': fields.Integer(required=True),
    'user_id': fields.Integer(required=True),
    'rating': fields.Integer(required=True),
    'comment': fields.String(),
    'created_at': fields.DateTime(readonly=True),
    'updated_at': fields.DateTime(readonly=True)
})

review_input_model = review_ns.model('ReviewInput', {
    'product_id': fields.Integer(required=True),
    'user_id': fields.Integer(required=True),
    'rating': fields.Integer(required=True),
    'comment': fields.String()
})

review_update_model = review_ns.model('ReviewUpdate', {
    'product_id': fields.Integer(),
    'user_id': fields.Integer(),
    'rating': fields.Integer(),
    'comment': fields.String()
})

# Read (List and Retrieve) - Protected
@review_ns.route('/')
class ReviewList(Resource):
    @review_ns.marshal_list_with(review_model)
    def get(self):
        """List all reviews"""
        return Review.query.all()

@review_ns.route('/<int:id>')
class ReviewResource(Resource):
    @review_ns.marshal_with(review_model)
    def get(self, id):
        """Retrieve a review by product id"""
        review = Review.query.filter_by(product_id=id).all()
        if not review:
            return jsonify({"message": "Review not found for product id {}".format(id)}), 404
        return review

    # Update - Protected
    @jwt_required()
    @review_ns.expect(review_update_model)
    @review_ns.marshal_with(review_model)
    def put(self, id):
        """Update a review by product id"""
        review = Review.query.filter_by(product_id=id).first()
        if not review:
            return jsonify({"message": "Review not found for product id {}".format(id)}), 404

        data = request.json
        review.product_id = id  # Actualiza la ID del producto si se proporciona

        if 'user_id' in data:
            review.user_id = data['user_id']
        if 'rating' in data:
            review.rating = data['rating']
        if 'comment' in data:
            review.comment = data['comment']
        
        review.updated_at = datetime.now()
        db.session.commit()
        return review

    # Delete - Protected
    @jwt_required()
    @review_ns.response(204, 'Review deleted')
    def delete(self, id):
        """Delete a review by product id"""
        review = Review.query.filter_by(product_id=id).first()
        if not review:
            return jsonify({"message": "Review not found for product id {}".format(id)}), 404
        
        db.session.delete(review)
        db.session.commit()
        return '', 204
        
# Create - Protected
@review_ns.route('/create')
class ReviewCreate(Resource):
    @jwt_required()
    @review_ns.expect(review_input_model)
    @review_ns.marshal_with(review_model, code=201)
    def post(self):
        """Create a new review"""
        data = request.json
        new_review = Review(
            product_id=data['product_id'],
            user_id=data['user_id'],
            rating=data['rating'],
            comment=data.get('comment', None)
        )
        db.session.add(new_review)
        db.session.commit()
        return new_review, 201
