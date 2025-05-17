# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


# форма для написания поста
class PostForm(FlaskForm):
    csrf = False

    header = StringField("Название поста", validators=[DataRequired()])
    text = TextAreaField("Текст поста")
    submit = SubmitField("Отправить")
