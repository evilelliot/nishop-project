from datetime import datetime
from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from app.models.db import db
from app.models.payments import Payment

payment_ns = Namespace('payments', description='Payment operations')

# Model
payment_model = payment_ns.model('Payment', {
    'id': fields.Integer(readonly=True),
    'order_id': fields.Integer(required=True),
    'amount': fields.String(required=True),
    'payment_method': fields.String(required=True),
    'status': fields.String(required=True),
    'created_at': fields.DateTime(readonly=True),
    'updated_at': fields.DateTime(readonly=True)
})

payment_input_model = payment_ns.model('PaymentInput', {
    'order_id': fields.Integer(required=True),
    'amount': fields.String(required=True),
    'payment_method': fields.String(required=True),
    'status': fields.String(required=False)
})

payment_update_model = payment_ns.model('PaymentUpdate', {
    'order_id': fields.Integer(),
    'amount': fields.String(),
    'payment_method': fields.String(),
    'status': fields.String()
})

# Read (List and Retrieve) - Protected
@payment_ns.route('/')
class PaymentList(Resource):
    @jwt_required()
    @payment_ns.marshal_list_with(payment_model)
    def get(self):
        """List all payments"""
        return Payment.query.all()

@payment_ns.route('/<int:id>')
class PaymentResource(Resource):
    @jwt_required()
    @payment_ns.marshal_with(payment_model)
    @payment_ns.response(404, 'Payment not found')
    def get(self, id):
        """Retrieve a payment"""
        payment = Payment.query.get_or_404(id)
        return payment

    # Update - Protected
    @jwt_required()
    @payment_ns.expect(payment_update_model)
    @payment_ns.marshal_with(payment_model)
    @payment_ns.response(404, 'Payment not found')
    def put(self, id):
        """Update a payment"""
        payment = Payment.query.get_or_404(id)
        data = request.json
        
        if 'order_id' in data:
            payment.order_id = data['order_id']
        if 'amount' in data:
            payment.amount = data['amount']
        if 'payment_method' in data:
            payment.payment_method = data['payment_method']
        if 'status' in data:
            payment.status = data['status']
        
        payment.updated_at = datetime.now()
        db.session.commit()
        return payment

    # Delete - Protected
    @jwt_required()
    @payment_ns.response(204, 'Payment deleted')
    @payment_ns.response(404, 'Payment not found')
    def delete(self, id):
        """Delete a payment"""
        payment = Payment.query.get_or_404(id)
        db.session.delete(payment)
        db.session.commit()
        return '', 204

# Create - Protected
@payment_ns.route('/create')
class PaymentCreate(Resource):
    @jwt_required()
    @payment_ns.expect(payment_input_model)
    @payment_ns.marshal_with(payment_model, code=201)
    def post(self):
        """Create a new payment"""
        data = request.json
        new_payment = Payment(
            order_id=data['order_id'],
            amount=data['amount'],
            payment_method=data['payment_method'],
            status=data.get('status', 'pending')
        )
        db.session.add(new_payment)
        db.session.commit()
        return new_payment, 201
