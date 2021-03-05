from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp, ValidationError, InputRequired
from blog.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=3, max=15)],  render_kw={"placeholder": "Please create a username"})
    first_name = StringField('First Name(s)', render_kw={"placeholder": "Enter first name"}, validators=[Length(max=20)])
    last_name = StringField('Last Name(s)', render_kw={"placeholder": "Enter last name"}, validators=[Length(max=20)])
    email = StringField('Email', render_kw={"placeholder": "Enter email address"}, validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Regexp(
        '^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$', message='Your password should contain at least one uppercase letter, one lowercase letter')], render_kw={"placeholder": "Must contain: number, uppercase and lowercase"})
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password', message='Your passwords DO NOT match.')], render_kw={"placeholder": "Re-enter password"})
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
