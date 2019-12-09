from flask import Flask, render_template, request, redirect, flash, url_for
from flaskext.mysql import MySQL

app = Flask(__name__)

#MySQL Connection

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'agustinmag'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_CHARSET'] = 'utf-8'

mysql = MySQL()
mysql.init_app(app)

#Initialize session
app.secret_key = 'mysecretkey'

@app.route('/login')
def Index():
    return render_template('login.html')

@app.route('/signup')
def Signup():
    return render_template('signup.html')

@app.route('/')
@app.route('/home')
def Home():
    return render_template('home.html')

@app.route('/home/dashboard')
def Dashboard():
    return render_template('dashboard.html')

@app.route('/home/statistics')
def Statistics():
    return render_template('statistics.html')

# @app.errorhandler(404)
# def page_not_found(error):
# 	return render_template("error.html",error="Página no encontrada...")

if __name__ == '__main__':
    app.run(port = 3000, debug = True)