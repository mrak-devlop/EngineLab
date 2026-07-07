import numpy as np
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
    cursor_moved = Signal(object, int)
    view_changed = Signal(object, float, float)

    def __init__(self):
        super().__init__()

        self.channel = None
        self._syncing = False

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

        self.curve = self.plot.plot(
            [],
            [],
            pen=pg.mkPen(width=2),
        )

        self.cursor = pg.InfiniteLine(
            angle=90,
            movable=False,
        )

        self.marker = pg.ScatterPlotItem(
            size=8,
            pen=pg.mkPen("w"),
            brush=pg.mkBrush("r"),
        )

        self.plot.addItem(self.marker)

        self.plot.addItem(self.cursor)

        self.cursor.hide()

        self.marker.hide()

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

        self.plot.scene().sigMouseMoved.connect(
            self.mouse_moved,
        )

        self.plot.plotItem.vb.sigXRangeChanged.connect(
            self.x_range_changed,
        )

        self._last_index = -1

    def show_channel(
        self,
        timestamps,
        channel: Channel,
    ):

        self.channel = channel

        self.timestamps = timestamps

        self.values = channel.values

        self.title.setText(channel.name)

        self.curve.setData(
            timestamps,
            channel.values,
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

    def mouse_moved(self, pos):

        view_pos = self.plot.plotItem.vb.mapSceneToView(pos)

        index = self.find_nearest_index(
            self.timestamps,
            view_pos.x(),
        )

        if index == self._last_index:
            return

        self._last_index = index

        self.cursor_moved.emit(
            self,
            index,
        )

    def find_nearest_index(self, timestamps, x):

        index = np.searchsorted(
            timestamps,
            x,
        )

        if index <= 0:
            return 0

        if index >= len(timestamps):
            return len(timestamps) - 1

        left = timestamps[index - 1]
        right = timestamps[index]

        if abs(x - left) <= abs(right - x):
            return index - 1

        return index

    def set_cursor(self, index: int):

        if self.channel is None:
            return

        if index < 0 or index >= len(self.timestamps):
            return

        x = self.timestamps[index]
        y = self.values[index]

        self.cursor.setValue(x)
        self.cursor.show()

        self.marker.setData(
            pos=[(x, y)],
        )

        self.marker.show()

    def x_range_changed(self, view_box, x_range):

        if self._syncing:
            return

        self.view_changed.emit(
            self,
            x_range[0],
            x_range[1],
        )

    def set_x_range(self, x_min: float, x_max: float):

        self._syncing = True

        self.plot.setXRange(
            x_min,
            x_max,
            padding=0,
        )

        self._syncing = False
