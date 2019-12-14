from flask import Blueprint, render_template, Markup, redirect, url_for, flash, request
from flask_login import login_required, current_user
import datetime, calendar

# DB
from app import db

# Forms
from .forms import FiltersForm, NewOperationForm

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

@main.route('/home/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'GET':
        filterForm = FiltersForm(month_id=0, type_id=0)

    #Calculate current month
    month = datetime.date.today().month

    # Get User Data
    user = User.query.filter_by(username=current_user.username).first()

    #Set hidden user_id to NewOperationForm
    newOperationForm = NewOperationForm(user_id=user.id)
    newOperationForm.type_id.choices = [(o.id, o.description) for o in OperationType.query.order_by('description')]
    
    if request.method == 'POST':
        filterForm = FiltersForm()

        if filterForm.validate():
            currentYear = datetime.date.today().year
            formatDate = datetime.datetime(currentYear, filterForm.month, calendar.monthrange(currentYear, filterForm.month)[1])
            operations = Operation.query.filter(Operation.user_id == user.id, Operation.date <= formatDate)
        else:
            flash('Los valores de los filtros son incorrectos', category="alert-danger")
    else:
        # Calculate SpendAmount ( user.totalAmount - SUM(user.operations.amount))
        operations = Operation.query.filter_by(user_id=user.id)
    
    spendAmount = sum(operation.amount for operation in operations)

    # Load Months
    months = Month.query.order_by(Month.id).all()

    # Load Operation Types
    operationTypes = OperationType.query.order_by(OperationType.id).all()

    #Find Month Name
    findMonth = Month.query.filter_by(id=month).first()

    return render_template('dashboard.html', curDate=datetime.date.today(), month=findMonth.description, user_id=user.id, username=user.username, totalAmount=user.totalAmount, spendAmount=spendAmount, months=months, operationTypes=operationTypes, operations=operations, form=filterForm, form2=newOperationForm)

@main.route('/home/dashboard/new_operation', methods=['POST'])
@login_required
def new_operation():
    #Obtain data from template
    formOperation = NewOperationForm()
    formOperation.type_id.choices = [(o.id, o.description) for o in OperationType.query.order_by('description')]

    print(formOperation.type_id.choices)
    print(formOperation.type_id)

    if formOperation.validate():
        #Save operation in DB
        operation = Operation(description= formOperation.description, date=formOperation.date, amount=formOperation.amount, type_id=formOperation.type_id, user_id=formOperation.user_id)
        
        db.session.add(operation)
        db.session.commit()

        flash('La operación fue creada con éxito!', category="alert-success")
        return redirect(url_for('main.dashboard'))
    
    flash('Algún dato de la operación es incorrecto', category="alert-danger")
    return redirect(url_for('main.dashboard'))


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
