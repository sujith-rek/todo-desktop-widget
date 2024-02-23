from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QDialog,QFileDialog
import sys
import os
from task import TaskNote
import re
from TaskWindow import TaskWindow


app = QApplication(sys.argv)

# selected_folder = QFileDialog.getExistingDirectory()
selected_folder = "C:\\Users\\somas\\OneDrive\\Documents\\tasks"

window = TaskWindow(selected_folder)
app.aboutToQuit.connect(window.save_tasks)
window.show()

app.exec()
