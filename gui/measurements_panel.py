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
        super().__init__(0, 6)

        self.setHorizontalHeaderLabels(
            [
                "Канал",
                "Точка A",
                "Точка B",
                "Δ",
                "Min",
                "Max",
            ]
        )

        self.verticalHeader().hide()

        self.horizontalHeader().setSectionResizeMode(
            0,
            QHeaderView.Stretch,
        )

        header = self.horizontalHeader()

        header.setStretchLastSection(False)

        #
        # Первая колонка занимает всё оставшееся место
        #

        header.setSectionResizeMode(
            0,
            QHeaderView.Stretch,
        )

        #
        # Остальные фиксированной ширины
        #

        for column in range(1, 6):
            header.setSectionResizeMode(
                column,
                QHeaderView.Fixed,
            )

        #
        # Ширина столбцов
        #

        self.setColumnWidth(1, 60)  # A
        self.setColumnWidth(2, 60)  # B
        self.setColumnWidth(3, 60)  # Δ
        self.setColumnWidth(4, 60)  # Min
        self.setColumnWidth(5, 60)  # Max

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
                    m.value_b,
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
                    signed=True,
                ),
            )

            item.setTextAlignment(
                Qt.AlignVCenter | Qt.AlignRight,
            )

            if m.delta is not None:
                if isinstance(m.delta, (int, float)):
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

            #
            # Minimum
            #

            item = QTableWidgetItem(
                self.format_value(
                    m.minimum,
                ),
            )

            item.setTextAlignment(
                Qt.AlignVCenter | Qt.AlignRight,
            )

            self.setItem(
                row,
                4,
                item,
            )

            #
            # Maximum
            #

            item = QTableWidgetItem(
                self.format_value(
                    m.maximum,
                ),
            )

            item.setTextAlignment(
                Qt.AlignVCenter | Qt.AlignRight,
            )

            self.setItem(
                row,
                5,
                item,
            )
