from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel

import sys

def clicked():
    print("clicked")

def initUI():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(200,200,300,300) # x, y, width, height
    win.setWindowTitle("My first window!")

    label = QLabel(win)
    label.setText("My first label!")
    label.move(50,50) # x, y from top left corner

    b1 = QtWidgets.QPushButton(win)
    b1.setText("Click me!")
    b1.clicked.connect(clicked)

    win.show()
    sys.exit(app.exec_())

main()
