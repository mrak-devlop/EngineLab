from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFileDialog

from gui.plot_manager import PlotManager
from models.cursor_mode import CursorMode
from models.project import Project
from parsers.parser_factory import ParserFactory


class MainController:
    def __init__(self, window):

        self.window = window

        self.plot_manager = PlotManager(
            window.plot_area,
        )

        #
        # Сигналы
        #

        self.window.open_action.triggered.connect(
            self.open_log,
        )

        self.window.channel_tree.itemChanged.connect(
            self.channels_changed,
        )

        self.plot_manager.plot_closed.connect(
            self.plot_closed,
        )

        self.plot_manager.cursor_moved.connect(
            self.cursor_moved,
        )

        self.plot_manager.marker_changed.connect(
            self.marker_changed,
        )

        self.current_index = -1

        self.cursor_mode = CursorMode.CURSOR

        self.window.cursor_mode_group.buttonClicked.connect(
            self.on_cursor_mode_changed,
        )

        self.window.zoom_markers_button.clicked.connect(
            self.zoom_to_markers,
        )

        self.window.reset_zoom_button.clicked.connect(
            self.reset_zoom,
        )

        self.window.project_panel.current_changed.connect(
            self.project_session_changed,
        )

    def current_session(self):

        project = self.window.project

        if project is None:
            return None

        return project.current_session

    def load_session(self):

        filename, _ = QFileDialog.getOpenFileName(
            self.window,
            "Открыть лог",
            ".",
            "Log files (*.log *.txt *.csv);;All files (*.*)",
        )

        if not filename:
            return None

        parser = ParserFactory.create(
            Path(filename),
        )

        return parser.parse(
            Path(filename),
        )

    def open_log(self):

        session = self.load_session()

        if session is None:
            return

        project = self.window.project

        #
        # Если проекта ещё нет — создаём его
        #

        if project is None:
            project = Project()

        #
        # Добавляем лог в проект
        #

        project.add_session(
            session,
        )

        #
        # Первый открытый лог
        #

        if self.window.project is None:
            self.window.set_project(
                project,
            )

            self.plot_manager.session = session

            self.plot_manager.clear()

        #
        # Последующие логи
        #

        else:
            self.window.project_panel.set_project(
                project,
            )

    def channels_changed(self, item):

        session = self.current_session()

        if session is None:
            return

        channel = item.data(0, Qt.UserRole)
        print("channels_changed:", channel.name, item.checkState(0))

        if channel is None:
            return

        if item.checkState(0) == Qt.Checked:
            session.opened_channels.add(
                channel.name,
            )

            self.plot_manager.show_channel(
                session.timestamps,
                channel,
            )

        else:
            session.opened_channels.discard(
                channel.name,
            )

            self.plot_manager.hide_channel(
                channel,
            )

    def cursor_moved(self, index: int):

        if index == self.current_index:
            return

        self.current_index = index

        if self.window.project is None:
            return

        session = self.current_session()

        if session is None:
            return

        values = session.values_at(index)

        for channel_name, value in values.items():
            self.window.info_panel.set_value(
                channel_name,
                value,
            )

    def on_cursor_mode_changed(self, button):

        if button is self.window.cursor_radio:
            self.cursor_mode = CursorMode.CURSOR

        elif button is self.window.marker_a_radio:
            self.cursor_mode = CursorMode.MARKER_A

        elif button is self.window.marker_b_radio:
            self.cursor_mode = CursorMode.MARKER_B

        self.plot_manager.set_cursor_mode(
            self.cursor_mode,
        )

    def marker_changed(self, measurements):

        self.window.measurements_panel.set_measurements(
            measurements,
        )

    def zoom_to_markers(self):

        if self.plot_manager.marker_a_index < 0 or self.plot_manager.marker_b_index < 0:
            return

        session = self.current_session()

        if session is None:
            return

        timestamps = session.timestamps

        x1 = timestamps[self.plot_manager.marker_a_index]
        x2 = timestamps[self.plot_manager.marker_b_index]

        left = min(x1, x2)
        right = max(x1, x2)

        padding = (right - left) * 0.03

        self.plot_manager.zoom_to_range(
            left - padding,
            right + padding,
        )

    def plot_closed(
        self,
        channel_name: str,
    ):

        self.window.channel_tree.set_channel_checked(
            channel_name,
            False,
        )

    def reset_zoom(self):

        self.plot_manager.reset_zoom()

    def project_session_changed(
        self,
        index: int,
    ):

        project = self.window.project

        if project is None:
            return

        project.set_current_session(
            index,
        )

        session = project.current_session

        if session is None:
            return

        #
        # Очистить текущие графики
        #

        self.plot_manager.clear()

        #
        # Сообщить PlotManager о новой сессии
        #

        self.plot_manager.session = session
        self.plot_manager.timestamps = session.timestamps
        self.plot_manager.marker_a_index = session.marker_a.index
        self.plot_manager.marker_b_index = session.marker_b.index

        #
        # Заполнить дерево каналов
        #

        self.window.channel_tree.set_channels(
            session.channels,
        )

        #
        # Восстановить открытые каналы
        #

        for channel_name in session.opened_channels:
            self.window.channel_tree.set_channel_checked(
                channel_name,
                True,
            )

        #
        # Обновить панель значений
        #

        self.window.info_panel.set_channels(
            session.channels,
        )

        #
        # Обновить правые панели
        #

        if session.cursor_index >= 0:
            self.cursor_moved(
                session.cursor_index,
            )

        self.plot_manager.update_measurements()
