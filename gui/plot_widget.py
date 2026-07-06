import pyqtgraph as pg
from PySide6.QtWidgets import QVBoxLayout, QWidget

from models.channel import Channel


class PlotWidget(QWidget):
    """Виджет одного графика."""

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.plot = pg.PlotWidget()

        self.plot.showGrid(x=True, y=True)

        self.plot.setBackground("w")

        layout.addWidget(self.plot)

    def clear(self):

        self.plot.clear()

    def show_channel(self, timestamps, channel: Channel):

        self.plot.clear()

        self.plot.plot(
            timestamps,
            channel.values,
            pen=pg.mkPen(width=2),
        )

        self.plot.setTitle(channel.name)

        self.plot.setLabel("left", channel.name)

        self.plot.setLabel("bottom", "Time")
