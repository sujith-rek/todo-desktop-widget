import os
from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QHBoxLayout
from TaskNote import TaskNote


class TaskWindow(QWidget):
    def __init__(self, folder_path):
        super().__init__()

        self.FILE_LOCATION = folder_path
        self.FILE_NAME = "tasks.txt"
        self.TASK_DELIMITER = "(*_*)(^_^)(*_*)"
        self.META_DELIMITER = "(>_<)(-_-)"
        self.META_DATA = "meta_data.txt"

        self.load_data()

        self.setWindowTitle("To-Do List")

        if self.meta:
            self.ax, self.ay, self.awidth, self.aheight = map(
                int, self.meta.split(self.META_DELIMITER))
            self.setGeometry(self.ax, self.ay, self.awidth, self.aheight)
        else:
            self.setGeometry(100, 100, 400, 400)

        self.layout = QVBoxLayout()

        self.h_layout = QHBoxLayout()

        add_button = QPushButton("Add Task")
        add_button.clicked.connect(self.add_task)
        self.h_layout.addWidget(add_button)

        save_button = QPushButton("Save Tasks")
        save_button.clicked.connect(self.save_tasks)
        self.h_layout.addWidget(save_button)

        self.layout.addLayout(self.h_layout)

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
        self.task_notes = [TaskNote(task) for task in self.tasks.split(
            self.TASK_DELIMITER) if task]
        for task_note in self.task_notes:
            self.layout.addWidget(task_note)

    def add_task(self):
        task_note = TaskNote()
        self.task_notes.append(task_note)
        self.layout.addWidget(task_note)

    def save_before_close(self):
        self.save_meta()
        self.save_tasks()

    def save_meta(self):
        self.ax = self.geometry().x()
        self.ay = self.geometry().y()
        self.awidth = self.geometry().width()
        self.aheight = self.geometry().height()

        with open(os.path.join(self.FILE_LOCATION, self.META_DATA), "w") as file:
            file.write(
                f"{self.ax}{self.META_DELIMITER}{self.ay}{self.META_DELIMITER}{self.awidth}{self.META_DELIMITER}{self.aheight}")

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
            file.write(self.TASK_DELIMITER.join(
                [task.get_task() for task in task_notes if task.get_task()]))
