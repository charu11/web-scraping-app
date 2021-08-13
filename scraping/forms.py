from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from scraping.models import User
from wtforms.validators import Length, Email, DataRequired, ValidationError



class RegisterForm(FlaskForm):

    def username_validation(self, check_username):
        user = User.query.filter_by(username=check_username.data).first()
        if user:
            raise ValidationError('User name is already registered.....!')

    def email_validation(self, check_email):
        email = User.query.filter_by(email=check_email.data).first()
        if email:
            raise ValidationError('User name is already registered.....!')

    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password = PasswordField(label='Password:',  validators=[Length(min=6), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):

    username = StringField(label='User Name', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Sign In')
