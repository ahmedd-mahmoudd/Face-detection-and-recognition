
# Face Recognition Application

This is a PyQt5-based application that performs face recognition using the Deepface library. It allows users to load an input image and a database image, and then compares the faces in both images to determine if they match.

## Installation

1. Clone the repository:

    git clone https://github.com/ahmedd-mahmoudd/face-recognition-app.git

2. Install the required dependencies. Make sure you have Python 3(3.10.9) and pip installed, and then run:

    pip install -r requirements.txt

3. Run the application:

    python main.py

## Usage

1. When the application starts, a window will appear with two buttons: "Load Input Image" and "Load Database Image".

2. Click the "Load Input Image" button to select an input image file (.png or .jpg) from your local system.

3. Click the "Load Database Image" button to select a database image file (.png or .jpg) from your local system.

4. After selecting both images, click the "Compare" button to perform face recognition.

5. The application will display the input and database images side by side, with facial contours drawn on the images using Mediapipe.

6. The application will display the result of the face recognition process, indicating whether the faces in the two images match or not.

## Folder Structure

- `main.py`: The main script that initializes the application and connects the UI elements.
- `facerecognition.py`: The module that performs the face recognition.
- `GUI/`: A folder containing the application's icon (`icon.ico`).

## Dependencies

- Python 3
- PyQt5
- OpenCV (cv2)
- Mediapipe

## License

This project is licensed under the [MIT License](LICENSE).
