from flask import Flask, request, jsonify
import os
import base64
from facerecognition import facerecognition

app = Flask(__name__)

@app.route('/', methods=['POST'])
def face_recognition():
    data = request.get_json()
    image1 = data['image1']
    image2 = data['image2']

    # Decode the base64-encoded images
    image_data1 = base64.b64decode(image1)
    image_data2 = base64.b64decode(image2)

    # Create the temp directory if it doesn't exist
    temp_dir = "temp"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    # Save the decoded images temporarily
    temp_image_path1 = os.path.join(temp_dir, "image1.jpg")
    temp_image_path2 = os.path.join(temp_dir, "image2.jpg")
    with open(temp_image_path1, 'wb') as f1, open(temp_image_path2, 'wb') as f2:
        f1.write(image_data1)
        f2.write(image_data2)

    # Call facerecognition function with the decoded images
    result = facerecognition(temp_image_path1, temp_image_path2)

    # Delete the temporary image files
    os.remove(temp_image_path1)
    os.remove(temp_image_path2)

    return jsonify({'result': result})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
