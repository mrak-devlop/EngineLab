from PySide6.QtWidgets import (
    QScrollArea,
    QVBoxLayout,
    QWidget,
)


class PlotArea(QScrollArea):
    """Контейнер для нескольких графиков."""

    def __init__(self):
        super().__init__()

        self.setWidgetResizable(True)

        self.container = QWidget()

        self.layout = QVBoxLayout(self.container)
        self.layout.setContentsMargins(4, 4, 4, 4)
        self.layout.setSpacing(8)

        self.layout.addStretch()

        self.setWidget(self.container)

    def add_plot(self, plot):

        self.layout.insertWidget(
            self.layout.count() - 1,
            plot,
        )

    def clear(self):

        while self.layout.count() > 1:
            item = self.layout.takeAt(0)

            widget = item.widget()

            if widget is not None:
                widget.deleteLater()
