import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QFileDialog, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from facerecognition import facerecognition

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Face Recognition")
        self.setGeometry(100, 100, 800, 400)

        self.input_button = QPushButton("Load Input Image", self)
        self.input_button.clicked.connect(self.load_input_image)

        self.database_button = QPushButton("Load Database Image", self)
        self.database_button.clicked.connect(self.load_database_image)

        self.compare_button = QPushButton("Compare", self)
        self.compare_button.clicked.connect(self.run_facerecognition)

        self.input_label = QLabel(self)
        self.input_label.setFixedSize(200, 200)

        self.database_label = QLabel(self)
        self.database_label.setFixedSize(200, 200)

        self.result_label = QLabel(self)
        self.result_label.setAlignment(Qt.AlignCenter)

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
            pixmap = QPixmap(input_file)
            self.input_label.setPixmap(pixmap.scaled(self.input_label.size(), aspectRatioMode=1))

    def load_database_image(self):
        database_file, _ = QFileDialog.getOpenFileName(self, "Open Database Image", "", "Image Files (*.png *.jpg)")
        self.database_file = database_file
        if database_file:
            pixmap = QPixmap(database_file)
            self.database_label.setPixmap(pixmap.scaled(self.database_label.size(), aspectRatioMode=1))

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
