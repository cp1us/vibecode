# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired


# форма для написания коментарев
class CommentForm(FlaskForm):
    csrf = False

    text = TextAreaField("Коментарий", validators=[DataRequired()])
    submit = SubmitField("Отправить")