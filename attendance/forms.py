from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from attendance.models import User,Add

class RegistrationForm(FlaskForm):
	username = StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
	email = StringField('Email', validators=[DataRequired(),Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('password')])
	submit = SubmitField('Register')
	def validate_username(self,username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('That username is taken. Please choose a different one')
	
	def	validate_email(self,email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('That email is taken. Please choose a different one')		

class LoginForm(FlaskForm):
	email = StringField('Email',validators=[DataRequired(),Email()])
	password = PasswordField('Password',validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')

class AddForm(FlaskForm):
	classname = StringField('Class Name',validators=[DataRequired()])
	students = IntegerField('No of Students')
	coordinator = StringField('Coordinator Name',validators=[DataRequired(),Length(min=2,max=20)])
	co_email = StringField('Coordinator Email',validators=[DataRequired(),Email()])
	stuname_1 = StringField('Student Name',validators=[DataRequired()])
	regno_1 = IntegerField('Reg No',validators=[DataRequired()])
	mobileno_1 = IntegerField('Parents Mobile No',validators=[DataRequired()])
	stuname_2 = StringField('Student Name',validators=[DataRequired()])
	regno_2 = IntegerField('Reg No',validators=[DataRequired()])
	mobileno_2 = IntegerField('Parents Mobile No',validators=[DataRequired()])
	stuname_3 = StringField('Student Name',validators=[DataRequired()])
	regno_3 = IntegerField('Reg No',validators=[DataRequired()])
	mobileno_3 = IntegerField('Parents Mobile No',validators=[DataRequired()])
	stuname_4 = StringField('Student Name',validators=[DataRequired()])
	regno_4 = IntegerField('Reg No',validators=[DataRequired()])
	mobileno_4 = IntegerField('Parents Mobile No',validators=[DataRequired()])	
	stuname_5 = StringField('Student Name',validators=[DataRequired()])
	regno_5 = IntegerField('Reg No',validators=[DataRequired()])
	mobileno_5 = IntegerField('Parents Mobile No',validators=[DataRequired()])	
	submit = SubmitField('Create')
	
class EditForm(FlaskForm):
	classname = StringField('Class Name',validators=[DataRequired()])
	students = IntegerField('No of Students',validators=[DataRequired()])
	coordinator = StringField('Coordinator Name',validators=[DataRequired(),Length(min=2,max=20)])
	co_email = StringField('Coordinator Email',validators=[DataRequired(),Email()])	
	stuname = StringField('Student Name',validators=[DataRequired(),Length(min=2,max=20)])
	regno = IntegerField('Reg No',validators=[DataRequired(),Length(min=12,max=12)])
	mobile_no = IntegerField('Parents Mobile No',validators=[DataRequired(),Length(min=10,max=10)])
	submit = SubmitField('Update')
