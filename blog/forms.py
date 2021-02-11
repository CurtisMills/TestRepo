from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp, ValidationError
from blog.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=3, max=15)])
    first_name = StringField('First Name(s)', validators=[Length(max=20)])
    last_name = StringField('Last Name(s)', validators=[Length(max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


def validate_user(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user:
        raise ValidationError(
            'Username already exists. Please choose a different username.')
