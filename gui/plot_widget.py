import pyqtgraph as pg
from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from models.channel import Channel


class PlotWidget(QFrame):
    """Панель одного графика."""

    closed = Signal(str)

    def __init__(self):
        super().__init__()

        self.channel = None

        self.setFrameShape(QFrame.Shape.StyledPanel)

        self.setMinimumHeight(180)
        self.setMaximumHeight(220)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(2)

        #
        # Верхняя панель
        #

        header = QHBoxLayout()

        self.title = QLabel("")

        self.close_button = QPushButton("✕")

        self.close_button.setFixedSize(24, 24)

        header.addWidget(self.title)

        header.addStretch()

        header.addWidget(self.close_button)

        #
        # График
        #

        self.plot = pg.PlotWidget()

        self.plot.showGrid(
            x=True,
            y=True,
            alpha=0.3,
        )

        self.plot.setMouseEnabled(
            x=True,
            y=False,
        )

        self.plot.setMenuEnabled(False)

        layout.addLayout(header)

        layout.addWidget(self.plot)

        self.close_button.clicked.connect(self.on_close)

    def show_channel(
        self,
        timestamps,
        channel: Channel,
    ):

        self.channel = channel

        self.title.setText(channel.name)

        self.plot.clear()

        self.plot.plot(
            timestamps,
            channel.values,
            pen=pg.mkPen(width=2),
        )

        self.plot.setLabel(
            "left",
            channel.name,
        )

        self.plot.setLabel(
            "bottom",
            "Time",
        )

    def on_close(self):

        if self.channel is None:
            return

        self.closed.emit(self.channel.name)
