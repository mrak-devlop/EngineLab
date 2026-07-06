import pyqtgraph as pg
from PySide6.QtWidgets import QVBoxLayout, QWidget


class PlotWidget(QWidget):
    """Обертка над PyQtGraph."""

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.graph = pg.PlotWidget()

        self.graph.showGrid(x=True, y=True)

        self.graph.setBackground("w")

        self.graph.addLegend()

        layout.addWidget(self.graph)

    def clear(self):

        self.graph.clear()

    def plot_channel(self, x, y, name):

        self.graph.clear()

        self.graph.plot(
            x,
            y,
            pen=pg.mkPen(width=2),
            name=name,
        )

        self.graph.setTitle(name)

        self.graph.setLabel("bottom", "Time")

        self.graph.setLabel("left", name)
