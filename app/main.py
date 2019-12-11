from flask import Blueprint, render_template, Markup
from flask_login import login_required, current_user
import datetime

# Models

from .models import User, Operation, OperationType, Month

main = Blueprint('main', __name__)

labels = [
    'JAN', 'FEB', 'MAR', 'APR',
    'MAY', 'JUN', 'JUL', 'AUG',
    'SEP', 'OCT', 'NOV', 'DEC'
]

values = [
    967.67, 1190.89, 1079.75, 1349.19,
    2328.91, 2504.28, 2873.83, 4764.87,
    4349.29, 6458.30, 9907, 16297
]

colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"
    ]


@main.route('/')
def home():
    return render_template('home.html')

@main.route('/home/dashboard')
@login_required
def dashboard():
    #Calculate current month
    month = datetime.date.today().month
    print(month)

    # Get User Data
    user = User.query.filter_by(username=current_user.username).first()

    # Calculate SpendAmount ( user.totalAmount - SUM(user.operations.amount))
    operations = Operation.query.filter_by(user_id=user.id)
    print(operations)
    spendAmount = sum(operation.amount for operation in operations)
    print(spendAmount)

    # Load Months
    months = Month.query.order_by(Month.id).all()
    print(months)

    # Load Operation Types
    operationTypes = OperationType.query.order_by(OperationType.id).all()
    print(operationTypes)

    #Find Month Name
    findMonth = Month.query.filter_by(id=month).first()
    print(findMonth.description)


    return render_template('dashboard.html', month=findMonth.description, username=user.username, totalAmount=user.totalAmount, spendAmount=spendAmount, months=months, operationTypes=operationTypes, operations=operations)

@main.route('/home/statistics')
@login_required
def statistics():
    # Get user.operations
    # Calculate Graphs

    line_labels = labels
    line_values = values

    return render_template('statistics.html', title='Bitcoin Monthly Price in USD', max=17000, labels=line_labels, values=line_values)

# @app.errorhandler(404)
# def page_not_found(error):
# 	return render_template("error.html",error="Página no encontrada...")
