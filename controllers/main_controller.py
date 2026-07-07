from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFileDialog

from gui.plot_manager import PlotManager
from parsers.nissan_datascan import NissanDataScanParser


class MainController:
    def __init__(self, window):

        self.window = window

        self.plot_manager = PlotManager(
            window.plot_area,
        )

        #
        # Сигналы
        #

        self.window.open_action.triggered.connect(
            self.open_log,
        )

        self.window.channel_tree.itemChanged.connect(
            self.channels_changed,
        )

        self.plot_manager.plot_closed.connect(
            self.plot_closed,
        )

        self.plot_manager.cursor_moved.connect(
            self.cursor_moved,
        )

    def open_log(self):

        filename, _ = QFileDialog.getOpenFileName(
            self.window,
            "Открыть лог",
            ".",
            "Log files (*.log);;All files (*.*)",
        )

        if not filename:
            return

        parser = NissanDataScanParser()

        session = parser.parse(Path(filename))

        self.window.set_session(session)

        self.plot_manager.clear()

    def channels_changed(self, item):

        if self.window.session is None:
            return

        channel = item.data(0, Qt.UserRole)

        if channel is None:
            return

        if item.checkState(0) == Qt.Checked:
            self.plot_manager.show_channel(
                self.window.session.timestamps,
                channel,
            )

        else:
            self.plot_manager.hide_channel(channel)

    def plot_closed(self, channel_name: str):

        self.window.channel_tree.set_channel_checked(
            channel_name,
            False,
        )

    def cursor_moved(self, index: int):

        session = self.window.session

        if session is None:
            return

        values = session.values_at(index)

        for channel_name, value in values.items():
            self.window.info_panel.set_value(
                channel_name,
                value,
            )
