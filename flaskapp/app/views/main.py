from flask import Blueprint, render_template, Markup, redirect, url_for, flash, request, session
from flask_login import login_required, current_user
from sqlalchemy import extract
import datetime, pytz, calendar, json, locale

# Forms
from app.forms import FiltersForm, NewOperationForm, UserSettingsForm

# Models
from app.models import User, UserConfiguration, Operation, OperationType, Month

# Database
from app.extensions import db

main = Blueprint('main', __name__)

operationTypeIcons = [
    "fas fa-tshirt", "fas fa-hamburger", "fas fa-file-invoice-dollar", "fas fa-gift",
    "fas fa-laptop", "fas fa-couch", "fas fa-gas-pump", "fas fa-money-check-alt", "fas fa-eye",
    "fas fa-bath", "fas fa-bus", "fas fa-suitcase-rolling", "fas fa-gamepad", "fas fa-list-ul", "fas fa-money-bill-wave", "fab fa-untappd"
]

operationTypeIconsColor = [
    "tshirt", "hamburger", "file-invoice-dollar", "gift", "laptop",
    "couch", "gas-pump", "money-check", "eye", "bath", "bus", "suitcase-rolling", "gamepad", "list-ul", "money-bill-wave", "untappd"
]

@main.route('/')
@main.route('/home')
def home():
    if ( current_user.is_authenticated ):
        return redirect(url_for('main.dashboard'))
    else:
        return render_template('home.html')

