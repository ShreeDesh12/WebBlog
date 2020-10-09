from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class queryForm(FlaskForm):
    email = StringField('Email',validators = [DataRequired(),Email()])
    Query = StringField('Query',validators = [DataRequired(),Length(min=10,max=150)])
    submit = SubmitField('Submit')
