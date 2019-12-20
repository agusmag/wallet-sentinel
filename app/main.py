from flask import Blueprint, render_template, Markup, redirect, url_for, flash, request, session
from flask_login import login_required, current_user
import datetime, calendar, json, locale

# DB
from app import db

# Forms
from .forms import FiltersForm, NewOperationForm, UserSettingsForm

# Models
from .models import User, UserConfiguration, Operation, OperationType, Month

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
        filter_month_id = 0
        filter_type_id = 0

        # Check for cookies values from preview dashboard filter POST
        if request.args.get('messages') is not None:
            messages = request.args['messages']
            messages=json.loads(messages)

            if messages.get('month_id') is not None:
                filter_month_id = messages.get('month_id')
            
            if messages.get('type_id') is not None:
                filter_type_id = messages.get('type_id')

        filterForm = FiltersForm(month_id=filter_month_id, type_id=filter_type_id)

        # Calculate current month
        month = datetime.date.today().month

        # Get User Data
        user = User.query.filter_by(username=current_user.username).first()

        # Get User Configuration
        userConfig = UserConfiguration.query.filter_by(user_id=user.id).first()

        # Set User Settings to UserSettingsForm
        userSettingsForm = UserSettingsForm(available_amount="$ {0}".format(userConfig.available_amount), main_theme=userConfig.main_theme, user_id=userConfig.user_id)
        
        # Set hidden user_id to all the Forms in the Dashboard View
        newOperationForm = NewOperationForm(user_id=user.id)
        editOperationForm = NewOperationForm(user_id=user.id)

        # Set DataTypes to all the Selects of EveryForm in Dashboard View
        filterForm.month_id.choices = [(m.id, m.description) for m in Month.query.order_by('id')]
        filterForm.month_id.choices.insert(0, ('0', 'Todos'))
        
        filterForm.type_id.choices = [(o.id, o.description) for o in OperationType.query.order_by('description')]
        filterForm.type_id.choices.insert(0, ('0', 'Todos'))

        newOperationForm.type_id.choices = [(o.id, o.description) for o in OperationType.query.order_by('description')]
        editOperationForm.type_id.choices = [(o.id, o.description) for o in OperationType.query.order_by('description')]

        # Calculate SpendAmount ( user.totalAmount - SUM(user.operations.amount))
        operations = None
        if filter_month_id != 0 and filter_type_id != 0:
            currentYear = datetime.date.today().year
            formatDate = datetime.datetime(currentYear, filter_month_id, calendar.monthrange(currentYear, filter_month_id)[1])
            operations = Operation.query.filter(Operation.user_id == user.id, Operation.date <= formatDate, Operation.type_id == filter_type_id)
        elif filter_month_id != 0 and filter_type_id == 0:
            currentYear = datetime.date.today().year
            formatDate = datetime.datetime(currentYear, filter_month_id, calendar.monthrange(currentYear, filter_month_id)[1])
            operations = Operation.query.filter(Operation.user_id == user.id, Operation.date <= formatDate)
        elif filter_month_id == 0 and filter_type_id != 0:
            operations = Operation.query.filter(Operation.user_id == user.id, Operation.type_id == filter_type_id)
        else:
            operations = Operation.query.filter_by(user_id=user.id)

        spendAmount = sum(operation.amount for operation in operations)

        # Load Operation Types
        operationTypes = OperationType.query.order_by(OperationType.id).all()

        # Find Month Name CHANGE TO DATETIME INSTED OF QUERY TO DB
        findMonth = Month.query.filter_by(id=month).first()

        # Format All the Amounts to Currency
        locale.setlocale( locale.LC_ALL, '' )
        formattedAvailableAmount = locale.currency( userConfig.available_amount, grouping=True )
        formattedSpendAmount = locale.currency( spendAmount, grouping=True )

        # Calculate Spend Amount Badge Status Color
        spendAmountStatusColor = 'badge-success'
        if spendAmount >= (userConfig.available_amount * 0.25) and spendAmount < userConfig.available_amount:
            spendAmountStatusColor = 'badge-warning'
        elif spendAmount >= userConfig.available_amount:
            spendAmountStatusColor = 'badge-danger'

        return render_template('dashboard.html', curDate=datetime.date.today(), month=findMonth.description, user_id=user.id, username=user.username, totalAmount= formattedAvailableAmount, spendAmount=formattedSpendAmount, spendAmountStatusColor=spendAmountStatusColor, operationTypes=operationTypes, operations=operations, form=filterForm, form2=newOperationForm, form3=editOperationForm, form4=userSettingsForm)

    elif request.method == 'POST':
        filterForm = FiltersForm()

        # Set DataTypes to all the Selects of EveryForm in Dashboard View
        filterForm.month_id.choices = [(m.id, m.description) for m in Month.query.order_by('id')]
        filterForm.month_id.choices.insert(0, ('0', 'Todos'))
        
        filterForm.type_id.choices = [(o.id, o.description) for o in OperationType.query.order_by('description')]
        filterForm.type_id.choices.insert(0, ('0', 'Todos'))

        userSettingsForm = UserSettingsForm()

        if filterForm.type_id.data != 0 and filterForm.month_id.data != 0:
            if not filterForm.is_submitted() or not filterForm.validate():
                flash('Los valores de los filtros son incorrectos', category="alert-danger")

        if userSettingsForm.is_submitted() and userSettingsForm.validate():
            # Get User Configuration
            userConfig = UserConfiguration.query.filter_by(user_id=userSettingsForm.user_id.data).first()

            # Update the fields with the current values
            userConfig.available_amount = float(userSettingsForm.available_amount.data.replace("$","").replace(",",""))
            userConfig.main_theme = userSettingsForm.main_theme.data

            db.session.commit()
            
            flash('La configuración fue actualizada con éxito', category='alert-success')
        
        messages = json.dumps({'month_id': filterForm.month_id.data, 'type_id': filterForm.type_id.data})

        print(session.get('messages'))
        
        return redirect(url_for('main.dashboard', messages=messages))

