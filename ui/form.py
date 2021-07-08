from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, AnyOf


class SearchForm(FlaskForm):
    search_key = StringField(u'Search', validators=[DataRequired()])
    submit = SubmitField()

