from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, BooleanField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
import sqlalchemy as sa
from app import db
from app.models import Users


class SubmitWordForm(FlaskForm):
    name = StringField('Word', validators=[DataRequired()])
    speach_part = StringField('Speach_part', validators=[DataRequired()])
    translations = StringField('Translations', validators=[DataRequired()])
    definition = StringField('Definition', validators=[DataRequired()])
    importance = IntegerField('Importance', validators=[DataRequired()])
    topic = StringField('Topic', validators=[DataRequired()])
    submit = SubmitField('Add word')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    @staticmethod
    def validate_username(self, username):
        user = db.session.scalar(sa.select(Users).where(Users.nickname == username.data))
        if user is not None:
            raise ValidationError('Please use a different username.')

    @staticmethod
    def validate_email(self, email):
        user = db.session.scalar(sa.select(Users).where(Users.email == email.data))
        if user is not None:
            raise ValidationError('Please use different email address.')


class EditProfileForm(FlaskForm):
    username = StringField('User', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')


