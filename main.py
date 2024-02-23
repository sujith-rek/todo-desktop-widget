from PyQt6.QtWidgets import QApplication
import sys
from TaskWindow import TaskWindow


app = QApplication(sys.argv)

# selected_folder = QFileDialog.getExistingDirectory()
selected_folder = "C:\\Users\\somas\\OneDrive\\Documents\\tasks"

window = TaskWindow(selected_folder)
app.aboutToQuit.connect(window.save_before_close)
window.show()

app.exec()
