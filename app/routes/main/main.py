from flask import Blueprint, render_template, request, session, redirect, url_for
from app.models import User
from app import db


main_bp = Blueprint(
    'main', __name__, template_folder='templates', static_folder='static')


@main_bp.route('/')
def index():

    if session.get('user_id'):
        return redirect(url_for('main.home'))
    
    return render_template('index.html')


@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        if not username or not password or not email or not role:
            error_message = 'Por favor, preencha todos os campos!'
            return render_template('register.html', error=error_message)

        user = User.query.filter_by(username=username).first()
        if user:
            error_message = 'Usuário já cadastrado!'
            return render_template('register.html', error=error_message)

        user = User.query.filter_by(email=email).first()
        if user:
            error_message = 'Email já cadastrado!'
            return render_template('register.html', error=error_message)

        new_user = User(username=username, email=email, role=role)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('main.login'))
    
    if session.get('user_id'):
        return redirect(url_for('main.home'))

    return render_template('register.html')


@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            return redirect(url_for('main.home'))
        else:
            return render_template('login.html', error='Usuário ou senha inválidos!')

    if session.get('user_id'):
        return redirect(url_for('main.home'))

    return render_template('login.html')


@main_bp.route('/dashboard')
def home():
    user_id = session.get('user_id')
    user = User.query.get(user_id)

    if user:
        return render_template('main.html', user=user)
    else:
        return redirect(url_for('main.login'))


@main_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return redirect(url_for('main.login'))
