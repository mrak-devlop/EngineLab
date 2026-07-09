from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
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
    def format_value(
        value,
        signed=False,
    ):

        if value is None:
            return ""

        if isinstance(value, float):
            if signed:
                return f"{value:+.2f}"

            return f"{value:.2f}"

        if isinstance(value, int):
            if signed:
                return f"{value:+d}"

            return str(value)

        return str(value)

    def set_measurements(
        self,
        measurements: list[Measurement],
    ):

        self.setRowCount(
            len(measurements),
        )

        for row, m in enumerate(measurements):
            #
            # Channel
            #

            item = QTableWidgetItem(
                m.name,
            )

            item.setTextAlignment(
                Qt.AlignVCenter | Qt.AlignLeft,
            )

            self.setItem(
                row,
                0,
                item,
            )

            #
            # Marker A
            #

            item = QTableWidgetItem(
                self.format_value(
                    m.value_a,
                ),
            )

            item.setTextAlignment(
                Qt.AlignVCenter | Qt.AlignRight,
            )

            self.setItem(
                row,
                1,
                item,
            )

            #
            # Marker B
            #

            item = QTableWidgetItem(
                self.format_value(
                    m.delta,
                    signed=True,
                ),
            )

            item.setTextAlignment(
                Qt.AlignVCenter | Qt.AlignRight,
            )

            self.setItem(
                row,
                2,
                item,
            )

            #
            # Delta
            #

            item = QTableWidgetItem(
                self.format_value(
                    m.delta,
                ),
            )

            item.setTextAlignment(
                Qt.AlignVCenter | Qt.AlignRight,
            )

            if m.delta is not None:
                if m.delta > 0:
                    item.setForeground(
                        QColor(0, 170, 0),
                    )

                elif m.delta < 0:
                    item.setForeground(
                        QColor(220, 0, 0),
                    )

                else:
                    item.setForeground(
                        QColor(120, 120, 120),
                    )

            self.setItem(
                row,
                3,
                item,
            )
