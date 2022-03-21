from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, IntegerField, BooleanField,
                     RadioField, EmailField, PasswordField, SelectField)
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import InputRequired, Length, DataRequired, EqualTo, ValidationError
from blogapp.models import User
from flask import flash


class SignupForm(FlaskForm):
    first_name = StringField(label='First name', validators=[DataRequired(message='First name required')])
    last_name = StringField(label='Last name', validators=[DataRequired(message='Last name required')])
    email = EmailField(label='Email address', validators=[DataRequired(message='Email address required')])
    password = PasswordField(label='Password', validators=[DataRequired(message='Password required')])
    password_repeat = PasswordField(label='Repeat Password',
                                    validators=[DataRequired(), EqualTo('password', message='Passwords must match')])

    def validate_email(self, email):
        users = User.query.filter_by(email=email.data).first()
        if users is not None:
            raise ValidationError('An account is already registered for that email address')

class LoginForm(FlaskForm):
    email = EmailField(label='Email address', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    remember = BooleanField(label='Remember me')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            flash(f'Error, no account found with that email address.', 'error')
            raise ValidationError('No account found with that email address.')

    def validate_password(self, password):
        user = User.query.filter_by(email=self.email.data).first()
        if user is None:
            flash(f'Error, no account found with that email address.', 'error')
            raise ValidationError('No account found with that email address.')
        if not user.check_password(password.data) and user.password != password.data:
            flash(f'Error, incorrect password.', 'error')
            raise ValidationError('Incorrect password.')
