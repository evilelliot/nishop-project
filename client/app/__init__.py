from flask import Flask
from flask_bootstrap import Bootstrap
from flask_session import Session
from .routes.user import user_bp
from .routes.auth import auth_bp
from .routes.main import main_bp
from .routes.products import products_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    Bootstrap(app)
    Session(app)

    app.register_blueprint(main_bp, url_prefix = '/')
    app.register_blueprint(auth_bp, url_prefix = '/auth')
    app.register_blueprint(user_bp, url_prefix = '/user')
    app.register_blueprint(products_bp, url_prefix = '/products')
    return app
