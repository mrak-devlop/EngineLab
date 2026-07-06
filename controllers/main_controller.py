from pathlib import Path

from PySide6.QtWidgets import QFileDialog

from gui.plot_manager import PlotManager
from parsers.nissan_datascan import NissanDataScanParser


class MainController:
    def __init__(self, window):

        self.window = window

        self.plot_manager = PlotManager(window.plot_area)

        self.window.open_action.triggered.connect(self.open_log)

        self.window.channel_tree.itemSelectionChanged.connect(self.channel_selected)

    def open_log(self):

        filename, _ = QFileDialog.getOpenFileName(self.window, "Открыть лог", ".", "Log (*.log)")

        if not filename:
            return

        parser = NissanDataScanParser()

        session = parser.parse(Path(filename))

        self.window.set_session(session)

        self.plot_manager.clear()

    def channel_selected(self):

        if self.window.session is None:
            return

        item = self.window.channel_tree.currentItem()

        if item is None:
            return

        self.plot_manager.show_channel(
            self.window.session,
            item.text(0),
        )
