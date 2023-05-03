import cv2
import sqlite3
import numpy as np
from deepface import DeepFace

model = DeepFace.build_model("VGG-Face") 
print("The model has been built!")

# load the face from the database
conn = sqlite3.connect("face_data.db")
cursor = conn.cursor()
cursor.execute("SELECT face FROM faces WHERE faceID = 1")
face_bytes = cursor.fetchone()[0]
face = np.frombuffer(face_bytes, dtype=np.uint8)
face = cv2.imdecode(face, cv2.IMREAD_GRAYSCALE)

# load the test image and detect faces
test_image = cv2.imread("input\\Donald1.jpg")
detected_faces = DeepFace.detectFace(test_image)

# perform face recognition
for detected_face in detected_faces:
    # convert the detected face to grayscale and resize it
    detected_face = cv2.cvtColor(detected_face, cv2.COLOR_BGR2GRAY)
    detected_face = cv2.resize(detected_face, (100, 100))

    # compare the detected face with the face from the database
    result = DeepFace.verify(face, detected_face)

    # if the verification succeeds, print the name of the person
    if result["verified"]:
        print("This is the face of the person in the database.")
    else:
        print("This is not the face of the person in the database.")
