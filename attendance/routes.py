from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from flask import render_template,url_for,flash,redirect,request,jsonify,abort,make_response
from attendance import app, db, bcrypt
from attendance.forms import RegistrationForm, LoginForm, AddForm, EditForm
from attendance.models import User,Add
from flask_login import login_user, current_user, logout_user, login_required

import os
import pickle
import sys
import time
import cv2
import numpy as np
import tensorflow as tf
from scipy import misc
import attendance.facenet.src.facenet as facenet
from facenet.src.align import detect_face
from keras.models import load_model
from flask_httpauth import HTTPBasicAuth
import sqlite3
import xlsxwriter
import datetime
import requests
from werkzeug.utils import secure_filename

auth = HTTPBasicAuth()

@app.route("/")
@app.route("/home")
def home():
	return render_template('home.html')

@app.route("/about")
def about():
	return render_template('about.html',title='About')

@app.route("/register", methods=['GET','POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash('Your account has been created! You are now able to Log In', 'success')
		return redirect(url_for('login'))
	return render_template('register.html',title='Register',form=form)

@app.route("/login", methods=['GET','POST'])	
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			flash('You have been logged in!','success')
			next_page = request.args.get('next')
			if next_page:
				return redirect(next_page) 
			else:
				return redirect(url_for('home'))
		else:
			flash('Login Unsuccessful. Please check Email and Password','danger')	
	return render_template('login.html',title='Login',form=form)

@app.route("/add", methods=['GET','POST'])
@login_required
def add():
	form = AddForm()
	if form.validate_on_submit():
		new = Add(classname=form.classname.data, coordinator=form.coordinator.data, co_email=form.co_email.data, stuname=form.stuname_1.data, regno=form.regno_1.data, mobileno=form.mobileno_1.data)
		db.session.add(new)
		new = Add(stuname=form.stuname_2.data, regno=form.regno_2.data, mobileno=form.mobileno_2.data)
		db.session.add(new)
		new = Add(stuname=form.stuname_3.data, regno=form.regno_3.data, mobileno=form.mobileno_3.data)
		db.session.add(new)		
		new = Add(stuname=form.stuname_4.data, regno=form.regno_4.data, mobileno=form.mobileno_4.data)
		db.session.add(new)
		new = Add(stuname=form.stuname_5.data, regno=form.regno_5.data, mobileno=form.mobileno_5.data)						
		db.session.add(new)
		db.session.commit()
		flash('A new class has been created!','success')
		return redirect(url_for('home'))
	return render_template('add.html',title='Adding Class',form=form)

@app.route("/edit",methods=['GET','POST'])
@login_required
def edit():
	form = EditForm()
	if form.validate_on_submit():
		db.session.commit()
		flash('The existing class has been updated!','success')
		return redirect(url_for('home'))
	return render_template('edit.html',title='Editing Class',form=form)	

@app.route("/take")
@login_required
def take():
	return render_template('take.html',title="Take Attendance")		

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))

@app.route("/recognition")
def recognition():
	return render_template('recog.html',title="Recognized students")
	
