from PyQt6.QtWidgets import QApplication, QFileDialog
from PyQt6.QtCore import QSettings
import sys
from TaskWindow import TaskWindow

app = QApplication(sys.argv)

settings = QSettings("MyCompany", "MyApp")

selected_folder = settings.value("selected_folder", defaultValue="")
if not selected_folder:
    selected_folder = QFileDialog.getExistingDirectory()
    if selected_folder:
        settings.setValue("selected_folder", selected_folder)

window = TaskWindow(selected_folder)
app.aboutToQuit.connect(window.save_before_close)
window.show()

app.exec()
