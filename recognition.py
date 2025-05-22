import os
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, Label, Button
from PIL import Image, ImageTk
import pyttsx3


# Helper: Calculate histogram correlation for image similarity
def compare_histograms(img1, img2):
    # Convert images to grayscale
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    # Calculate histograms
    hist1 = cv2.calcHist([img1_gray], [0], None, [256], [0, 256])
    hist2 = cv2.calcHist([img2_gray], [0], None, [256], [0, 256])
    # Normalize histograms
    cv2.normalize(hist1, hist1)
    cv2.normalize(hist2, hist2)
    # Compute correlation (higher = more similar)
    correlation = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
    return correlation * 100  # Convert to percentage


class FaceRecognition:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Parent Resemblance Detector")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.video_capture = None
        self.compare_face = None
        self.webcam_running = False
        self.setup_ui()

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
        self.compare_label = Label(self.compare_frame, text="Webcam: Not active", bg="#f0f0f0")
        self.compare_label.pack()

        # Result label
        self.result_label = tk.Label(self.root, text="Upload parent images and start webcam!", font=("Arial", 14), bg="#f0f0f0")
        self.result_label.pack(pady=20)

        # Buttons
        tk.Button(self.root, text="Upload Parent 1 Image", command=lambda: self.upload_image("parent1"), bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=5)
        tk.Button(self.root, text="Upload Parent 2 Image", command=lambda: self.upload_image("parent2"), bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=5)
        tk.Button(self.root, text="Start Webcam", command=self.start_webcam, bg="#FF9800", fg="white", font=("Arial", 12)).pack(pady=5)
        tk.Button(self.root, text="Compare Faces", command=self.run_recognition, bg="#2196F3", fg="white", font=("Arial", 12)).pack(pady=10)

        # Initialize text-to-speech
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)
        self.engine.setProperty('rate', 170)

        # Image storage
        self.parent1_image = None
        self.parent2_image = None
        self.parent1_face = None
        self.parent2_face = None

    def upload_image(self, image_type):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            img = Image.open(file_path)
            img = img.resize((150, 150), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            # Load image for OpenCV processing
            cv_img = cv2.imread(file_path)
            faces = self.face_cascade.detectMultiScale(cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY), 1.3, 5)
            face_img = None
            if len(faces) > 0:
                (x, y, w, h) = faces[0]  # Use the first detected face
                face_img = cv_img[y:y+h, x:x+w]

            if image_type == "parent1":
                self.parent1_image = file_path
                self.parent1_face = face_img
                self.parent1_label.config(image=photo, text="")
                self.parent1_label.image = photo
                self.result_label.config(text="Parent 1 image loaded!" if face_img is not None else "No face detected in Parent 1!")
            elif image_type == "parent2":
                self.parent2_image = file_path
                self.parent2_face = face_img
                self.parent2_label.config(image=photo, text="")
                self.parent2_label.image = photo
                self.result_label.config(text="Parent 2 image loaded!" if face_img is not None else "No face detected in Parent 2!")

    def start_webcam(self):
        if not self.webcam_running:
            self.video_capture = cv2.VideoCapture(0)
            if not self.video_capture.isOpened():
                self.result_label.config(text="Error: Could not open webcam!")
                return
            self.webcam_running = True
            self.result_label.config(text="Webcam active! Face detection running...")
            self.update_webcam()
        else:
            self.stop_webcam()

    def stop_webcam(self):
        if self.video_capture:
            self.video_capture.release()
            self.video_capture = None
        self.webcam_running = False
        self.compare_label.config(image="", text="Webcam: Not active")
        self.result_label.config(text="Webcam stopped. Upload parent images to continue.")

    def update_webcam(self):
        if self.webcam_running and self.video_capture:
            ret, frame = self.video_capture.read()
            if ret:
                # Detect faces
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
                if len(faces) > 0:
                    (x, y, w, h) = faces[0]  # Use the first detected face
                    self.compare_face = frame[y:y+h, x:x+w]
                    # Draw rectangle around face
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                else:
                    self.compare_face = None

                # Convert frame to PIL Image for Tkinter
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                img = img.resize((150, 150), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.compare_label.config(image=photo, text="")
                self.compare_label.image = photo

            # Schedule next update
            self.root.after(50, self.update_webcam)

    def run_recognition(self):
        if not (self.parent1_image and self.parent2_image):
            self.result_label.config(text="Please upload both parent images!")
            return
        if not (self.parent1_face is not None and self.parent2_face is not None):
            self.result_label.config(text="No face detected in one or both parent images!")
            return
        if not self.webcam_running or self.compare_face is None:
            self.result_label.config(text="No face detected in webcam feed! Ensure webcam is active.")
            return

        # Compare faces using histogram correlation
        parent1_score = compare_histograms(self.parent1_face, self.compare_face)
        parent2_score = compare_histograms(self.parent2_face, self.compare_face)

        if parent1_score > parent2_score:
            result_text = f"You look most like Parent 1 with {parent1_score:.2f}% similarity!"
            highlight = "parent1"
        elif parent2_score > parent1_score:
            result_text = f"You look most like Parent 2 with {parent2_score:.2f}% similarity!"
            highlight = "parent2"
        else:
            result_text = "Equal resemblance to both parents!"
            highlight = None

        # Update UI and speak result
        self.result_label.config(text=result_text)
        try:
            self.engine.say(result_text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Text-to-speech error: {e}")

        # Highlight matched parent
        self.parent1_label.config(bg="#f0f0f0")
        self.parent2_label.config(bg="#f0f0f0")
        if highlight == "parent1":
            self.parent1_label.config(bg="#ffeb3b")
        elif highlight == "parent2":
            self.parent2_label.config(bg="#ffeb3b")

    def run(self):
        try:
            self.root.mainloop()
        finally:
            self.stop_webcam()  # Ensure webcam is released when window closes

    def __del__(self):
        self.stop_webcam()


if __name__ == '__main__':
    fr = FaceRecognition()
    fr.run()