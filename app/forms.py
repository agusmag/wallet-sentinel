from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, DateField, DecimalField, SelectField, HiddenField
from wtforms.validators import  Length, InputRequired, Email, DataRequired, EqualTo, Optional

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

class FiltersForm(FlaskForm):
    month_id = SelectField('Mes', coerce=int, validators=[
        Optional()
    ])
    type_id = SelectField('Tipo Operación', coerce=int, validators=[
        Optional()
    ])

class NewOperationForm(FlaskForm):
    description = StringField('Descripción', validators=[
        Length(min=4, max=100, message='La longitud debe ser entre %(min)d y %(max)d'),
        InputRequired('Tenés que agregar una descripción')
    ])
    date = DateField('Fecha', validators=[
        InputRequired('Tenés que indicar una fecha')
    ])
    amount = DecimalField('Monto', places=2, validators=[
        InputRequired('Tenés que indicar un monto')
    ])
    type_id = SelectField('Tipo Operación', coerce=int)
    user_id = HiddenField('User Id')