@app.route("/face_recog", methods=['GET','POST'])
def face_recog():
	if request.method == "POST":
		file=request.files["image"]
		filename = secure_filename(file.filename)
	names = []	
	img_name=str(filename)	
	img_path="attendance/facenet/dataset/test-images/"+img_name
	modeldir = "attendance/facenet/src/20180402-114759/"
	classifier_filename = "attendance/facenet/src/20180402-114759/my_classifier.pkl"
	npy=""
	train_img="attendance/facenet/dataset/raw"

	workbook = xlsxwriter.Workbook('C:\\Users\\Dell\\Attendance\\Reports\\Report_for_'+ datetime.datetime.now().strftime("%Y_%m_%d-%H")+'.xlsx')
	worksheet = workbook.add_worksheet()
	conn = sqlite3.connect('C:\\Users\\Dell\\Attendance\\attendance\\site.db')
	c = conn.cursor()
	students = c.execute("SELECT stuname FROM 'add'")

	with tf.Graph().as_default():
		gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.6)
		sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
		with sess.as_default():
			pnet, rnet, onet = detect_face.create_mtcnn(sess, npy)
			
			minsize = 20  # minimum size of face
			threshold = [0.6, 0.7, 0.7]  # three steps's threshold
			factor = 0.709  # scale factor
			margin = 32
			frame_interval = 3
			batch_size = 1000
			image_size = 160
			input_image_size = 160

			HumanNames = os.listdir(train_img)
			HumanNames.sort()

			print('Loading feature extraction model')
			facenet.load_model(modeldir)

			images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
			embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
			phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
			embedding_size = embeddings.get_shape()[1]

			classifier_filename_exp = os.path.expanduser(classifier_filename)
			with open(classifier_filename_exp, 'rb') as infile:
				(model, class_names) = pickle.load(infile)
			# video_capture = cv2.VideoCapture("akshay_mov.mp4")
			c = 0 

			print('Start Recognition!')
			prevTime = 0
			# ret, frame = video_capture.read()
			frame = cv2.imread(img_path,0)
			#frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)    #resize frame (optional)
			curTime = time.time()+1    # calc fps
			timeF = frame_interval
			if (c % timeF == 0):
				find_results = []
				if frame.ndim == 2:
					frame = facenet.to_rgb(frame)
				frame = frame[:, :, 0:3]
				bounding_boxes, _ = detect_face.detect_face(frame, minsize, pnet, rnet, onet, threshold, factor)
				nrof_faces = bounding_boxes.shape[0]
				print('Face Detected: %d' % nrof_faces)   				
				if nrof_faces > 0:
					det = bounding_boxes[:, 0:4]
					img_size = np.asarray(frame.shape)[0:2]
					cropped = []
					scaled = []
					scaled_reshape = []
					bb = np.zeros((nrof_faces,4), dtype=np.int32)
				for i in range(nrof_faces):
					emb_array = np.zeros((1, embedding_size))
					bb[i][0] = det[i][0]
					bb[i][1] = det[i][1]
					bb[i][2] = det[i][2]
					bb[i][3] = det[i][3]
					#inner exception
					if bb[i][0] <= 0 or bb[i][1] <= 0 or bb[i][2] >= len(frame[0]) or bb[i][3] >= len(frame):
						print('face is too close')
						break
					cropped.append(frame[bb[i][1]:bb[i][3], bb[i][0]:bb[i][2], :])
					cropped[i] = facenet.flip(cropped[i], False)
					scaled.append(misc.imresize(cropped[i], (image_size, image_size), interp='bilinear'))
					scaled[i] = cv2.resize(scaled[i], (input_image_size,input_image_size),
										   interpolation=cv2.INTER_CUBIC)
					scaled[i] = facenet.prewhiten(scaled[i])
					scaled_reshape.append(scaled[i].reshape(-1,input_image_size,input_image_size,3))
					feed_dict = {images_placeholder: scaled_reshape[i], phase_train_placeholder: False}
					emb_array[0, :] = sess.run(embeddings, feed_dict=feed_dict)
					predictions = model.predict_proba(emb_array)
					#print(predictions)
					best_class_indices = np.argmax(predictions, axis=1)
					# no print(best_class_indices)
					best_class_probabilities = predictions[np.arange(len(best_class_indices)), best_class_indices]
					#print(best_class_probabilities)
					cv2.rectangle(frame, (bb[i][0], bb[i][1]), (bb[i][2], bb[i][3]), (0, 255, 0), 2)    #boxing face
					#plot result idx under box
					text_x = bb[i][0]
					text_y = bb[i][3] + 20
					#print('Result Indices: ', best_class_indices[0])
					print(HumanNames[best_class_indices[0]])
					names.append(HumanNames[best_class_indices[0]])
					for H_i in HumanNames:
						if HumanNames[best_class_indices[0]] == H_i and best_class_probabilities > 0.43:
							result_names = HumanNames[best_class_indices[0]]
							cv2.putText(frame, result_names, (text_x, text_y), cv2.FONT_HERSHEY_COMPLEX_SMALL,1, (0, 0, 255), thickness=1, lineType=1)
			else:
				print('Unable to align')

	for i, row in enumerate(students):
		for j, value in enumerate(row):
			worksheet.write_string(i,j+2,'Absent')
			for name in names:
				if name == value:
					worksheet.write_string(i,j+2,'Present') 
			worksheet.write_string(i,j, str(value))	

	# reg_no = c.execute("SELECT regno FROM 'add'")
	# for i, row in enumerate(reg_no):
	# 	for j, value in enumerate(row):
	# 		worksheet.write(i,j+1,value)

	cv2.imshow('Image', frame)
	cv2.imwrite('output/'+img_path.split('/')[-1],frame)
	if cv2.waitKey(9000) & 0xFF == ord('q'):
		sys.exit("Thanks")
	workbook.close()		
	cv2.destroyAllWindows() 
	flash('The students faces were recognized successfully!','success')
	return render_template('take.html',title="Take Attendance")	                   

@app.route("/mark", methods=['GET','POST'])
def mark():
	#workbook = xlsxwriter.Workbook('C:\\Users\\Dell\\Attendance\\Reports\\Report_for_'+ datetime.datetime.now().strftime("%Y_%m_%d-%H")+'.xlsx')
	#worksheet = workbook.add_worksheet()
	#conn = sqlite3.connect('C:\\Users\\Dell\\Attendance\\attendance\\site.db')
	#c = conn.cursor()
	#students = c.execute("SELECT stuname FROM 'add'")
	#name = face_recog()
	#for i, row in enumerate(students):
		#for j, value in enumerate(row):
			#worksheet.write_string(i,j, str(value))
			#if name == value:
				#worksheet.write_string(i,j+1,'Present') 
			#else:
				#worksheet.write_string(i,j+1, 'Absent')
	#workbook.close()
	return render_template('take.html',title="Take Attendance")

@app.route("/sms", methods=['GET','POST'])
def sms():	
	return render_template('take.html',title="Take Attendance")
