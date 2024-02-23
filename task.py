from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QLabel, QCheckBox, QLineEdit, QHBoxLayout

class TaskNote(QWidget):

    def __init__(self, task=""):
        super().__init__()

        self.CHECK_DELIMITER = "!@#"
        self.task = task
        self.checked = 0
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout()

        self.task_layout = QHBoxLayout()

        self.check_box = QCheckBox()
        self.label = QLabel(self.extract_task_label())
        self.check_box.setChecked(self.extract_checked_status())
        self.task_layout.addWidget(self.check_box)
        self.task_layout.addWidget(self.label)

        self.layout.addLayout(self.task_layout)

        self.edit_button = QPushButton("Edit")
        self.layout.addWidget(self.edit_button)

        self.edit_data = QLineEdit()
        self.layout.addWidget(self.edit_data)
        self.edit_data.hide()

        self.edit_button.clicked.connect(self.toggle_edit)

        self.check_box.stateChanged.connect(self.mark_complete)
        self.setLayout(self.layout)

    def extract_task_label(self):
        parts = self.task.split(self.CHECK_DELIMITER)
        if len(parts) > 1:
            self.checked = int(parts[1])
            return parts[2]
        return ""

    def extract_checked_status(self):
        return self.checked == 1

    def mark_complete(self):
        self.checked = 1 if self.check_box.isChecked() else 0

    def toggle_edit(self):
        if self.edit_button.text() == "Edit":
            self.start_editing()
        else:
            self.save_task()

    def start_editing(self):
        self.edit_data.setText(self.label.text())
        self.label.hide()
        self.edit_data.show()
        self.edit_button.setText("Save")
        self.edit_button.clicked.disconnect(self.toggle_edit)
        self.edit_button.clicked.connect(self.save_task)

    def save_task(self):
        self.label.setText(self.edit_data.text())
        self.edit_data.hide()
        self.label.show()
        self.edit_button.setText("Edit")
        self.edit_button.clicked.disconnect(self.save_task)
        self.edit_button.clicked.connect(self.toggle_edit)

    def get_task(self):
        return f"{self.CHECK_DELIMITER}{self.checked}{self.CHECK_DELIMITER}{self.label.text()}"
