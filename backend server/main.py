from flask import Flask, request, jsonify
import os
import base64
from pymongo import MongoClient
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import datetime
import bcrypt
from facerecognition import facerecognition


app = Flask(__name__)

secretKey = os.environ.get("SECRETKEY")
app.config['JWT_SECRET_KEY'] = secretKey  # Change this to your actual secret key
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=1)

jwt = JWTManager(app)
mongo_url = os.environ.get("MONGO_URL")
client = MongoClient(mongo_url)
try:
    if client.list_database_names():
        print("Connected to MongoDB successfully!")
except:
    print("Could not connect to MongoDB")
    exit()

db = client["mydatabase"]
users_collection = db["users"]

@app.route('/test')
def test():
    return jsonify({"status" : 'Server is up'}),200

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data['username']
    password = data['password']

    # Check if the username already exists in the database
    existing_user = users_collection.find_one({'username': username})
    if existing_user:
        return jsonify({'message': 'Username already exists.'}), 400

    # Hash the password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Insert the new user into the database
    user = {'username': username, 'password': hashed_password}
    users_collection.insert_one(user)

    return jsonify({'message': 'User registered successfully.'}), 201

@app.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    username = data['username']
    password = data['password']

    # Check if the username exists in the database
    existing_user = users_collection.find_one({'username': username})
    if not existing_user:
        return jsonify({'message': 'Invalid username or password.'}), 401

    # Verify the password using bcrypt
    if not bcrypt.checkpw(password.encode('utf-8'), existing_user['password']):
        return jsonify({'message': 'Invalid username or password.'}), 401

    # Generate an access token using Flask-JWT-Extended
    access_token = create_access_token(identity=username, expires_delta=datetime.timedelta(hours=1))

    return jsonify({'access_token': access_token}), 200


@app.route('/identify', methods=['GET'])
@jwt_required()
def protected_route():
    current_user = get_jwt_identity()

    return jsonify(message=f'Hello, {current_user}! You have access to this protected route.')


@app.route('/compare', methods=['POST'])
@jwt_required()  # Require a valid access token to access this route
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
    current_user = get_jwt_identity()
    print("\n" , "the current_user is :",current_user)

    # Call facerecognition function with the decoded images
    result = facerecognition(temp_image_path1, temp_image_path2)

    # Delete the temporary image files
    os.remove(temp_image_path1)
    os.remove(temp_image_path2)
    
    return jsonify({'result': result})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6000, debug=True)
