from flask import Flask
from flask_restx import Api
from app.config import Config
from app.models.db import db
from app.auth import auth_ns
from app.routes.users import user_ns
from app.routes.products import product_ns
from app.routes.cart_items import cart_ns
from app.routes.categories import category_ns
from app.routes.order_items import order_item_ns
from app.routes.payment import payment_ns
from app.routes.orders import order_ns
from app.routes.reviews import review_ns



from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

authorizations = {
        'Bearer Auth': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        },
    }

jwt = JWTManager(app)

api = Api(app, title='Nishop API', version='1.2', description='Small api',
              authorizations=authorizations, security='Bearer Auth')

api.add_namespace(auth_ns, path = "/auth")
api.add_namespace(user_ns, path = "/users")
api.add_namespace(product_ns, path = "/products")
api.add_namespace(cart_ns, path = "/cart")
api.add_namespace(category_ns, path = "/categories")
api.add_namespace(order_item_ns, path = "/order-items")
api.add_namespace(order_ns, path = "/orders")
api.add_namespace(payment_ns, path = "/payment")
api.add_namespace(review_ns, path = "/reviews")

    

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
