import os
from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QScrollArea, QApplication
from PyQt6.QtCore import Qt
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

        # Set initial geometry or use defaults
        self.ax, self.ay, self.awidth, self.aheight = map(
            int, self.meta.split(self.META_DELIMITER)) if self.meta else (100, 100, 400, 400)

        # Create the main layout
        main_layout = QVBoxLayout(self)

        # Create a layout for the fixed content
        self.h_layout = QHBoxLayout()
        add_button = QPushButton("Add Task")
        add_button.clicked.connect(self.add_task)
        self.h_layout.addWidget(add_button)

        save_button = QPushButton("Save Tasks")
        save_button.clicked.connect(self.save_tasks)
        self.h_layout.addWidget(save_button)

        # Add the fixed layout to the main layout
        main_layout.addLayout(self.h_layout)

        # Create a layout for the scrollable content
        self.layout = QVBoxLayout()

        style_sheet = """
            QScrollArea {
                border: none;
            }
        """

        # Create a scroll area and set the scrollable layout as its widget
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        scrollable_widget = QWidget()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        scrollable_widget.setLayout(self.layout)
        self.scroll_area.setWidget(scrollable_widget)
        self.scroll_area.setStyleSheet(style_sheet)

        # Add the scroll area to the main layout
        main_layout.addWidget(self.scroll_area)

        # Set the main layout of the window
        self.setLayout(main_layout)

        self.init_task_notes()

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
        self.task_notes = [TaskNote(task, self.delete_task_note) for task in self.tasks.split(
            self.TASK_DELIMITER) if task]
        for task_note in self.task_notes:
            self.layout.addWidget(task_note)

        self.adjust_window_size()

    def delete_task_note(self, task_note):
        self.layout.removeWidget(task_note)
        task_note.deleteLater()
        self.task_notes.remove(task_note)
        self.adjust_window_size()

    def adjust_window_size(self):
        screen_geometry = QApplication.primaryScreen().geometry()

        # Ensure window size is within screen size
        if self.aheight > screen_geometry.height():
            self.aheight = screen_geometry.height()

        if self.awidth > screen_geometry.width():
            self.awidth = screen_geometry.width()

        # Set new geometry
        self.setGeometry(self.ax, self.ay, self.awidth, self.aheight)

    def add_task(self):
        task_note = TaskNote(delete_callback=self.delete_task_note)
        self.task_notes.append(task_note)
        self.layout.addWidget(task_note)
        self.adjust_window_size()

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
