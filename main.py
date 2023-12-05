import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('yolov8n.pt')

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window title
        self.setWindowTitle("YOLOv8 Tracking")

        # Create a QLabel widget to display the annotated frame
        self.label = QLabel()
        self.setCentralWidget(self.label)

        # Open the webcam
        self.cap = cv2.VideoCapture(0) # Use 0 for the default webcam, or 1, 2, etc. for other webcams

        # Create a QTimer to update the QLabel with the webcam frames
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(20) # Update every 20 ms

    def update_frame(self):
        # Read a frame from the webcam
        success, frame = self.cap.read()

        if success:
            # Run YOLOv8 tracking on the frame, persisting tracks between frames
            results = model.track(frame, persist=True)

            # Visualize the results on the frame
            annotated_frame = results[0].plot()

            # Convert the frame to QImage format
            height, width, channel = annotated_frame.shape
            bytes_per_line = 3 * width
            qimg = QImage(annotated_frame.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()

            # Display the QImage on the QLabel
            self.label.setPixmap(QPixmap.fromImage(qimg))
        else:
            # Break the loop if the webcam is disconnected
            self.timer.stop()
            self.cap.release()

# Create an instance of QApplication
app = QApplication(sys.argv)

# Create an instance of MainWindow
window = MainWindow()
window.show()

# Start the event loop
sys.exit(app.exec_())
