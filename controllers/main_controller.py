from pathlib import Path

from PySide6.QtWidgets import QFileDialog

from parsers.nissan_datascan import NissanDataScanParser


class MainController:
    def __init__(self, window):

        self.window = window

        self.window.open_action.triggered.connect(self.open_log)

        self.window.channel_tree.itemSelectionChanged.connect(self.channel_selected)

    def open_log(self):

        filename, _ = QFileDialog.getOpenFileName(self.window, "Открыть лог", ".", "Log (*.log)")

        if not filename:
            return

        parser = NissanDataScanParser()

        session = parser.parse(Path(filename))

        self.window.set_session(session)

    def channel_selected(self):

        if self.window.session is None:
            return

        item = self.window.channel_tree.currentItem()

        if item is None:
            return

        name = item.text(0)

        channel = self.window.session[name]

        self.window.plot.plot_channel(
            self.window.session.timestamps,
            channel.values,
            channel.name,
        )
