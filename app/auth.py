from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required

# Forms 
from .forms import LoginForm, SignupForm
# Models

from .models import User, UserConfiguration

from app import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    loginForm = LoginForm()

    return render_template('login.html', form=loginForm)

@auth.route('/login', methods=['POST'])
def login_post():
    loginForm = LoginForm()

    if loginForm.validate():
        #Check if the user credentials are store in the DB
        user = User.query.filter_by(username=loginForm.username.data).first()

        if not user or not check_password_hash(user.password, loginForm.password.data):
            flash('Por favor verificá los datos de ingreso nuevamente.')
            return redirect(url_for('auth.login'))

        #Create the cookie for user in the browser
        login_user(user)

        return redirect(url_for('main.dashboard'))
    else:
        return render_template('login.html', form=loginForm)

@auth.route('/signup')
def signup():
    signupForm = SignupForm()

    return render_template('signup.html', form=signupForm)

@auth.route('/signup', methods=['POST'])
def signup_post():
    signupForm = SignupForm()

    if signupForm.validate():
        #Verify that the user doesn't exist in the DB
        user = User.query.filter_by(email=signupForm.email.data, username=signupForm.username.data).first()

        if user:
            flash('El email ya se encuentra registrado.')
            return redirect(url_for('auth.signup'))

        totalAmount = 0
        mainThemeEnabled = True

        #Create the object User to store it in the DB
        new_user = User(email=signupForm.email.data, username=signupForm.username.data, password=generate_password_hash(signupForm.password.data, method='sha256'), totalAmount=totalAmount)

        #Create the object UserConfiguration to store it in the BD
        new_user_config = UserConfiguration(available_amount=totalAmount, main_theme=mainThemeEnabled, user_id=new_user.id)
        
        #Save both records in the DB
        db.session.add(new_user)
        db.session.add(new_user_config)
        db.session.commit()

        return redirect(url_for('auth.login'))
    else:
        return render_template('signup.html', form=signupForm)

@auth.route('/logout')
@login_required
def logout():
    #The logout_user method provided by flask_login remove the cookie from browser
    logout_user()

    return redirect(url_for('auth.home'))