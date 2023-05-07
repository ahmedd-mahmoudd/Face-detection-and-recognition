import os
import cv2
import sqlite3
from PIL import Image


def detect_faces(input_image_path):

    inputimg = Image.open(input_image_path)

    input_image = cv2.imread(input_image_path)

    face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    faces = face_detector.detectMultiScale(input_image, scaleFactor=1.2, minNeighbors=6)

    # remove the face2.jpg if exists
    inputfilename = os.path.basename(input_image_path)
    outputfilepath = f"Database\\{inputfilename}"
    if os.path.isfile(outputfilepath):
        os.remove(outputfilepath)
    for (x, y, w, h) in faces:
        face_roi = input_image[y:y+h, x:x+w]
        cv2.imwrite(outputfilepath, face_roi)

    face = cv2.imread(outputfilepath)
    face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
    face = cv2.resize(face, (100, 100))
    cv2.imwrite(outputfilepath, face)

    conn = sqlite3.connect("face_data.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS faces(faceID TEXT PRIMARY KEY, face BLOB)")
    cmd = "SELECT * FROM faces WHERE faceID = 1"
    cursor = conn.execute(cmd)
    isRecordExist = 0
    for row in cursor:
        isRecordExist = 1
    if isRecordExist == 1:
        cmd = "UPDATE faces SET face = (?) WHERE faceID = 1"
    else:
        cmd = "INSERT INTO faces (faceID, face) VALUES (1, ?)"
    with open(outputfilepath, 'rb') as f:
        data = f.read()
    conn.execute(cmd, (data,))
    conn.commit()
    conn.close()

    if __name__ != "__main__":
        return outputfilepath


if __name__ == "__main__":
    detect_faces("input\\liam hemsworth.jpg")
