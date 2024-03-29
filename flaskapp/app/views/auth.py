from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from sqlalchemy import or_

# Forms 
from app.forms import LoginForm, SignupForm

# Models
from app.models import User, UserConfiguration, Saving

# Database
# Slack Bot
from app.extensions import db, sendNewUserSlackMessage

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
        user = User.query.filter(or_(User.username == loginForm.username.data, User.email == loginForm.username.data)).first()

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
        user = User.query.filter_by(email=signupForm.email.data).first()

        if user:
            flash('El email ya se encuentra registrado.')
            return redirect(url_for('auth.signup'))

        user = User.query.filter_by(username=signupForm.username.data).first()

        if user:
            flash('El usuario ya se encuentra registrado.')
            return redirect(url_for('auth.signup'))

        totalAmount = 0

        #Create the object User to store it in the DB
        new_user = User(email=signupForm.email.data, username=signupForm.username.data, password=generate_password_hash(signupForm.password.data, method='sha256'))

        #Save three objects in the DB
        db.session.add(new_user)
        db.session.commit()

        #Create the object UserConfiguration to store it in the BD
        new_user_config = UserConfiguration(spend_limit=totalAmount, warning_percent=75, hide_amounts=0, user_id=new_user.id, exchange_rates='{"ars": 1, "usd": 1, "eur": 1, "gbp": 1}')

        db.session.add(new_user_config)
        db.session.commit()

        #Create the object Saving to store it in the DB, by default is ARS (Pesos) with amount 0
        new_user_default_saving = Saving(user_id=new_user.id, currency_id=1, amount=0)

        db.session.add(new_user_default_saving)
        db.session.commit()

        #Send Slack Message notifying the new registration
        try:
            wsChannel = 'CSWSV4LLF' #walletsentinel channel
            sendNewUserSlackMessage(wsChannel, signupForm.username.data)
        except:
            print('Ha ocurrido un error al enviar la notifiación a slack..')

        return redirect(url_for('auth.login'))
    else:
        return render_template('signup.html', form=signupForm)

@auth.route('/logout')
@login_required
def logout():
    #The logout_user method provided by flask_login remove the cookie from browser
    logout_user()

    return redirect(url_for('main.home'))
