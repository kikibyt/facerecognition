import face_recognition
import os, sys
import cv2
import numpy as np
import numpy
import math
import tkinter as tk
from tkinter import filedialog, Label, Button
from PIL import Image, ImageTk
import pyttsx3


# Helper
def face_confidence(face_distance, face_match_threshold=0.6):
    range = (1.0 - face_match_threshold)
    linear_val = (1.0 - face_distance) / (range * 2.0)

    if face_distance > face_match_threshold:
        return str(round(linear_val * 100, 2)) + '%'
    else:
        value = (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
        return str(round(value, 2)) + '%'


class FaceRecognition:
    face_locations = []
    face_encodings = []
    face_names = []
    known_face_encodings = []
    known_face_names = []

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Parent Resemblance Detector")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        self.encode_faces()
        self.setup_ui()

    def encode_faces(self):
        # Load parent images from 'faces' folder
        for image in os.listdir('faces'):
            face_image = face_recognition.load_image_file(f"faces/{image}")
            face_encodings = face_recognition.face_encodings(face_image)
            if face_encodings:  # Ensure at least one face is detected
                self.known_face_encodings.append(face_encodings[0])
                self.known_face_names.append(os.path.splitext(image)[0])
        print("Known faces:", self.known_face_names)

    def setup_ui(self):
        # Title
        tk.Label(self.root, text="Parent Resemblance Detector", font=("Arial", 20, "bold"), bg="#f0f0f0").pack(pady=10)

        # Frames for images
        self.parent1_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.parent1_frame.pack(side=tk.LEFT, padx=20)
        self.parent2_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.parent2_frame.pack(side=tk.LEFT, padx=20)
        self.compare_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.compare_frame.pack(side=tk.LEFT, padx=20)

        # Image labels
        self.parent1_label = Label(self.parent1_frame, text="Parent 1: Not loaded", bg="#f0f0f0")
        self.parent1_label.pack()
        self.parent2_label = Label(self.parent2_frame, text="Parent 2: Not loaded", bg="#f0f0f0")
        self.parent2_label.pack()
        self.compare_label = Label(self.compare_frame, text="Compare Image: Not loaded", bg="#f0f0f0")
        self.compare_label.pack()

        # Result label
        self.result_label = tk.Label(self.root, text="Upload images to compare!", font=("Arial", 14), bg="#f0f0f0")
        self.result_label.pack(pady=20)

        # Buttons
        tk.Button(self.root, text="Upload Parent 1 Image", command=lambda: self.upload_image("parent1"), bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=5)
        tk.Button(self.root, text="Upload Parent 2 Image", command=lambda: self.upload_image("parent2"), bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=5)
        tk.Button(self.root, text="Upload Compare Image", command=lambda: self.upload_image("compare"), bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=5)
        tk.Button(self.root, text="Compare Faces", command=self.run_recognition, bg="#2196F3", fg="white", font=("Arial", 12)).pack(pady=10)

        # Initialize text-to-speech
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)
        self.engine.setProperty('rate', 170)

        # Image storage
        self.parent1_image = None
        self.parent2_image = None
        self.compare_image = None

    def upload_image(self, image_type):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            img = Image.open(file_path)
            img = img.resize((150, 150), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            
            if image_type == "parent1":
                self.parent1_image = file_path
                self.parent1_label.config(image=photo, text="")
                self.parent1_label.image = photo
                self.result_label.config(text="Parent 1 image loaded!")
            elif image_type == "parent2":
                self.parent2_image = file_path
                self.parent2_label.config(image=photo, text="")
                self.parent2_label.image = photo
                self.result_label.config(text="Parent 2 image loaded!")
            else:  # compare
                self.compare_image = file_path
                self.compare_label.config(image=photo, text="")
                self.compare_label.image = photo
                self.result_label.config(text="Compare image loaded!")

    def run_recognition(self):
        if not (self.parent1_image and self.parent2_image and self.compare_image):
            self.result_label.config(text="Please upload all images!")
            return

        # Load compare image
        compare_image = face_recognition.load_image_file(self.compare_image)
        compare_encodings = face_recognition.face_encodings(compare_image)

        if not compare_encodings:
            self.result_label.config(text="No face detected in compare image!")
            return

        compare_encoding = compare_encodings[0]
        face_distances = face_recognition.face_distance(self.known_face_encodings, compare_encoding)
        matches = face_recognition.compare_faces(self.known_face_encodings, compare_encoding)

        # Find best match
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = self.known_face_names[best_match_index]
            confidence = face_confidence(face_distances[best_match_index])
            result_text = f"You look most like {name} with {confidence} confidence!"
        else:
            result_text = "No strong match with either parent!"

        # Update UI and speak result
        self.result_label.config(text=result_text)
        self.engine.say(result_text)
        self.engine.runAndWait()

        # Highlight matched parent
        if "parent1" in result_text.lower():
            self.parent1_label.config(bg="#ffeb3b")
            self.parent2_label.config(bg="#f0f0f0")
        elif "parent2" in result_text.lower():
            self.parent2_label.config(bg="#ffeb3b")
            self.parent1_label.config(bg="#f0f0f0")
        else:
            self.parent1_label.config(bg="#f0f0f0")
            self.parent2_label.config(bg="#f0f0f0")

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    fr = FaceRecognition()
    fr.run()


