import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QDialog
import sys
from task import TaskNote

class TaskWindow(QWidget):
    def __init__(self,folder_path):
        super().__init__()

        self.FILE_LOCATION = folder_path
        self.FILE_NAME = "tasks.txt"
        self.TASK_DELIMITER = "----------------------------------"
        self.META_DATA = "meta_data.txt"

        self.load_data()

        self.setWindowTitle("To-Do List")
        self.setGeometry(100, 100, 400, 400)

        self.layout = QVBoxLayout()


        add_button = QPushButton("Add Task")
        add_button.clicked.connect(self.add_task)
        self.layout.addWidget(add_button)

        save_button = QPushButton("Save Tasks")
        save_button.clicked.connect(self.save_tasks)
        self.layout.addWidget(save_button)

        self.init_task_notes()

        self.setLayout(self.layout)

    def load_data(self):
        self.tasks = self.load_file(self.FILE_NAME)
        self.meta = self.load_file(self.META_DATA)

    def load_file(self, filename):
        filepath = os.path.join(self.FILE_LOCATION, filename)
        if os.path.exists(filepath):
            with open(filepath, "r") as file:
                return file.read()
        else:
            with open(filepath, "w"):
                pass
            return ""

    def init_task_notes(self):
        self.task_notes = [TaskNote(task) for task in self.tasks.split(self.TASK_DELIMITER) if task]
        for task_note in self.task_notes:
            self.layout.addWidget(task_note)

    def add_task(self):
        task_note = TaskNote()
        self.task_notes.append(task_note)
        self.layout.addWidget(task_note)

    def save_tasks(self):
        def find_widgets(layout, widget_type):
            widgets = []
            for i in range(layout.count()):
                widget = layout.itemAt(i).widget()
                if isinstance(widget, widget_type):
                    widgets.append(widget)
            return widgets

        task_notes = find_widgets(self.layout, TaskNote)
        with open(os.path.join(self.FILE_LOCATION, self.FILE_NAME), "w") as file:
            file.write(self.TASK_DELIMITER.join([task.get_task() for task in task_notes if task.get_task()]))
