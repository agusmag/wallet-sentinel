from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    
    #Check if the user credentials are store in the DB
    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    #Create the cookie for user in the browser
    login_user(user)

    return redirect(url_for('main.dashboard'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    #Fill the default amount
    totalAmount = 0

    #Verify that the user doesn't exist in the DB
    user = User.query.filter_by(email=email, username=username).first()

    if user:
        flash('Email adress or Username already exist.')
        return redirect(url_for('auth.signup'))

    #Create the object User to store it in the DB
    new_user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'), totalAmount=totalAmount)

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    #The logout_user method provided by flask_login remove the cookie from browser
    logout_user()

    return redirect(url_for('auth.login'))