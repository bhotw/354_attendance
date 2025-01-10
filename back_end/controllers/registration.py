from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
import phonenumbers

# Phone number validation function
def validate_phone(form, field):
    value = field.data

    try:
        parsed_number = phonenumbers.parse(value, "US")
        if not phonenumbers.is_valid_number(parsed_number):
            raise ValidationError('Invalid phone number')
    except phonenumbers.phonenumberutil.NumberParseException:
        raise ValidationError('Invalid phone number')

class Registration(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    role = SelectField('Role', choices=[('Student', 'Student'), ('Mentor', 'Mentor')], validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired(), validate_phone])
    emergency_contact = StringField("Emergency contact", validators=[DataRequired()])
    emergency_phone = StringField('Emergency Phone', validators=[DataRequired(), validate_phone])
    parent_email = StringField("Parent's email", validators=[DataRequired(), Email()])
    submit = SubmitField("Register")
