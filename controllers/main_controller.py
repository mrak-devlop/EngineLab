from pathlib import Path

from PySide6.QtWidgets import QFileDialog, QTreeWidgetItem

from parsers.nissan_datascan import NissanDataScanParser


class MainController:
    def __init__(self, window):
        self.window = window

        print("MainController initialized")

        self.window.open_action.triggered.connect(self.open_log)

        print("Signal connected")

    def open_log(self):
        print("open_log()")

        filename, _ = QFileDialog.getOpenFileName(
            parent=self.window,
            caption="Открыть лог",
            dir=".",
            filter="Log files (*.log);;All files (*.*)",
        )

        print(f"Selected file: {filename}")

        if not filename:
            print("Файл не выбран")
            return

        parser = NissanDataScanParser()

        session = parser.parse(Path(filename))

        self.window.set_session(session)

    # Пока оставляем здесь
    def fill_channels(self):
        self.window.channel_tree.clear()

        for channel in self.window.session.channels.values():
            item = QTreeWidgetItem([channel.name])
            self.window.channel_tree.addTopLevelItem(item)
