from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QMainWindow,
    QSplitter,
    QStatusBar,
    QTreeWidget,
    QTreeWidgetItem,
)

from gui.plot_area import PlotArea


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.session = None

        self.setWindowTitle("EngineLab")

        self.resize(1600, 900)

        self.create_menu()

        self.create_ui()

    def create_menu(self):

        menu = self.menuBar()

        file_menu = menu.addMenu("Файл")

        self.open_action = QAction("Открыть лог...", self)

        file_menu.addAction(self.open_action)

        file_menu.addSeparator()

        self.exit_action = QAction("Выход", self)

        file_menu.addAction(self.exit_action)

        self.exit_action.triggered.connect(self.close)

    def create_ui(self):

        splitter = QSplitter(Qt.Horizontal)

        self.setCentralWidget(splitter)

        self.channel_tree = QTreeWidget()

        self.channel_tree.setHeaderLabel("Каналы")

        self.plot_area = PlotArea()

        splitter.addWidget(self.channel_tree)

        splitter.addWidget(self.plot_area)

        splitter.setStretchFactor(1, 1)

        self.setStatusBar(QStatusBar())

    def set_session(self, session):

        self.session = session

        self.channel_tree.clear()

        for channel in session.channels.values():
            self.channel_tree.addTopLevelItem(QTreeWidgetItem([channel.name]))

        self.statusBar().showMessage(f"{session.name} | {len(session.timestamps)} samples")
