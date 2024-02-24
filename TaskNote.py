from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QCheckBox, QTextEdit, QHBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt

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
        self.text_edit = QTextEdit(self.extract_task_label())
        self.text_edit.setReadOnly(True)

        # Set size policy for text edit to allow vertical expansion
        self.text_edit.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

        # Show the scrollbar even in read-only mode
        self.text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.text_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Set a style sheet to make QTextEdit look like a label
        style_sheet = """
            QTextEdit {
                border: none;
                background-color: transparent;
                color: black;
            }
        """
        self.text_edit.setStyleSheet(style_sheet)

        self.check_box.setChecked(self.extract_checked_status())

        checkbox_fixed_width = int(self.width() * 0.1)
        self.check_box.setFixedWidth(checkbox_fixed_width)

        self.task_layout.addWidget(self.check_box)
        self.task_layout.addWidget(self.text_edit)

        self.layout.addLayout(self.task_layout)

        self.edit_button = QPushButton("Edit")
        self.layout.addWidget(self.edit_button)

        self.edit_button.clicked.connect(self.toggle_edit)
        self.check_box.stateChanged.connect(self.mark_complete)

        self.setLayout(self.layout)

    def on_resize(self, width, height):
        self.text_edit.setFixedWidth(width - int(width * 0.1))
        self.check_box.setFixedWidth(int(width * 0.1))

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
        # Change style for editing
        style_sheet_editing = """
            QTextEdit {
                border: 1px solid gray;
                background-color: white;
                color: black;
            }
        """
        self.text_edit.setStyleSheet(style_sheet_editing)
        self.text_edit.setReadOnly(False)
        self.edit_button.setText("Save")
        self.edit_button.clicked.disconnect(self.toggle_edit)
        self.edit_button.clicked.connect(self.save_task)

    def save_task(self):
        # Restore original style after saving
        style_sheet_original = """
            QTextEdit {
                border: none;
                background-color: transparent;
                color: black;
            }
        """
        self.text_edit.setStyleSheet(style_sheet_original)
        new_text = self.text_edit.toPlainText()
        self.text_edit.setReadOnly(True)
        self.edit_button.setText("Edit")
        self.edit_button.clicked.disconnect(self.save_task)
        self.edit_button.clicked.connect(self.toggle_edit)

    def get_task(self):
        return f"{self.CHECK_DELIMITER}{self.checked}{self.CHECK_DELIMITER}{self.text_edit.toPlainText()}"
