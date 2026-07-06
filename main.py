import sys

from PySide6.QtWidgets import QApplication

from controllers.main_controller import MainController
from gui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    window = MainWindow()

    controller = MainController(window)

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
