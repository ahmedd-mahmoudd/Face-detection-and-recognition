import os
import base64
from flask import Flask, render_template, request, jsonify
import requests
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'uploads')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compare', methods=['POST'])
def compare_images():
    if 'input_image' not in request.files or 'database_image' not in request.files:
        return jsonify({'error': 'Input image and database image are required.'}), 400

    input_image = request.files['input_image']
    database_image = request.files['database_image']

    if not allowed_file(input_image.filename) or not allowed_file(database_image.filename):
        return jsonify({'error': 'Invalid file format. Only PNG and JPEG images are allowed.'}), 400

    input_image_data = input_image.read()
    database_image_data = database_image.read()

    input_image_base64 = base64.b64encode(input_image_data).decode('utf-8')
    database_image_base64 = base64.b64encode(database_image_data).decode('utf-8')

    data = {
        'image1': input_image_base64,
        'image2': database_image_base64
    }

    response = requests.post('http://192.168.3.15:5000', json=data)
    result = response.json().get('result')

    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
