# Self-Attendance-System
A Web Application for marking attendance of students by recognizing the faces of students from the surveillance video footage of classroom.
## Getting Started
A Web Application in Python for recognizing students faces in a classroom from the surveillance video and marking the attendance in an Excel Sheet. Deep learning algorithms like **MTCNN** and **FaceNet** are used for face detection and recognition respectively. And using the **Flask framework**, Web App was created.
## Prerequisites
The following things needs to be installed properly in your machine.
- Tensorflow
- Flask
- scipy
- opencv
- h5py
- matplotlib
- Pillow
- requests
- psutil

For installing the packages use ```pip install ```command.
## How to use
### Step 1: Dataset Preparation
The required number of images (atleast 10) for each students should be collected and stored in seperate folders. The folders should be named in the respective students name. The path to folders can be like```Root_folder/attendance/facenet/dataset/raw/```

![raw_folder](https://user-images.githubusercontent.com/26355166/55208071-c2048880-5202-11e9-883a-b1d6f2d5ee61.png)
### Step 2: Face Detection and Alignment
Here the MTCNN face detection algorithm is used. It takes```Root_folder/attendance/facenet/dataset/raw/``` as input and```Root_folder/attendance/facenet/dataset/aligned/``` as output. Basically, it detects the faces, aligns face region of each image and store it in the aligned directory.
Run the following commands in the command prompt.
```python facenet/src/align/align_dataset_mtcnn.py facenet/dataset/raw facenet/dataset/aligned --image_size 160 --margin 32```
### Step 3: Training The Faces


