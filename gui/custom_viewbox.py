import pyqtgraph as pg
from PySide6.QtCore import QObject, Signal


class ViewBoxSignals(QObject):

    mouse_moved = Signal(object)
    mouse_clicked = Signal(object)


class CustomViewBox(pg.ViewBox):

    def __init__(self):
        super().__init__()

        self.signals = ViewBoxSignals()

    def mouseMoveEvent(self, event):

        self.signals.mouse_moved.emit(event)

        super().mouseMoveEvent(event)

    def mouseClickEvent(self, event):

        self.signals.mouse_clicked.emit(event)

        super().mouseClickEvent(event)