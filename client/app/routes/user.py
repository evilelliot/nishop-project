from flask import Blueprint, render_template, session, redirect, url_for, flash
import requests

user_bp = Blueprint('user', __name__)

@user_bp.route('/profile')
def profile():
    token = session.get('token')
    if not token:
        flash('You need to login first', 'warning')
        return redirect(url_for('auth.login'))

    # Llamada a la API para obtener el perfil del usuario autenticado
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get('http://localhost:5000/users/profile', headers=headers)

    if response.status_code == 200:
        user = response.json()
        return render_template('profile.html', user=user)
    else:
        print('Failed to load profile  ' + str(response.content))
        flash('Failed to load profile', 'danger')
        return redirect(url_for('auth.login'))
    

@user_bp.route('/products')
def products():
    token = session.get('token')
    if not token:
        flash('You need to login first', 'warning')
        return redirect(url_for('auth.login'))

    # Llamada a la API para obtener el perfil del usuario autenticado
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get('http://localhost:5000/users/profile', headers=headers)
    
    if response.status_code == 200:
        user = response.json()
        user_id = user["id"]
        get_products = requests.get(f'http://127.0.0.1:5000/products/user/{user_id}', headers=headers)
        products = get_products.json()
        products_count = len(products)
        print(products)
        return render_template('products.html', 
                               user = user, 
                               token = token, 
                               products_count = products_count,
                               products = products)
    else:
        print('Failed to load profile  ' + str(response.content))
        flash('Failed to load profile', 'danger')
        return redirect(url_for('auth.login'))