import os
import cv2
from deepface import DeepFace

model = DeepFace.build_model("VGG-Face") 
print("The model has been built!")

def facerecognition(input,database) :
    inputimg_path = input
    data_base_path = database


    inputimg = cv2.imread(inputimg_path)
    face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    face = face_detector.detectMultiScale(inputimg, scaleFactor=1.2, minNeighbors=6)

    output_path = os.path.join("output", os.path.basename(inputimg_path))


    for (x, y, w, h) in face:
        face_roi = inputimg[y:y+h+1 , x:x+w+1]

        cv2.imwrite(output_path, face_roi)

    print(inputimg_path, "\n" , data_base_path)

    result = DeepFace.verify(inputimg_path, data_base_path, enforce_detection=False)
    print(result)

    if result["verified"]:
        print("The faces match!")
        return True
    else:
        print("The faces do not match.")
        return False

if __name__ == "__main__":
    facerecognition("input\\obama.jpg","Database\\obama3.png")