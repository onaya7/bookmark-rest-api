from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from src.database import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=4, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(
        min=6, max=35, message='Little short for an email address?')])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm_password'), Length(min=5, max=50, message="Password is too short"), Regexp('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$',message='Password must include at least one uppercase letter, one lowercase letter, one number, and one special character')])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired()])

    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "This username is already in use by another user"
            )
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                "This email is taken. Please choose a different one")


class PasswordresetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(
        min=6, max=35, message='Little short for an email address?')])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm_password' , message="Password must match confirm password"), Length(min=5, max=50, message="Password is too short"), Regexp('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$',
                                                                                                                                                                 message='Password must include at least one uppercase letter, one lowercase letter, one number, and one special character')])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired()])
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        
        if not user:
            raise ValidationError(
                "This user does not exit in this system"
            )
