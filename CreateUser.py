from flask_wtf import Form
from wtforms import StringField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField
from wtforms import validators, ValidationError

class CreateUser(Form):
    email = StringField("Email",[validators.Email("Please enter a valid email address.")])
    password = StringField("Password")
    verifyPassword = StringField("Verify Password")
    role = RadioField("Role", choices = [('S','Staff'), ('C','Customer')])
    submit = SubmitField("Submit")

                           