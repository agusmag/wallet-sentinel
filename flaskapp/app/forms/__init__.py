from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, DecimalField, SelectField, HiddenField
from wtforms.fields.html5 import DateField
from wtforms.validators import  Length, InputRequired, Email, DataRequired, EqualTo, Optional

import datetime

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[
        Length(min=4, max=25, message='La longitud debe ser entre %(min)d y %(max)d'),
        InputRequired('Este campo es obligatorio')
    ])
    email = StringField('Email', validators=[
        Length(min=6, max=35, message='La longitud debe ser entre %(min)d y %(max)d'),
        Email(message='El formato debe ser de correo'),
        InputRequired('Este campo es obligatorio')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, max=100, message='La longitud debe ser entre %(min)d y %(max)d'),
        EqualTo('confirm', message='La password debe coincidir')
    ])
    confirm = PasswordField('Repita la password', validators=[
        InputRequired('Este campo es obligatorio')
    ])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        InputRequired(message='Este campo es obligatorio'),
        Length(min=4, max=25, message='La longitud debe ser entre %(min)d y %(max)d')
    ])
    password = PasswordField('Password', validators=[
        InputRequired(message='Este campo es obligatorio'),
        Length(min=8, max=100, message='La longitud debe ser entre %(min)d y %(max)d')
    ])

class UserSettingsForm(FlaskForm):
    spend_limit = StringField('Límite por Compra', validators=[ Optional()], render_kw={'pattern':'^\d{1,3}(\d{3})*(\.\d+)?$', 'placeholder': '$ 0,00'})
    warning_percent = StringField('Porcentaje de advertencia', validators=[ Optional()])
    hide_amounts = BooleanField('Difuminar Totales', validators=[ Optional()], id="user_cfg_hide_amt", render_kw={"data-toggle": "toggle", "data-onstyle": "success", "data-offstyle": "default"})
    user_id = HiddenField('User Id')

class FiltersForm(FlaskForm):
    month_id = SelectField('Mes', coerce=int, validators=[
        Optional()
    ], id="monthIdFilter")
    year_id = SelectField('Año', coerce=int, validators=[
        Optional()
    ], id="yearFilter")
    type_id = SelectField('Tipo Operación', coerce=int, validators=[
        Optional()
    ], id="opTypeIdFilter")

class NewOperationForm(FlaskForm):
    description = StringField('Descripción', validators=[
        Length(min=4, max=100, message='La longitud debe ser entre %(min)d y %(max)d'),
        InputRequired('Tenés que agregar una descripción')
    ])
    date = DateField('Fecha', validators=[
        InputRequired('Tenés que indicar una fecha')
    ], format='%Y-%m-%d')
    amount = StringField('Monto', validators=[InputRequired('Tenés que indicar un monto')], render_kw={'pattern':'^\d{1,3}(\d{3})*(\.\d+)?$', 'placeholder': '$ 0,00'})
    type_id = SelectField('Tipo Operación', coerce=int)
    user_id = HiddenField('User Id')
    currency_id = SelectField('Moneda', coerce=int, id="opCurrencyId")
    from_saving = BooleanField('Usar ahorro', validators=[ Optional()], id="new_op_use_saving", render_kw={"data-toggle": "toggle", "data-onstyle": "success", "data-offstyle": "default"})

class AddCurrencyForm(FlaskForm):
    currency_id = SelectField('Moneda', coerce=int, id="currencyId")
    user_id = HiddenField('User Id')

class ChangeCurrencyForm(FlaskForm):
    origin_currency_id = SelectField('Moneda', coerce=int, id="orCurrencyId")
    destination_currency_id = SelectField('Moneda', coerce=int, id="desCurrencyId")
    origin_amount = StringField('Monto', validators=[InputRequired('Tenés que indicar un monto')], render_kw={'pattern':'^\d{1,3}(\d{3})*(\.\d+)?$', 'placeholder': '$ 0,00'})
    exchange_value = StringField('Monto', validators=[InputRequired('Tenés que indicar un monto')], render_kw={'pattern':'^\d{1,3}(\d{3})*(\.\d+)?$', 'placeholder': '$ 0,00'})
    total_amount = HiddenField('Monto Total')
    user_id = HiddenField('User Id')