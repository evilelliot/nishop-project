from flask import Blueprint, render_template, session, redirect, url_for, flash
import requests

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    token = session.get('token')
    if not token:
        token = None

    
        flash('You need to login first', 'warning')
        return redirect(url_for('auth.login'))

    # Llamada a la API para obtener el perfil del usuario autenticado
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get('http://localhost:5000/users/profile', headers=headers)
    get_categories = requests.get('http://127.0.0.1:5000/categories/')
    get_products = requests.get('http://127.0.0.1:5000/products/')
    products = get_products.json()  
    categories = get_categories.json()   
    user = response.json()
     
    
    return render_template('main.html', products=products, categories=categories, user = user)
