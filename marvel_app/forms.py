from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms import StringField, PasswordField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, Email

class UserLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit_button = SubmitField()

class UserSignUpForm(UserLoginForm):
    name = StringField('Name', validators=[DataRequired()])