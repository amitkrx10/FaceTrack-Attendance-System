🎯 FaceTrack Attendance System

FaceTrack Attendance System is an AI-powered face recognition attendance project built with Python, OpenCV, and face_recognition. It captures faces in real time through a webcam, recognizes them using a pre-trained model, and automatically marks attendance in an Excel sheet with name, time, and date.

🚀 Features

Real-time face detection and recognition

Automatically creates daily Excel attendance files

Prevents duplicate entries for the same person

Simple webcam-based interface

Works offline once trained

🧩 Tech Stack

Language: Python

Libraries: face_recognition, OpenCV, NumPy, Pandas, Pickle

Storage: Excel (.xlsx files)

⚙️ Setup

Install required libraries:

pip install face_recognition opencv-python numpy pandas


Train faces (run once):

python improved_face_trainer.py


Run the attendance system:

python attendance_system.py

📂 Folder Structure

attendance_system.py → Main program

improved_face_trainer.py → Used for training faces

trained_faces.pkl → Stores trained encodings

Attendance/ → Saves daily Excel attendance files

📊 Output Example
Name	Time	Date
Lucky	10:12:45	2025-11-10
💡 Future Improvements

Add GUI dashboard

Cloud storage and reporting

Web or mobile integration
