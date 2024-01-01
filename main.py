import cv2, os
from ultralytics import YOLO
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.inference_running = False

        # Create a central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a vertical layout for the central widget
        layout = QVBoxLayout(central_widget)

        # Create a label to display the camera feed
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        # Create a horizontal layout for the buttons
        button_layout = QHBoxLayout()

        # Create a button to start the YOLOv8 inference
        self.start_button = QPushButton('Start YOLOv8 Inference', self)
        self.start_button.clicked.connect(self.start_inference)
        button_layout.addWidget(self.start_button)

        # Create a button to stop the YOLOv8 inference
        self.stop_button = QPushButton('Stop YOLOv8 Inference', self)
        self.stop_button.clicked.connect(self.stop_inference)
        self.stop_button.setEnabled(False)
        button_layout.addWidget(self.stop_button)

        # Create a button to exit the application
        self.exit_button = QPushButton('Exit', self)
        self.exit_button.clicked.connect(self.close)
        button_layout.addWidget(self.exit_button)

        # Add the button layout to the central layout
        layout.addLayout(button_layout)

        # Load the YOLOv8 model
        self.model = YOLO('yolov8n.pt')

        # Open the video capture device
        self.cap = cv2.VideoCapture(0)

        # Create a timer to update the camera feed
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(50)

    def start_inference(self):
        # Enable the stop button and disable the start button
        self.stop_button.setEnabled(True)
        self.start_button.setEnabled(False)

        # Start the YOLOv8 inference
        self.inference_running = True

    def stop_inference(self):
        # Disable the stop button and enable the start button
        self.stop_button.setEnabled(False)
        self.start_button.setEnabled(True)

        # Stop the YOLOv8 inference
        self.inference_running = False
        
    def play_audio_file(self):
        full_file_path = os.path.join(os.getcwd(), 'alert.mp3')
        url = QUrl.fromLocalFile(full_file_path)
        content = QMediaContent(url)

        self.player.setMedia(content)
        self.player.play()

    def update_frame(self):
        # Read a frame from the video capture device
        success, frame = self.cap.read()

        # List of harmful objects
        harmful_objects = [
            "knife", "gun", "scissors", "axe", "sword",
            "hammer", "chain saw", "wrench", "machete", "grenade"
        ]

        if success:
        # Run YOLOv8 inference on the frame
            if self.inference_running:
                results = self.model(frame)

                # Check if any harmful object is detected
                if results[0] in harmful_objects:
                    self.play_audio_file()

                annotated_frame = results[0].plot()
            else:
                annotated_frame = frame

            # Convert the frame to a QImage
            height, width, channel = annotated_frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(annotated_frame.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()

            # Set the QImage as the pixmap for the label
            self.label.setPixmap(QPixmap.fromImage(q_image))

    def closeEvent(self, event):
        # Release the video capture device
        self.cap.release()

        # Stop the timer
        self.timer.stop()

        # Call the parent closeEvent method
        super().closeEvent(event)

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
