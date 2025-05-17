# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired, Email


# форма регистрации
class RegisterForm(FlaskForm):
    username = StringField("Имя", validators=[DataRequired()])
    email = EmailField("Почта", validators=[DataRequired(), Email()])
    passwd = PasswordField("Пароль", validators=[DataRequired()])
    passwd_repeat = PasswordField("Повтор пароля", validators=[DataRequired()])
    submit = SubmitField("Зарегистрироваться")