@main.route('/home/dashboard/new_operation', methods=['POST'])
@login_required
def new_operation():
    # Obtain data from template
    formOperation = NewOperationForm()
    formOperation.type_id.choices = [(o.id, o.description) for o in OperationType.query.order_by('description')]

    if formOperation.validate():
        # Parse amount string to decimal
        convertedAmount = float(formOperation.amount.data.replace("$","").replace(",",""))

        # Save operation in DB
        operation = Operation(description= formOperation.description.data, date=formOperation.date.data, amount=convertedAmount, type_id=formOperation.type_id.data, user_id=formOperation.user_id.data)
        
        db.session.add(operation)
        db.session.commit()

        flash('La operación fue creada con éxito!', category="alert-success")
        return redirect(url_for('main.dashboard'))
    
    flash('Hubo un problema al crear la operación', category="alert-danger")
    return redirect(url_for('main.dashboard', form2=formOperation, showNewModal=True))


@main.route('/home/dashboard/update_operation/<string:id>', methods=['POST'])
@login_required
def update_operation(id):
    editOperationForm = NewOperationForm()
    editOperationForm.type_id.choices = [(o.id, o.description) for o in OperationType.query.order_by('description')]

    if editOperationForm.validate():
        # Search the edited operation from DB to update it
        edit_operation = Operation.query.filter_by(id=id).first()

        # Update the fields
        edit_operation.description = editOperationForm.description.data
        edit_operation.date = editOperationForm.date.data
        edit_operation.amount = float(editOperationForm.amount.data.replace("$","").replace(",",""))
        edit_operation.type_id = editOperationForm.type_id.data

        db.session.commit()

        flash('La operación fue actualizada con éxito', category='alert-success')
        return redirect(url_for('main.dashboard'))

    flash('Hubo un problema al actualizar la operación', category='alert-danger')
    return redirect(url_for('main.dashboard'))

@main.route('/home/dashboard/delete_operation/<string:id>', methods=['POST'])
@login_required
def delete_operation(id):
    # Detele operation from DB
    Operation.query.filter_by(id=id).delete()

    db.session.commit()

    flash('La operación fue eliminada con éxito', category='alert-success')
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
