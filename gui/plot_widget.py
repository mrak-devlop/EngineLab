import numpy as np
import pyqtgraph as pg
from PySide6.QtCore import Qt, Signal
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
    clicked = Signal(object, int)

    def __init__(self):
        super().__init__()

        self.channel = None
        self.timestamps = None
        self.values = None

        self._syncing = False
        self._last_index = -1

        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setMinimumHeight(180)
        self.setMaximumHeight(220)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(2)

        #
        # Header
        #

        header = QHBoxLayout()

        self.title = QLabel()

        self.close_button = QPushButton("✕")
        self.close_button.setFixedSize(24, 24)

        header.addWidget(self.title)
        header.addStretch()
        header.addWidget(self.close_button)

        #
        # Plot
        #

        self.plot = pg.PlotWidget()

        self.selection = pg.LinearRegionItem(
            values=(0, 0),
            orientation="vertical",
            movable=False,
            brush=pg.mkBrush(0, 120, 255, 40),
            pen=pg.mkPen(None),
        )

        self.selection.setZValue(-100)

        self.selection.hide()

        self.plot.addItem(self.selection)

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

        self.marker_a_line = pg.InfiniteLine(
            angle=90,
            movable=False,
            pen=pg.mkPen((0, 255, 0), width=2),
        )

        self.marker_a_point = pg.ScatterPlotItem(
            size=10,
            pen=pg.mkPen("w"),
            brush=pg.mkBrush(0, 255, 0),
        )

        self.marker_b_line = pg.InfiniteLine(
            angle=90,
            movable=False,
            pen=pg.mkPen((255, 0, 0), width=2),
        )

        self.marker_b_point = pg.ScatterPlotItem(
            size=10,
            pen=pg.mkPen("w"),
            brush=pg.mkBrush(255, 0, 0),
        )

        self.plot.addItem(self.cursor)
        self.plot.addItem(self.marker)

        self.plot.addItem(self.marker_a_line)
        self.plot.addItem(self.marker_a_point)

        self.plot.addItem(self.marker_b_line)
        self.plot.addItem(self.marker_b_point)

        self.marker_a_line.hide()
        self.marker_a_point.hide()

        self.marker_b_line.hide()
        self.marker_b_point.hide()

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

        #
        # Signals
        #

        self.close_button.clicked.connect(
            self.on_close,
        )

        self.plot.scene().sigMouseMoved.connect(
            self.mouse_moved,
        )

        self.click_proxy = pg.SignalProxy(
            self.plot.scene().sigMouseClicked,
            slot=self.mouse_clicked,
        )

        self.plot.plotItem.vb.sigXRangeChanged.connect(
            self.x_range_changed,
        )

    #
    # Public
    #

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
            x=[x],
            y=[y],
        )

        self.marker.show()

    def set_marker_a(self, index: int):

        if self.channel is None:
            return

        if index < 0 or index >= len(self.timestamps):
            return

        x = self.timestamps[index]
        y = self.values[index]

        self.marker_a_line.setValue(x)

        self.marker_a_point.setData(
            x=[x],
            y=[y],
        )

        self.marker_a_line.show()
        self.marker_a_point.show()

    def set_marker_b(self, index: int):

        if self.channel is None:
            return

        if index < 0 or index >= len(self.timestamps):
            return

        x = self.timestamps[index]
        y = self.values[index]

        self.marker_b_line.setValue(x)

        self.marker_b_point.setData(
            x=[x],
            y=[y],
        )

        self.marker_b_line.show()
        self.marker_b_point.show()

    def set_x_range(
        self,
        x_min: float,
        x_max: float,
    ):

        self._syncing = True

        self.plot.setXRange(
            x_min,
            x_max,
            padding=0,
        )

        self._syncing = False

    #
    # Events
    #

    def on_close(self):

        if self.channel is None:
            return

        self.closed.emit(
            self.channel.name,
        )

    def mouse_moved(self, pos):

        if self.channel is None:
            return

        view_pos = self.plot.plotItem.vb.mapSceneToView(
            pos,
        )

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

    def mouse_clicked(self, args):

        event = args[0]

        if self.channel is None:
            return

        if event.button() != Qt.LeftButton:
            return

        view_pos = self.plot.plotItem.vb.mapSceneToView(
            event.scenePos(),
        )

        index = self.find_nearest_index(
            self.timestamps,
            view_pos.x(),
        )

        self.clicked.emit(
            self,
            index,
        )

    def x_range_changed(
        self,
        view_box,
        x_range,
    ):

        if self._syncing:
            return

        self.view_changed.emit(
            self,
            x_range[0],
            x_range[1],
        )

    #
    # Helpers
    #

    @staticmethod
    def find_nearest_index(
        timestamps,
        x,
    ):

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

    def set_region(
        self,
        index_a: int,
        index_b: int,
    ):

        if self.channel is None or index_a < 0 or index_b < 0:
            self.selection.hide()
            return

        x1 = self.timestamps[index_a]
        x2 = self.timestamps[index_b]

        self.selection.setRegion(
            (
                min(x1, x2),
                max(x1, x2),
            )
        )

        self.selection.show()

    def get_x_range(self) -> tuple[float, float]:

        return tuple(self.plot.getViewBox().viewRange()[0])
