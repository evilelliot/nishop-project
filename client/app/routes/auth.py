from flask import url_for
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import requests

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Llamada a la API para autenticar al usuario
        response = requests.post('http://localhost:5000/auth/login', json={
            'username': username,
            'password': password
        })

        print(f"API Response: {response.status_code}")  # Añade este print
        print(f"API Response content: {response.content}")  # Y este

        if response.status_code == 200:
            data = response.json()
            session['token'] = data['access_token']
            flash('Login successful!', 'success')
            print(f"Redirecting to: {url_for('user.profile')}")
            return redirect(url_for('user.profile'))
        else:
            flash(f'Login failed: {response.content}', 'danger')  # Modifica este flash
            return redirect(url_for('auth.login'))

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('token', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('auth.login'))
