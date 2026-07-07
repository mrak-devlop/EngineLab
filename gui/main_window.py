import pyqtgraph as pg
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QMainWindow,
    QSplitter,
    QStatusBar,
)

from gui.channel_tree import ChannelTree
from gui.info_panel import InfoPanel
from gui.plot_area import PlotArea


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("EngineLab")
        self.resize(1600, 900)

        self.session = None

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

        self.channel_tree = ChannelTree()

        self.plot_area = PlotArea()

        self.info_panel = InfoPanel()

        splitter.addWidget(self.channel_tree)
        splitter.addWidget(self.plot_area)
        splitter.addWidget(self.info_panel)

        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setStretchFactor(2, 0)

        self.setStatusBar(QStatusBar())

    def set_session(self, session):

        self.session = session

        self.channel_tree.set_channels(session.channels)

        self.info_panel.set_channels(session.channels)
