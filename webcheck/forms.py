from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from webcheck.models import Pengguna, Web, Instansi

class SignupForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	token = StringField('Token',validators=[DataRequired()])
	submit = SubmitField('Signup')


class SigninForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Signin')


class PostUrl(FlaskForm):
	url = StringField('Url', validators=[DataRequired()])
	submit = SubmitField('Submit')

class PostInstansi(FlaskForm):
	instansi = StringField('Instansi', validators=[DataRequired()])
	submit = SubmitField('Submit')
