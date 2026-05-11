from flask_wtf import FlaskForm

from wtforms import PasswordField
from wtforms import BooleanField
from wtforms import SubmitField
from wtforms import EmailField

from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')