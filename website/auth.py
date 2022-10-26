from  flask import Blueprint,redirect,url_for,render_template,request,flash,session
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import os


auth = Blueprint('auth', __name__,)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    session.pop('_flashes', None)
    if request.method == 'POST':
        email = request.form.get('Email')
        password = request.form.get('Password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.dashboard'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template('login.html')


@auth.route('/logout')
@login_required
def logout():
    tokenName = session['token']
    if os.path.exists(str(tokenName) + 'token.json'):
        os.remove(str(tokenName) + 'token.json')
    logout_user()
    return redirect(url_for('views.home'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    session.pop('_flashes', None)
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        email = request.form.get('Email')
        first_name = request.form.get('FirstName')
        last_name = request.form.get('LastName')
        password1 = request.form.get('Password1')
        password2 = request.form.get('Password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, last_name = last_name, profile_image='user.png', password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit() 
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.dashboard'))

        return render_template('signup.html')
