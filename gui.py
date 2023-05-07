import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QFileDialog, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from facerecognition import facerecognition
import mediapipe as mp


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Face Recognition")
        self.setGeometry(100, 100, 800, 400)

        # Create widgets
        self.input_button = QPushButton("Load Input Image", self)
        self.input_button.clicked.connect(self.load_input_image)

        self.database_button = QPushButton("Load Database Image", self)
        self.database_button.clicked.connect(self.load_database_image)

        self.compare_button = QPushButton("Compare", self)
        self.compare_button.clicked.connect(self.run_facerecognition)

        self.input_label = QLabel(self)
        self.input_label.setFixedSize(400, 400)

        self.database_label = QLabel(self)
        self.database_label.setFixedSize(400, 400)

        self.result_label = QLabel(self)
        self.result_label.setAlignment(Qt.AlignCenter)

        # Layout widgets
        image_layout = QHBoxLayout()
        image_layout.addWidget(self.input_label)
        image_layout.addWidget(self.database_label)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.input_button)
        button_layout.addWidget(self.database_button)
        button_layout.addWidget(self.compare_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(image_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.result_label)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def load_input_image(self):
        input_file, _ = QFileDialog.getOpenFileName(self, "Open Input Image", "", "Image Files (*.png *.jpg)")
        self.input_file = input_file
        if input_file:
            self.display_image(self.input_label, input_file,2)

    def load_database_image(self):
        database_file, _ = QFileDialog.getOpenFileName(self, "Open Database Image", "", "Image Files (*.png *.jpg)")
        self.database_file = database_file
        if database_file:
            self.display_image(self.database_label, database_file,1)

    def run_facerecognition(self):
        if hasattr(self, "input_file") and hasattr(self, "database_file"):
            result = facerecognition(self.input_file, self.database_file)
            if result:
                self.result_label.setText("The faces match!")
                self.result_label.setStyleSheet("color: green;")
            else:
                self.result_label.setText("The faces do not match.")
                self.result_label.setStyleSheet("color: red;")
        else:
            self.result_label.setText("Please select both input and database images.")
            self.result_label.setStyleSheet("color: black;")

    def display_image(self, label, image_path,x):
        image = cv2.imread(image_path)
        facemesh_image = self.apply_facemesh(image,x)
        height, width, channel = facemesh_image.shape
        bytes_per_line = 3 * width
        q_image = QImage(facemesh_image.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(q_image)
        label.setPixmap(pixmap.scaled(label.size(), aspectRatioMode=1))

    def apply_facemesh(self, image,x):
        mp_drawing = mp.solutions.drawing_utils
        mp_face_mesh = mp.solutions.face_mesh

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        with mp_face_mesh.FaceMesh(static_image_mode=True) as face_mesh:
            results = face_mesh.process(image_rgb)

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    for idx, connection in enumerate(mp_face_mesh.FACEMESH_TESSELATION):
                        if idx % 3 != 0:
                            continue
                        point1 = face_landmarks.landmark[connection[0]]
                        point2 = face_landmarks.landmark[connection[1]]
                        x1, y1 = int(point1.x * image.shape[1]), int(point1.y * image.shape[0])
                        x2, y2 = int(point2.x * image.shape[1]), int(point2.y * image.shape[0])
                        cv2.line(image, (x1, y1), (x2, y2), (100, 100, 100), x)

        return image



