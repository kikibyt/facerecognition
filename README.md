Parent Resemblance Detector


https://github.com/user-attachments/assets/50644006-db54-4430-b268-c12df45f93b5


👩🏾‍💻 Parent Resemblance Detector
🌸 A Python application to compare your face to two parent images and determine resemblance.
This project offers two versions: a local desktop app with a Tkinter GUI and webcam support, and a web-based app deployed on Streamlit Cloud. Both use OpenCV for face detection and histogram correlation for similarity comparison, delivering a fun and accessible way to explore facial resemblance.

🎯 Features
🖥️ Local Version (Tkinter)

📸 Upload two parent images via a sleek Tkinter GUI.
🎥 Capture your face in real-time using a webcam (green rectangle for face detection).
🔊 Hear results announced via text-to-speech (e.g., "You look most like Parent 1 with 75.23% similarity!").
🖼️ Visual feedback highlights the matched parent.




🛠️ Prerequisites
Local Version

💻 Windows 10/11 with a webcam and speakers.
🐍 Python 3.10+ (tested with 3.13).
📂 Project directory: C:\Users\lenovo\OneDrive\Desktop\facerecognition (or /workspaces/facerecognition in Codespaces).
🖥️ VSCode with Python extension.



📦 Dependencies



Version
Dependencies



Local
opencv-python, numpy, pyttsx3, pillow


Streamlit
streamlit, opencv-python, numpy, pillow



⚙️ Setup Instructions
🖥️ Local Version (Windows/VSCode)

Set Up Project Directory:

Place recognition.py in C:\Users\lenovo\OneDrive\Desktop\facerecognition (or /workspaces/facerecognition in Codespaces).
Download recognition.py from the project artifacts.


Create Virtual Environment:
cd C:\Users\lenovo\OneDrive\Desktop\facerecognition
python -m venv .venv
.venv\Scripts\activate


Install Dependencies:
pip install opencv-python numpy pyttsx3 pillow


For Codespaces (Linux):
sudo apt update && sudo apt install -y libgl1-mesa-glx libglib2.0-0 python3-tk
pip install opencv-python numpy pyttsx3 pillow


Configure VSCode:

Open VSCode: code .
Select .venv\Scripts\python.exe (or .venv/bin/python in Codespaces) as the interpreter.



🌐 Streamlit Version (Cloud)

Create GitHub Repository:

Create a repository (e.g., facerecognition).
Add app.py (Streamlit script) and requirements.txt:streamlit
opencv-python
numpy
pillow








🚀 Usage
🖥️ Local Version

Run the Application:
.venv\Scripts\activate
python recognition.py

A Tkinter GUI will open.

Upload Parent Images:

Click “Upload Parent 1 Image” and “Upload Parent 2 Image” (JPG/PNG, clear frontal faces).


Start Webcam:

Click “Start Webcam” to view the feed with a green rectangle around detected faces.
Ensure good lighting and a frontal face position.


Compare Faces:

Click “Compare Faces” to see and hear the resemblance result.


Exit:

Close the window to stop the webcam and exit.






Upload Images:

Upload Parent 1, Parent 2, and Compare images.


Compare Faces:

Click “Compare Faces” to view the result (e.g., “You look most like Parent 1 with 75.23% similarity!”).




🛠️ Troubleshooting

ModuleNotFoundError: No module named 'cv2':
pip install opencv-python

For Codespaces:
sudo apt install -y libgl1-mesa-glx libglib2.0-0


Webcam Not Opening (Local):

Test:import cv2
cap = cv2.VideoCapture(0)
print(cap.isOpened())


Check Windows camera permissions: Settings → Privacy → Camera.


No Face Detected:

Use clear, frontal face images with good lighting.
Adjust detectMultiScale parameters: scaleFactor=1.1, minNeighbors=3.


Audio Issues (Local):

Test pyttsx3:import pyttsx3
engine = pyttsx3.init()
engine.say("Test")
engine.runAndWait()


Check Windows audio settings.


Tkinter Not Working:

For Codespaces: sudo apt install -y python3-tk.
For Windows: Verify Python installation includes Tkinter.


Streamlit Deployment:

Ensure requirements.txt lists all dependencies.
Check Streamlit Cloud logs for errors.




⚠️ Limitations

Local Version: Requires a webcam and speakers. Histogram correlation is less accurate than deep learning (e.g., face_recognition).
Streamlit Version: No webcam or audio support; relies on uploaded images.


📬 Get in Touch
Have questions or ideas? Reach out! mercyokebiorun@gmail.com


 “Technology brings us closer—sometimes literally, by finding family resemblance!”


  body {
    background-color: #FFF5F7;
    font-family: 'Arial', sans-serif;
    color: #333;
  }
  h1, h2, h3 {
    color: #FF69B4;
  }
  a {
    color: #FF1493;
    text-decoration: none;
  }
  a:hover {
    color: #C71585;
  }
  i {
    color: #FF69B4;
    margin-right: 8px;
  }
  table {
    border-collapse: collapse;
    width: 100%;
    margin: 20px 0;
  }
  th, td {
    border: 1px solid #FF69B4;
    padding: 10px;
    text-align: left;
  }
  th {
    background-color: #FFD1DC;
  }




