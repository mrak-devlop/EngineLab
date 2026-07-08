from PySide6.QtWidgets import (
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from models.measurement import Measurement


class MeasurementsPanel(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.table = QTableWidget()

        self.table.setColumnCount(4)

        self.table.setHorizontalHeaderLabels(
            [
                "Channel",
                "Marker A",
                "Marker B",
                "Δ",
            ]
        )

        self.table.horizontalHeader().setStretchLastSection(True)

        self.table.horizontalHeader().setSectionResizeMode(
            0,
            QHeaderView.Stretch,
        )

        layout.addWidget(self.table)

    def set_measurements(
        self,
        measurements: list[Measurement],
    ):

        self.table.setRowCount(
            len(measurements),
        )

        for row, m in enumerate(measurements):
            self.table.setItem(
                row,
                0,
                QTableWidgetItem(m.name),
            )

            self.table.setItem(
                row,
                1,
                QTableWidgetItem(str(m.value_a)),
            )

            self.table.setItem(
                row,
                2,
                QTableWidgetItem(str(m.value_b)),
            )

            self.table.setItem(
                row,
                3,
                QTableWidgetItem(str(m.delta)),
            )
