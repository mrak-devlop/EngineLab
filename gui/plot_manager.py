from PySide6.QtCore import QObject, Signal

from gui.plot_widget import PlotWidget
from models.cursor_mode import CursorMode


class PlotManager(QObject):
    plot_closed = Signal(str)
    cursor_moved = Signal(int)
    marker_changed = Signal()

    def __init__(self, plot_area):
        super().__init__()

        self.plot_area = plot_area
        self.plots = {}

        self.cursor_mode = CursorMode.CURSOR

    def set_cursor_mode(self, mode):

        self.cursor_mode = mode

    def show_channel(self, timestamps, channel):

        if channel.name in self.plots:
            return self.plots[channel.name]

        plot = PlotWidget()

        plot.closed.connect(self.on_plot_closed)
        plot.cursor_moved.connect(self.on_cursor_moved)
        plot.view_changed.connect(self.on_view_changed)
        plot.clicked.connect(self.on_plot_clicked)

        plot.show_channel(
            timestamps,
            channel,
        )

        self.plot_area.add_plot(plot)

        self.plots[channel.name] = plot

        return plot

    def hide_channel(self, channel):

        plot = self.plots.pop(channel.name, None)

        if plot is None:
            return

        self.plot_area.remove_plot(plot)

    def clear(self):

        for plot in list(self.plots.values()):
            self.plot_area.remove_plot(plot)

        self.plots.clear()

    def on_plot_closed(self, channel_name: str):

        plot = self.plots.pop(channel_name, None)

        if plot is None:
            return

        self.plot_area.remove_plot(plot)

        self.plot_closed.emit(channel_name)

    def on_cursor_moved(self, source_plot, index):

        for plot in self.plots.values():
            plot.set_cursor(index)

        self.cursor_moved.emit(index)

    def on_view_changed(
        self,
        source_plot,
        x_min: float,
        x_max: float,
    ):

        for plot in self.plots.values():
            if plot is source_plot:
                continue

            plot.set_x_range(
                x_min,
                x_max,
            )

    def on_plot_clicked(self, source_plot, index):

        match self.cursor_mode:
            case CursorMode.CURSOR:
                return

            case CursorMode.MARKER_A:
                for plot in self.plots.values():
                    plot.set_marker_a(index)

            case CursorMode.MARKER_B:
                for plot in self.plots.values():
                    plot.set_marker_b(index)

        self.marker_changed.emit()
