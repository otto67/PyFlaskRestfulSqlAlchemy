from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from .models import User
from flask_login import login_user, logout_user, login_required

my_auth = Blueprint('my_auth', __name__)

@my_auth.route('/login', methods=['GET', 'POST'])
def login():
    print("Hello from login")
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()

        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('my_auth.login')) # if the user doesn't exist or password is wrong, reload the page

        # if the above check passes, then we know the user has the right credentials
        login_user(user, remember=remember)
        
        return redirect(url_for('my_app.userprofile'))


@my_auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

    user = User.query.filter_by(email=email).first() 
    if user:
        flash('Email address already exists')
        return redirect(url_for('my_auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'), admin=False)
    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
      
    return redirect(url_for('my_auth.login'))

@my_auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('my_app.index'))

