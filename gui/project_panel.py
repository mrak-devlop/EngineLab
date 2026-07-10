from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem


class ProjectPanel(QTreeWidget):
    current_changed = Signal(int)

    def __init__(self):
        super().__init__()

        self.setHeaderLabel("Логи")

        self.currentItemChanged.connect(
            self.on_current_item_changed,
        )

    def set_project(
        self,
        project,
    ):

        self.clear()

        if project is None:
            return

        for session in project.sessions:
            item = QTreeWidgetItem(
                [session.name],
            )

            item.setFlags(
                Qt.ItemIsSelectable | Qt.ItemIsEnabled,
            )

            self.addTopLevelItem(
                item,
            )

        if project.session_count:
            self.setCurrentItem(
                self.topLevelItem(
                    project.current_index,
                )
            )

    def on_current_item_changed(
        self,
        current,
        previous,
    ):

        if current is None:
            return

        index = self.indexOfTopLevelItem(
            current,
        )

        self.current_changed.emit(
            index,
        )
