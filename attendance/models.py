from datetime import datetime
from attendance import app, db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model,UserMixin):
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(20),unique=True,nullable=False)
	email = db.Column(db.String(20),unique=True,nullable=False)
	password = db.Column(db.String(20),nullable=False)
	def __repr__(self):
		return f"User('{self.username}','{self.email}')"

class Add(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	classname = db.Column(db.String(20),unique=True)
	#students = db.Column(db.Integer, unique=True, nullable=False)
	coordinator = db.Column(db.String(30), unique=True)
	co_email = db.Column(db.String(30),unique=True)
	stuname = db.Column(db.String(30),unique=True)
	regno = db.Column(db.Integer,unique=True)
	mobileno = db.Column(db.Integer,unique=True)
	# def get_my_form(self):
	# 	from attendance.forms import AddForm
	# 	return AddForm()
	# def insertion():		
	# 	form = self.get_my_form()
	# 	num = form.students.data
	# 	stu[num]
	# 	regno[num]	
	# 	for i in range(num):
	def __repr__(self):
		return f"Add('{self.classname}','{self.coordinator}','{self.co_email}','{self.stuname}','{self.regno}','{self.mobileno}')"
		   