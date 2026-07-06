from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem


class ChannelTree(QTreeWidget):
    """Дерево каналов."""

    def __init__(self):
        super().__init__()

        self.setHeaderLabel("Каналы")

    def set_channels(self, channels):

        self.clear()

        for channel in channels.values():
            item = QTreeWidgetItem([channel.name])

            item.setFlags(
                item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsSelectable | Qt.ItemIsEnabled
            )

            item.setCheckState(0, Qt.Unchecked)

            # Храним сам объект Channel
            item.setData(0, Qt.UserRole, channel)

            self.addTopLevelItem(item)

    def checked_channels(self):

        result = []

        root = self.invisibleRootItem()

        for i in range(root.childCount()):
            item = root.child(i)

            if item.checkState(0) == Qt.Checked:
                result.append(item.data(0, Qt.UserRole))

        return result

    def clear_checks(self):

        root = self.invisibleRootItem()

        for i in range(root.childCount()):
            root.child(i).setCheckState(
                0,
                Qt.Unchecked,
            )

    def set_channel_checked(self, channel_name: str, checked: bool):
        root = self.invisibleRootItem()

        for i in range(root.childCount()):
            item = root.child(i)

            if item.text(0) == channel_name:
                item.setCheckState(
                    0,
                    Qt.Checked if checked else Qt.Unchecked,
                )
                return
