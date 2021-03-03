from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp, ValidationError, InputRequired
from blog.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=3, max=15)],  render_kw={"placeholder": "test"})
    first_name = StringField('First Name(s)', validators=[Length(max=20)])
    last_name = StringField('Last Name(s)', validators=[Length(max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Regexp(
        '^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$', message='Your password should contain at least one uppercase letter, one lowercase letter and one number.')], render_kw={"placeholder": "must contain one lowercase, one uppercase and one number"})
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password', message='Your passwords DO NOT match.')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username taken. Please enter a new username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(
                'An account with this email address already exsists.')


class LoginForm(FlaskForm):
    email = StringField('Email', render_kw={"placeholder": "Enter Email Address"}, validators=[DataRequired(), Email()])
    password = PasswordField('Password', render_kw={"placeholder": "Enter Password"}, validators=[DataRequired()])
    submit = SubmitField('Login')


class CommentForm(FlaskForm):
    comment = StringField('Comment', validators=[InputRequired()])
    submit = SubmitField('Post comment')
