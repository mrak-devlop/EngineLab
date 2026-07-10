from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QButtonGroup,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QRadioButton,
    QSplitter,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)

from gui.channel_tree import ChannelTree
from gui.info_panel import InfoPanel
from gui.measurements_panel import MeasurementsPanel
from gui.plot_area import PlotArea


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("EngineLab")
        self.resize(1500, 800)

        self.session = None

        self.create_menu()
        self.create_ui()

    def create_menu(self):

        menu = self.menuBar()

        file_menu = menu.addMenu("Файл")

        self.open_action = QAction(
            "Открыть лог...",
            self,
        )

        file_menu.addAction(
            self.open_action,
        )

        file_menu.addSeparator()

        self.exit_action = QAction(
            "Выход",
            self,
        )

        file_menu.addAction(
            self.exit_action,
        )

        self.exit_action.triggered.connect(
            self.close,
        )

    def create_ui(self):

        splitter = QSplitter(
            Qt.Horizontal,
        )

        self.setCentralWidget(
            splitter,
        )

        #
        # Левая панель
        #

        self.channel_tree = ChannelTree()

        #
        # Центральная панель
        #

        self.plot_area = PlotArea()

        plot_container = QWidget()

        plot_layout = QVBoxLayout(
            plot_container,
        )

        plot_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        plot_layout.setSpacing(
            2,
        )

        #
        # Панель режимов курсора
        #

        mode_layout = QHBoxLayout()

        self.cursor_radio = QRadioButton(
            "Курсор",
        )

        self.marker_a_radio = QRadioButton(
            "Точка A",
        )

        self.marker_b_radio = QRadioButton(
            "Точка B",
        )

        self.cursor_radio.setChecked(
            True,
        )

        self.cursor_mode_group = QButtonGroup(
            self,
        )

        self.cursor_mode_group.addButton(
            self.cursor_radio,
        )

        self.cursor_mode_group.addButton(
            self.marker_a_radio,
        )

        self.cursor_mode_group.addButton(
            self.marker_b_radio,
        )

        mode_layout.addWidget(
            self.cursor_radio,
        )

        mode_layout.addWidget(
            self.marker_a_radio,
        )

        mode_layout.addWidget(
            self.marker_b_radio,
        )

        self.zoom_markers_button = QPushButton("Zoom A-B")
        self.reset_zoom_button = QPushButton("Reset zoom")

        mode_layout.addWidget(self.zoom_markers_button)
        mode_layout.addWidget(self.reset_zoom_button)

        mode_layout.addStretch()

        plot_layout.addLayout(
            mode_layout,
        )

        plot_layout.addWidget(
            self.plot_area,
        )

        #
        # Правая панель
        #

        self.info_panel = InfoPanel()

        self.measurements_panel = MeasurementsPanel()

        self.info_panel.setMinimumHeight(
            180,
        )

        self.measurements_panel.setMinimumHeight(
            180,
        )

        right_splitter = QSplitter(
            Qt.Vertical,
        )

        right_splitter.addWidget(
            self.info_panel,
        )

        right_splitter.addWidget(
            self.measurements_panel,
        )

        right_splitter.setStretchFactor(
            0,
            1,
        )

        right_splitter.setStretchFactor(
            1,
            1,
        )

        right_splitter.setSizes(
            [
                450,
                450,
            ]
        )

        right_splitter.setChildrenCollapsible(
            False,
        )

        #
        # Основной splitter
        #

        splitter.addWidget(
            self.channel_tree,
        )

        splitter.addWidget(
            plot_container,
        )

        splitter.addWidget(
            right_splitter,
        )

        splitter.setStretchFactor(
            0,
            0,
        )

        splitter.setStretchFactor(
            1,
            1,
        )

        splitter.setStretchFactor(
            2,
            0,
        )

        splitter.setSizes(
            [
                260,
                1050,
                420,
            ]
        )

        self.setStatusBar(
            QStatusBar(),
        )

    def set_session(self, session):

        self.session = session

        self.channel_tree.set_channels(
            session.channels,
        )

        self.info_panel.set_channels(
            session.channels,
        )