@main.route('/home/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    timezone = pytz.timezone("America/Buenos_Aires")
    today = datetime.datetime.today()
    today_localize = timezone.localize(today)

    if request.method == 'GET':
        # Fill Filter Fields with current date and None for Operation_Type
        month = today_localize.month
        year = today_localize.year
        filter_month_id = month
        filter_year_id = 0
        filter_type_id = 0
        
        # Check for cookies values from preview dashboard filter POST
        if request.args.get('messages') is not None:
            messages = request.args['messages']
            messages=json.loads(messages)

            if messages.get('month_id') is not None:
                filter_month_id = messages.get('month_id')

            if messages.get('year_id') is not None:
                filter_year_id = messages.get('year_id')
            
            if messages.get('type_id') is not None:
                filter_type_id = messages.get('type_id')

        filterForm = FiltersForm(month_id=filter_month_id, year_id=filter_year_id, type_id=filter_type_id)
        
        # Get User Data
        user = User.query.filter_by(username=current_user.username).first()

        # Get User Configuration
        userConfig = UserConfiguration.query.filter_by(user_id=user.id).first()

        # Set User Settings to UserSettingsForm
        userSettingsForm = UserSettingsForm(spend_limit=userConfig.spend_limit, warning_percent=userConfig.warning_percent, hide_amounts=userConfig.hide_amounts, user_id=userConfig.user_id)

        # Set hidden user_id to all the Forms in the Dashboard View
        newOperationForm = NewOperationForm(user_id=user.id)
        editOperationForm = NewOperationForm(user_id=user.id)

        # Set DataTypes to all the Selects of EveryForm in Dashboard View
        filterForm.month_id.choices = [(m.id, m.description) for m in Month.query.order_by('id')]
        filterForm.month_id.choices.insert(0, ('0', 'Todos'))

        yearList = list(range(year, year - 21, -1))
        filterForm.year_id.choices = [(index, description) for index, description in enumerate(yearList, start=0)]
        
        filterForm.type_id.choices = [(o.id, o.description) for o in OperationType.query.order_by('description')]
        filterForm.type_id.choices.insert(0, ('0', 'Todos'))

        newOperationForm.type_id.choices = [(o.id, o.description) for o in OperationType.query.order_by('description')]
        editOperationForm.type_id.choices = [(o.id, o.description) for o in OperationType.query.order_by('description')]

        # Get Operation (Gained and Spend) by filter
        operations = None
        yearFilter = year - filter_year_id
        if filter_month_id != 0 and filter_type_id != 0:
            formatDateStart = datetime.datetime(yearFilter, filter_month_id, 1)
            formatDateEnd = datetime.datetime(yearFilter, filter_month_id, calendar.monthrange(yearFilter, filter_month_id)[1])
            operations = Operation.query.filter(Operation.user_id == user.id, Operation.date <= formatDateEnd, Operation.date >= formatDateStart, Operation.type_id == filter_type_id)
        elif filter_month_id != 0 and filter_type_id == 0:
            formatDateStart = datetime.datetime(yearFilter, filter_month_id, 1)
            formatDateEnd = datetime.datetime(yearFilter, filter_month_id, calendar.monthrange(yearFilter, filter_month_id)[1])
            operations = Operation.query.filter(Operation.user_id == user.id, Operation.date <= formatDateEnd, Operation.date >= formatDateStart)
        elif filter_month_id == 0 and filter_type_id != 0:
            operations = Operation.query.filter(Operation.user_id == user.id, Operation.type_id == filter_type_id, extract('year', Operation.date) == yearFilter)
        else:
            operations = Operation.query.filter(Operation.user_id == user.id, extract('year', Operation.date) == yearFilter)

        # Calculate gainedAmount ( SUM(user.operations.amount type == Ganancia ))
        gainedAmount = sum(operation.amount for operation in operations if operation.type_id == 15)
        
        # Calculate SpendAmount ( gainedAmount - SUM(user.operations.amount type != Ganancia ))
        spendAmount = sum(operation.amount for operation in operations if operation.type_id != 15)
            
        # Load Operation Types
        operationTypes = OperationType.query.order_by(OperationType.id).all()

        # Calculate Operation Type Statistics
        # Get total amounts of all User's operation types loaded
        userOperationTypesAmounts = [ (op.id, round(sum(operation.amount for operation in operations if operation.type_id == op.id ), 2)) for op in operationTypes if op.id != 15 ]

        #Calculate 
        operationStatistics = [ (operationTypes[uop[0]-1], uop[1], round((uop[1] * 100) / spendAmount if spendAmount > 0 else 0 , 2)) for uop in userOperationTypesAmounts ]

        # Format All the Amounts to Currency
        formattedTotalAmount = "$ {:,.2f}".format(gainedAmount)
        formattedSpendAmount = "$ {:,.2f}".format(spendAmount)
        formattedAvailableAmount = "$ {:,.2f}".format(gainedAmount - spendAmount)

        # Calculate Spend Amount Badge Status Color
        spendAmountStatusColor = 'badge-success'
        if userConfig.warning_percent is None:
            userConfig.warning_percent = 25

        if spendAmount >= (gainedAmount * ( userConfig.warning_percent / 100)) and spendAmount < gainedAmount:
            spendAmountStatusColor = 'badge-warning'
        elif spendAmount >= gainedAmount:
            spendAmountStatusColor = 'badge-danger'

        return render_template('dashboard.html',
                                    curDate=datetime.date.today(),
                                    user_id=user.id,
                                    username=user.username,
                                    totalAmount=formattedTotalAmount,
                                    spendAmount=formattedSpendAmount,
                                    spendAmountStatusColor=spendAmountStatusColor,
                                    availableAmount=formattedAvailableAmount,
                                    operationStatistics=operationStatistics,
                                    hideAmounts=userConfig.hide_amounts,
                                    operationTypes=operationTypes,
                                    operationTypeIcons=operationTypeIcons,
                                    operationTypeIconsColor=operationTypeIconsColor,
                                    operations=operations,
                                    form=filterForm,
                                    form2=newOperationForm,
                                    form3=editOperationForm,
                                    form4=userSettingsForm)

    elif request.method == 'POST':
        filterForm = FiltersForm()

        # Set DataTypes to all the Selects of EveryForm in Dashboard View
        filterForm.month_id.choices = [(m.id, m.description) for m in Month.query.order_by('id')]
        filterForm.month_id.choices.insert(0, ('0', 'Todos'))

        year = today_localize.year
        yearList = list(range(year, year - 21, -1))
        filterForm.year_id.choices = [(index, description) for index, description in enumerate(yearList, start=0)]
        
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
            userConfig.spend_limit = float(userSettingsForm.spend_limit.data.replace("$", "").replace(",", ""))
            userConfig.warning_percent = int(userSettingsForm.warning_percent.data)
            userConfig.hide_amounts = userSettingsForm.hide_amounts.data

            db.session.commit()
            
            flash('La configuración fue actualizada con éxito', category='alert-success')
        
        messages = json.dumps({'month_id': filterForm.month_id.data,'year_id': filterForm.year_id.data, 'type_id': filterForm.type_id.data})
        
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
        if convertedAmount <= 0:
            flash('El gasto de la operación debe ser mayor a 0.', category="alert-danger")
            return redirect(url_for('main.dashboard'))
            
        # Search User Configuration to verify Spend Limit
        userConfig = UserConfiguration.query.filter_by(user_id=formOperation.user_id.data).first()

        if userConfig.spend_limit != 0 and convertedAmount > userConfig.spend_limit and formOperation.type_id.data != 15:
                flash('El gasto supera el límite establecido en la configuración.', category="alert-danger")
                return redirect(url_for('main.dashboard'))
        else:
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
        # Parse amount string to decimal
        convertedAmount = float(editOperationForm.amount.data.replace("$","").replace(",",""))

        # Search User Configuration to verify Spend Limit
        userConfig = UserConfiguration.query.filter_by(user_id=editOperationForm.user_id.data).first()

        if userConfig.spend_limit != 0 and convertedAmount > userConfig.spend_limit:
                flash('El gasto supera el límite establecido en la configuración.', category="alert-danger")
                return redirect(url_for('main.dashboard'))
        else:
            # Search the edited operation from DB to update it
            edit_operation = Operation.query.filter_by(id=id).first()

            # Update the fields
            edit_operation.description = editOperationForm.description.data
            edit_operation.date = editOperationForm.date.data
            edit_operation.amount = convertedAmount
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

# @app.errorhandler(404)
# def page_not_found(error):
# 	return render_template("error.html",error="Página no encontrada...")
