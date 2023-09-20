from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Phone

class Registration(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    role = StringField('Role', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired(), Phone()])
    emergency_contact = StringField("Emergeny contact", validators=[DataRequired()])
    emergency_phone = StringField('Emergency Phone', validators=[DataRequired(), Phone()])
    parent_email = StringField("Parent's email", validators=[DataRequired(), Email()])
    submit = SubmitField("Register")