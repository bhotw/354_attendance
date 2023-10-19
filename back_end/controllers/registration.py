from flask_wtf import FlaskForm
from wtforms import StringField, validators
import phonenumbers

from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

def validate_phone(form, field):
    value = field.data

    try:
        parsed_number = phonenumbers.parse(value, "US")
        if not phonenumbers.is_valid_number(parsed_number):
            raise validators.ValidationError('Invalid phone number')
    except phonenumbers.phonenumberrutil.NumberFormatError:
        raise validators.ValidationError('Invalid phone number')

class Registration(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    role = StringField('Role', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired(), validate_phone])
    emergency_contact = StringField("Emergeny contact", validators=[DataRequired()])
    emergency_phone = StringField('Emergency Phone', validators=[DataRequired(), validate_phone])
    parent_email = StringField("Parent's email", validators=[DataRequired(), Email()])
    submit = SubmitField("Register")