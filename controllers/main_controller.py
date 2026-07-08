from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFileDialog

from gui.plot_manager import PlotManager
from models.cursor_mode import CursorMode
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

        self.plot_manager.marker_changed.connect(
            self.marker_changed,
        )

        self.current_index = -1

        self.cursor_mode = CursorMode.CURSOR

        self.window.cursor_mode_group.buttonClicked.connect(
            self.on_cursor_mode_changed,
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

        self.plot_manager.session = session

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

        if index == self.current_index:
            return

        self.current_index = index

        session = self.window.session

        if session is None:
            return

        values = session.values_at(index)

        for channel_name, value in values.items():
            self.window.info_panel.set_value(
                channel_name,
                value,
            )

    def on_cursor_mode_changed(self, button):

        if button is self.window.cursor_radio:
            self.cursor_mode = CursorMode.CURSOR

        elif button is self.window.marker_a_radio:
            self.cursor_mode = CursorMode.MARKER_A

        elif button is self.window.marker_b_radio:
            self.cursor_mode = CursorMode.MARKER_B

        self.plot_manager.set_cursor_mode(
            self.cursor_mode,
        )

        print(f"Cursor mode: {self.cursor_mode.name}")

    def marker_changed(self, measurements):

        self.window.measurements_panel.set_measurements(
            measurements,
        )
