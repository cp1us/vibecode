# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email


# форма логина
class LoginForm(FlaskForm):
    email = EmailField("Почта", validators=[DataRequired(), Email()])
    passwd = PasswordField("Пароль", validators=[DataRequired()])
    remember_me = BooleanField("Запомнить меня")
    submit = SubmitField("Войти")
