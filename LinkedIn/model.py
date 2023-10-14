from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from .sqlite import getUsername
import re
from flask_login import UserMixin

def username_ckeck(form, field):
    usernames = getUsername()
    if field.data in usernames:
        raise ValidationError("Username already taken!")
    
def has_special(form, field):
    pattern = r'[^a-zA-Z0-9]'

    if not re.search(pattern, field.data):
        raise ValidationError("Password should contain a special character")


class SignupForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), username_ckeck, Length(max=20)])
    email = StringField('email', validators=[DataRequired(), Email()])
    pro_type = StringField('pro_type', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(), has_special, Length(min=6)])
    confirm_password = PasswordField('confirm_password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(max=20)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('LogIn')

class User(UserMixin):
    def __init__(self, id, username, password, email, type) -> None:
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.type = type
