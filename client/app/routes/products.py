from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify
import requests

products_bp = Blueprint('products', __name__)

@products_bp.route('/<int:id>')
def product(id):
    token = session.get('token')
    if token is None:
        token = None 

    get_product = requests.get(f'http://localhost:5000/products/{id}')
    get_reviews = requests.get(f'http://localhost:5000/reviews/{id}')
    reviews = get_reviews.json()
    product = get_product.json()
    
    
    print(reviews)
    return render_template('product.html', data = product, r_count = len(reviews), reviews = reviews, token = token)
    

