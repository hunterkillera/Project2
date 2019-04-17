''' Flask's pythonic way to deal with HTML froms '''
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators


class QueryForm(FlaskForm):
    artist = StringField('Artist', [validators.DataRequired()])
    submit = SubmitField('Submit')