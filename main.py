from PyQt6.QtWidgets import QApplication, QFileDialog
from PyQt6.QtCore import QSettings
import sys
from TaskWindow import TaskWindow

if __name__ == "__main__":

    app = QApplication(sys.argv)

    # Load the last selected folder from the settings
    # If no folder was selected, prompt the user to select a folder
    # and save the selected folder to the settings
    settings = QSettings("TaskManager", "TaskManager")

    # This is the folder path where the tasks will be saved
    # Tasks and metadata will be saved to remember the window geometry
    # and the tasks that were added
    selected_folder = settings.value("selected_folder", defaultValue="")
    if not selected_folder:
        selected_folder = QFileDialog.getExistingDirectory()
        if selected_folder:
            settings.setValue("selected_folder", selected_folder)

    window = TaskWindow(selected_folder)
    app.aboutToQuit.connect(window.save_before_close)
    window.show()

    app.exec()
