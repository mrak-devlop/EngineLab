import numpy as np
from PySide6.QtCore import QObject, Signal

from gui.plot_widget import PlotWidget
from models.cursor_mode import CursorMode
from models.measurement import Measurement


class PlotManager(QObject):
    plot_closed = Signal(str)
    cursor_moved = Signal(int)
    marker_changed = Signal(list)
    marker_placed = Signal(CursorMode)

    def __init__(self, plot_area):
        super().__init__()

        self.plot_area = plot_area
        self.plots = {}

        self.cursor_mode = CursorMode.CURSOR
        self.cursor_index = -1

        self.marker_a_index = -1
        self.marker_b_index = -1
        self.timestamps = None
        self.session = None
        self.measurements = []

    def set_cursor_mode(self, mode):

        self.cursor_mode = mode

    def set_session(
        self,
        session,
    ):

        self.session = session

        self.timestamps = session.timestamps

        #
        # Закрыть все текущие графики
        #

        self.clear()

        #
        # Сбросить курсор
        #

        self.cursor_index = -1

        self.marker_a_index = -1

        self.marker_b_index = -1

        #
        # Открыть сохранённые графики
        #

        for channel_name in session.opened_channels:
            channel = session.channels.get(
                channel_name,
            )

            if channel is not None:
                self.show_channel(
                    session.timestamps,
                    channel,
                )

    def show_channel(
        self,
        timestamps,
        channel,
    ):

        if channel.name in self.plots:
            return self.plots[channel.name]

        self.timestamps = timestamps

        #
        # Запоминаем текущий масштаб
        #

        current_range = None

        if self.plots:
            current_range = next(iter(self.plots.values())).get_x_range()

        plot = PlotWidget()

        plot.closed.connect(
            self.on_plot_closed,
        )

        plot.cursor_moved.connect(
            self.on_cursor_moved,
        )

        plot.view_changed.connect(
            self.on_view_changed,
        )

        plot.clicked.connect(
            self.on_plot_clicked,
        )

        plot.show_channel(
            timestamps,
            channel,
        )

        #
        # Восстановить курсор
        #

        if self.session is not None and self.session.cursor_index >= 0:
            self.cursor_index = self.session.cursor_index

            plot.set_cursor(
                self.session.cursor_index,
            )
        #
        # Marker A
        #

        if self.session is not None and self.session.marker_a.visible:
            self.marker_a_index = self.session.marker_a.index

            plot.set_marker_a(
                self.session.marker_a.index,
            )

        #
        # Marker B
        #

        if self.session is not None and self.session.marker_b.visible:
            self.marker_b_index = self.session.marker_b.index

            plot.set_marker_b(
                self.session.marker_b.index,
            )

        #
        # Выделение между маркерами
        #

        if (
            self.session is not None
            and self.session.marker_a.visible
            and self.session.marker_b.visible
        ):
            plot.set_region(
                self.session.marker_a.index,
                self.session.marker_b.index,
            )
        #
        # Восстановить масштаб
        #

        if current_range is not None:
            #
            # Есть уже открытые графики этой Session
            #

            plot.set_x_range(
                current_range[0],
                current_range[1],
            )

        elif (
            self.session is not None
            and self.session.zoom_left is not None
            and self.session.zoom_right is not None
        ):
            #
            # Первый график после переключения Session
            #

            plot.set_x_range(
                self.session.zoom_left,
                self.session.zoom_right,
            )
        self.plot_area.add_plot(
            plot,
        )

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

        self.cursor_index = index

        if self.session is not None:
            self.session.cursor_index = index

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

        if self.session is not None:
            self.session.zoom_left = x_min
            self.session.zoom_right = x_max

    def on_plot_clicked(self, source_plot, index):

        match self.cursor_mode:
            case CursorMode.CURSOR:
                return

            case CursorMode.MARKER_A:
                self.marker_a_index = index

                if self.session is not None:
                    self.session.marker_a.index = index
                    self.session.marker_a.visible = True

                for plot in self.plots.values():
                    plot.set_marker_a(index)
                    plot.set_region(
                        self.marker_a_index,
                        self.marker_b_index,
                    )
                self.marker_placed.emit(
                    CursorMode.MARKER_A,
                )
            case CursorMode.MARKER_B:
                self.marker_b_index = index

                if self.session is not None:
                    self.session.marker_b.index = index
                    self.session.marker_b.visible = True

                for plot in self.plots.values():
                    plot.set_marker_b(index)
                    plot.set_region(
                        self.marker_a_index,
                        self.marker_b_index,
                    )
                self.marker_placed.emit(
                    CursorMode.MARKER_B,
                )
        self.update_measurements()

    def update_measurements(self):

        if self.timestamps is None or self.session is None or self.marker_a_index < 0:
            return

        t1 = self.timestamps[self.marker_a_index]
        t2 = self.timestamps[self.marker_b_index]

        values_a = self.session.values_at(
            self.marker_a_index,
        )

        values_b = {}

        if self.marker_b_index >= 0:
            values_b = self.session.values_at(
                self.marker_b_index,
            )

        left = min(
            self.marker_a_index,
            self.marker_b_index,
        )

        right = max(
            self.marker_a_index,
            self.marker_b_index,
        )

        self.measurements.clear()

        for name, value_a in values_a.items():
            value_b = values_b.get(name)

            delta = None
            minimum = None
            maximum = None

            if (
                self.marker_b_index >= 0
                and isinstance(value_a, (int, float, np.integer, np.floating))
                and isinstance(value_b, (int, float, np.integer, np.floating))
            ):
                delta = value_b - value_a

                channel = self.session.channels.get(name)

                if channel is not None:
                    values = channel.values[left : right + 1]

                    try:
                        if np.issubdtype(
                            values.dtype,
                            np.number,
                        ):
                            minimum = np.nanmin(values)
                            maximum = np.nanmax(values)

                    except Exception:
                        pass

            self.measurements.append(
                Measurement(
                    name=name,
                    value_a=value_a,
                    value_b=value_b,
                    delta=delta,
                    minimum=minimum,
                    maximum=maximum,
                )
            )

        self.marker_changed.emit(
            self.measurements,
        )

    def zoom_to_range(
        self,
        left: float,
        right: float,
    ):

        if self.session is not None:
            self.session.zoom_left = left
            self.session.zoom_right = right

        for plot in self.plots.values():
            plot.set_x_range(
                left,
                right,
            )

    def reset_zoom(self):

        if self.timestamps is None:
            return

        left = self.timestamps[0]
        right = self.timestamps[-1]

        for plot in self.plots.values():
            plot.set_x_range(
                left,
                right,
            )
