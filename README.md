Parent Resemblance Detector
Overview
The Parent Resemblance Detector is a Python application that compares a user's face to two parent images to determine resemblance. It offers two versions:

Local Version: Uses a Tkinter GUI, webcam for real-time face capture, and pyttsx3 for text-to-speech, running locally on Windows (e.g., in VSCode).
Streamlit Version: A web-based app for Streamlit Cloud, using image uploads for all inputs (no webcam) and text output.

The local version uses opencv-python with a Haar Cascade classifier for face detection and histogram correlation for similarity comparison, avoiding dlib. The Streamlit version adapts this for web deployment.
Features

Local Version:
Upload two parent images via Tkinter GUI.
Capture your face via webcam with real-time face detection (green rectangle).
Compare faces and announce results via pyttsx3 (e.g., "You look most like Parent 1 with 75.23% similarity!").
Visual feedback with highlighted matched parent.


Streamlit Version:
Upload three images (Parent 1, Parent 2, Compare) via web interface.
Display resemblance result as text.
No webcam or audio support.



Prerequisites

Local Version:
Windows 10/11 with a webcam and speakers.
Python 3.10 or later (3.13 tested).
VSCode with Python extension.
Project directory: C:\Users\lenovo\OneDrive\Desktop\facerecognition (or your workspace, e.g., /workspaces/facerecognition).


Streamlit Version:
GitHub account for Streamlit Cloud deployment.
No hardware requirements (runs in browser).



Dependencies

Local Version:
opencv-python
numpy
pyttsx3
pillow


Streamlit Version:
streamlit
opencv-python
numpy
pillow



Setup Instructions
Local Version (Windows/VSCode)

Set Up Project Directory:

Ensure recognition.py is in C:\Users\lenovo\OneDrive\Desktop\facerecognition (or /workspaces/facerecognition in Codespaces).
Download recognition.py from the project artifacts.


Set Up Virtual Environment:
cd C:\Users\lenovo\OneDrive\Desktop\facerecognition
python -m venv .venv
.venv\Scripts\activate


Install Dependencies:
pip install opencv-python numpy pyttsx3 pillow


For Codespaces (Linux):sudo apt update && sudo apt install -y libgl1-mesa-glx libglib2.0-0 python3-tk
pip install opencv-python numpy pyttsx3 pillow




Configure VSCode:

Open VSCode:code .


Select .venv\Scripts\python.exe (or .venv/bin/python in Codespaces) as the interpreter.



Streamlit Version (Cloud)

Create GitHub Repository:

Create a repository (e.g., facerecognition).
Add app.py (Streamlit script) and requirements.txt:streamlit
opencv-python
numpy
pillow




Deploy on Streamlit Cloud:

Sign up at streamlit.io.
Create a new app, link your GitHub repository, and select app.py.
Access the app (e.g., https://your-app-name.streamlit.app).



Usage
Local Version

Run the Application:
.venv\Scripts\activate
python recognition.py


A Tkinter GUI opens.


Upload Parent Images:

Click “Upload Parent 1 Image” and “Upload Parent 2 Image” to select clear, frontal face images (JPG/PNG).


Start Webcam:

Click “Start Webcam” to show the webcam feed with a green rectangle around detected faces.
Ensure good lighting and a frontal face position.


Compare Faces:

Click “Compare Faces” to compare your face to parent images.
Results display in the GUI and are announced via speakers.


Exit:

Close the window to stop the webcam and exit.



Streamlit Version

Access the App:
Open the Streamlit Cloud URL.


Upload Images:
Upload Parent 1, Parent 2, and Compare images.


Compare Faces:
Click “Compare Faces” to see the result (e.g., “You look most like Parent 1 with 75.23% similarity!”).



Troubleshooting

ModuleNotFoundError: No module named 'cv2':
Install opencv-python:pip install opencv-python


For Codespaces:sudo apt install -y libgl1-mesa-glx libglib2.0-0




Webcam Not Opening (Local):
Test:import cv2
cap = cv2.VideoCapture(0)
print(cap.isOpened())


Check Windows camera permissions (Settings → Privacy → Camera).


No Face Detected:
Use clear, frontal face images and good lighting.
Adjust detectMultiScale parameters (e.g., scaleFactor=1.1, minNeighbors=3).


Audio Issues (Local):
Test pyttsx3:import pyttsx3
engine = pyttsx3.init()
engine.say("Test")
engine.runAndWait()


Check Windows audio settings.


Tkinter Not Working:
Install python3-tk (Codespaces) or verify Python installation (Windows).


Streamlit Deployment:
Ensure requirements.txt includes all dependencies.
Check Streamlit Cloud logs for errors.



Limitations

Local Version:
Requires a webcam and speakers.
Histogram correlation is less accurate than deep learning (e.g., face_recognition).


Streamlit Version:
No webcam or audio support.
Requires image uploads for comparison.


Cloud Platforms:
Replit and Streamlit Cloud don’t support webcams, limiting the local version to Windows.



License
For personal use. Contact the author for permissions.
Author
Developed for a user needing a webcam-based face recognition app, avoiding dlib and supporting local Windows execution.

