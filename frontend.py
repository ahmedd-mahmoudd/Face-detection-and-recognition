import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from facerecognition import facerecognition

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'uploads')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/' )
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

    input_image_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(input_image.filename))
    database_image_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(database_image.filename))

    input_image.save(input_image_path)
    database_image.save(database_image_path)

    result = facerecognition(input_image_path, database_image_path)

    response = {'result': result}
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80 , debug=True)
