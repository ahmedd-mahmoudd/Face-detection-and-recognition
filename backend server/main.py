from flask import Flask, request, jsonify
import os
import base64
from facerecognition import facerecognition
from werkzeug.utils import secure_filename
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
import bcrypt


app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/your_database_name'
app.config['SECRET_KEY'] = 'your_secret_key'
mongo = PyMongo(app)
#confirm the mongoDB connection
print(mongo.db)

@app.route('/test')
def test():
    return 'Server is up'

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data['username']
    password = data['password']

    # Check if the username already exists in the database
    existing_user = mongo.db.users.find_one({'username': username})
    if existing_user:
        return jsonify({'message': 'Username already exists.'}), 400

    # Hash the password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Insert the new user into the database
    user = {'username': username, 'password': hashed_password}
    mongo.db.users.insert_one(user)

    return jsonify({'message': 'User registered successfully.'}), 201


@app.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    username = data['username']
    password = data['password']

    # Check if the username exists in the database
    existing_user = mongo.db.users.find_one({'username': username})
    if not existing_user:
        return jsonify({'message': 'Invalid username or password.'}), 401

    # Verify the password using bcrypt
    if not check_password_hash(existing_user['password'], password):
        return jsonify({'message': 'Invalid username or password.'}), 401

    # Generate a JWT token
    token = jwt.encode({'username': username, 'exp': datetime.utcnow() + timedelta(days=1)}, app.config['SECRET_KEY'])

    return jsonify({'token': token}), 200


@app.route('/compare', methods=['POST'])
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
