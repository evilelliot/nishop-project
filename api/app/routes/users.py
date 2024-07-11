from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.db import db
from app.models.user import User

user_ns = Namespace('users', description='User operations')

# Models
user_model = user_ns.model('User', {
    'id': fields.Integer(readonly=True),
    'username': fields.String(required=True),
    'email': fields.String(required=True),
    'role': fields.String(required=True),
    'avatar': fields.String(required=True),
    'created_at': fields.DateTime(readonly=True),
    'updated_at': fields.DateTime(readonly=True)
})

user_input_model = user_ns.model('UserInput', {
    'username': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True),
    'role': fields.String(required=False)
})

user_update_model = user_ns.model('UserUpdate', {
    'username': fields.String(required=False),
    'email': fields.String(required=False),
    'password': fields.String(required=False),
    'role': fields.String(required=False),
    'avatar': fields.String(required=False)
})

# Create (Signup) - Not protected
@user_ns.route('/signup')
class UserSignup(Resource):
    @user_ns.expect(user_input_model)
    @user_ns.marshal_with(user_model, code=201)
    @user_ns.response(400, 'Validation Error')
    def post(self):
        """Create a new user"""
        data = request.json
        if User.query.filter_by(email=data['email']).first():
            user_ns.abort(400, "Email already exists")
        if User.query.filter_by(username=data['username']).first():
            user_ns.abort(400, "Username already exists")
        
        new_user = User(
            username=data['username'],
            email=data['email'],
            role=data.get('role', 'user')
        )
        new_user.set_password(data['password'])
        db.session.add(new_user)
        db.session.commit()
        
        return new_user, 201

# Read (List and Retrieve) - Protected
@user_ns.route('/')
class UserList(Resource):
    @jwt_required()
    @user_ns.marshal_list_with(user_model)
    def get(self):
        """List all users"""
        return User.query.all()

@user_ns.route('/<int:id>')
class UserResource(Resource):
    @jwt_required()
    @user_ns.marshal_with(user_model)
    @user_ns.response(404, 'User not found')
    def get(self, id):
        """Retrieve a user"""
        user = User.query.get_or_404(id)
        return user

    # Update - Protected
    @jwt_required()
    @user_ns.expect(user_update_model)
    @user_ns.marshal_with(user_model)
    @user_ns.response(404, 'User not found')
    def put(self, id):
        """Update a user"""
        user = User.query.get_or_404(id)
        data = request.json
        
        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email']
        if 'password' in data:
            user.set_password(data['password'])
        if 'role' in data:
            user.role = data['role']
        if 'avatar' in data:
            user.avatar = data['avatar']
        
        db.session.commit()
        return user

    # Delete - Protected
    @jwt_required()
    @user_ns.response(204, 'User deleted')
    @user_ns.response(404, 'User not found')
    def delete(self, id):
        """Delete a user"""
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return '', 204

# User Profile - Protected
@user_ns.route('/profile')
class UserProfile(Resource):
    @jwt_required()
    @user_ns.marshal_with(user_model)
    def get(self):
        """Get current user's profile"""
        current_user = get_jwt_identity()
        user = User.query.filter_by(username=current_user).first()
        return user