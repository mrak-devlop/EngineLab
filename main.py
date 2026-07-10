import sys

from PySide6.QtWidgets import QApplication

from controllers.main_controller import MainController
from gui.main_window import MainWindow


def main():

    if sys.platform == "win32":
        import ctypes

        myappid = "kitfactory.enginelab.main.v1.0alpha"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    app = QApplication(sys.argv)

    window = MainWindow()

    controller = MainController(window)

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
