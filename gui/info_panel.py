from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
)


class InfoPanel(QTableWidget):
    def __init__(self):
        super().__init__(0, 2)

        self.setHorizontalHeaderLabels(["Канал", "Значение"])

        self.verticalHeader().hide()

        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setSectionResizeMode(
            0,
            QHeaderView.ResizeToContents,
        )

        self.setEditTriggers(QTableWidget.NoEditTriggers)

        self.setSelectionMode(QTableWidget.NoSelection)

        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def clear_channels(self):

        self.setRowCount(0)

    def set_channels(self, channels):

        self.setRowCount(0)

        for channel in channels.values():
            row = self.rowCount()

            self.insertRow(row)

            self.setItem(
                row,
                0,
                QTableWidgetItem(channel.name),
            )

            self.setItem(
                row,
                1,
                QTableWidgetItem("-----"),
            )

    def set_value(self, channel_name, value):

        for row in range(self.rowCount()):
            if self.item(row, 0).text() != channel_name:
                continue

            self.item(row, 1).setText(str(value))

            return
