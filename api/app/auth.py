from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.db import db
from app.models.user import User

auth_ns = Namespace('auth', description='Authentication operations')


signup_model = auth_ns.model('Signup', {
    'email': fields.String(required=True, description='Correo electrónico'),
    'username': fields.String(required=True, description='Nombre de usuario'),
    'password': fields.String(required=True, description='Contraseña')
})

login_model = auth_ns.model('Login', {
    'username': fields.String(required=True, description='Nombre de usuario'),
    'password': fields.String(required=True, description='Contraseña')
})

@auth_ns.route('/signup')
class Signup(Resource):
    @auth_ns.expect(signup_model)
    @auth_ns.response(201, 'Usuario creado exitosamente')
    @auth_ns.response(400, 'Email o nombre de usuario ya existe')
    def post(self):
        """Crea un nuevo usuario"""
        data = request.json
        if User.query.filter_by(email=data['email']).first():
            auth_ns.abort(400, "Email ya existe")
        if User.query.filter_by(username=data['username']).first():
            auth_ns.abort(400, "Nombre de usuario ya existe")
        
        nuevo_usuario = User(username=data['username'], email=data['email'])
        nuevo_usuario.set_password(data['password'])
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        return {"msg": "Usuario creado exitosamente"}, 201

    
@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    @auth_ns.response(200, 'Login exitoso')
    @auth_ns.response(401, 'Credenciales inválidas')
    def post(self):
        """Autentica a un usuario"""
        data = request.json
        user = User.query.filter_by(username=data['username']).first()
        if user and user.check_password(data['password']):
            access_token = create_access_token(identity=user.username)
            return {"access_token": access_token}, 200
        auth_ns.abort(401, "Credenciales inválidas")