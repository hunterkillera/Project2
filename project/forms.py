''' Flask's pythonic way to deal with HTML forms '''

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators


class QueryForm(FlaskForm):
    artist = StringField('Artist', [validators.DataRequired()])
    submit = SubmitField('Submit')