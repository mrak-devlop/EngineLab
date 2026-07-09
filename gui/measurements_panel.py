from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
)

from models.measurement import Measurement


class MeasurementsPanel(QTableWidget):
    def __init__(self):
        super().__init__(0, 4)

        self.setHorizontalHeaderLabels(
            [
                "Channel",
                "Marker A",
                "Marker B",
                "Δ",
            ]
        )

        self.verticalHeader().hide()

        self.horizontalHeader().setStretchLastSection(True)

        self.horizontalHeader().setSectionResizeMode(
            0,
            QHeaderView.Stretch,
        )

        self.setEditTriggers(
            QTableWidget.NoEditTriggers,
        )

        self.setSelectionMode(
            QTableWidget.NoSelection,
        )

        self.setFocusPolicy(
            Qt.FocusPolicy.NoFocus,
        )

    @staticmethod
    def format_value(value):

        if value is None:
            return ""

        if isinstance(value, float):
            return f"{value:.2f}"

        return str(value)

    def set_measurements(
        self,
        measurements: list[Measurement],
    ):

        self.setRowCount(
            len(measurements),
        )

        for row, m in enumerate(measurements):
            self.setItem(
                row,
                0,
                QTableWidgetItem(
                    m.name,
                ),
            )

            self.setItem(
                row,
                1,
                QTableWidgetItem(
                    self.format_value(
                        m.value_a,
                    ),
                ),
            )

            self.setItem(
                row,
                2,
                QTableWidgetItem(
                    self.format_value(
                        m.value_b,
                    ),
                ),
            )

            self.setItem(
                row,
                3,
                QTableWidgetItem(
                    self.format_value(
                        m.delta,
                    ),
                ),
            )
