# FaceNet based Attendance System
> A **Deep Learning** based Web Application for marking attendance of students by recognizing the student's faces from the surveillance video footage of classroom.

## Getting Started
A Web Application in Python for recognizing student's faces in a classroom from the surveillance video and marking the attendance in an Excel Sheet. Deep learning algorithms like **MTCNN** and **FaceNet** are used for **face detection** and **recognition** respectively. And using the **Flask framework**, the Web App was created.

## Algorithms Used
- MTCNN (Multi-Task Cascaded Convolutional Neural Networks)
- FaceNet

## Prerequisites
The following things needs to be installed properly in your machine.
- Tensorflow
- Python 
- Flask
- scipy
- opencv
- h5py
- matplotlib
- Pillow
- requests
- psutil

For installing the packages use `pip install` command.

## How to use
### Step 1: Prepare Dataset
The required number of **images** (atleast 10) for each students should be collected and stored in seperate folders. The folders should be named in the respective students name. The path to folders can be `Root_folder/attendance/facenet/dataset/raw/`

![raw_folder](https://user-images.githubusercontent.com/26355166/55208071-c2048880-5202-11e9-883a-b1d6f2d5ee61.png)

### Step 2: Detect and Align Faces
Here the **MTCNN face detection algorithm** is used. It takes `Root_folder/attendance/facenet/dataset/raw/` as input and returns `Root_folder/attendance/facenet/dataset/aligned/` as output. Basically, it **detects** the faces, **aligns** face region of each image and **store** it in the aligned directory.

Run the following command in the command prompt.</br>
```bash
$ python attendance/facenet/src/align/align_dataset_mtcnn.py 
attendance/facenet/dataset/raw attendance/facenet/dataset/aligned 
--image_size 160 --margin 32
```

![aligned_folder](https://user-images.githubusercontent.com/26355166/55209252-9e900c80-5207-11e9-8964-ef9a09a50fc1.png)

![aligned_faces](https://user-images.githubusercontent.com/26355166/55208772-730c2280-5205-11e9-928d-475c07118af4.png)

### Step 3: Training The Faces
The output dataset from **Step 2** are fed into the **Support Vector Machine classifier** which generates a **512 dimensional embedding vector** for faces of each students and **trains** the classifier on the generated vectors.

Run the following commands in the command prompt.</br>
```bash
$ python attendance/facenet/src/classifier.py TRAIN 
attendance/facenet/dataset/aligned attendance/facenet/src/20180402-114759/  
attendance/facenet/src/20180402-114759/my_classifier.pkl 
--batch_size 1000 --min_nrof_images_per_class 10  --nrof_train_images_per_class 10 --use_split_dataset
```

### Step 4: Report folder
Create an empty folder named **Reports**. This is for storing the **Excel sheets report of the attendance**, which is automatically generated when the Facenet algorithm recognizes the students. This is implemented using **XlsxWriter Python module**.

### Step 5: Running the Web Application
Now run the Web application by `$ python run.py` It will show a localhost address like `http://127.0.0.1:5000/` which will be the URL for the Web App.

### Step 6: Storing Data
While running the application, it redirects to the Home page. On that page, there is an **Add class details** hyperlink. Basically it asks the user to enter the student's details. The provided details are stored in the **Sqlite Database**.
> **Note:** The **Name** of each students entered should be the same as the **name of the student's dataset** created in **step 1**. 

### Step 7: Uploading Image
On pressing the **Take Attendance** hyperlink, it redirects you to a page where the user needs to upload an image of the classroom.
> **Note:** The image should be in a good resolution and also it contains the clear faces of all students.

## Result
After uploading the image it takes sometime to process. You can view the running background details in the command prompt. Then it creates an Excel sheet in the Reports folder which contains the attendance details.

## References
- https://github.com/davidsandberg/facenet
- https://github.com/AISangam/Facenet-Real-time-face-recognition-using-deep-learning-Tensorflow
- https://github.com/abhijeet3922/Face_ID


