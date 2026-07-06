from gui.plot_widget import PlotWidget


class PlotManager:
    def __init__(self, plot_area):

        self.plot_area = plot_area

        # имя канала -> PlotWidget
        self.plots = {}

    def show_channel(self, timestamps, channel):

        if channel.name in self.plots:
            return

        plot = PlotWidget()

        plot.show_channel(
            timestamps,
            channel,
        )

        self.plot_area.add_plot(plot)

        self.plots[channel.name] = plot

    def hide_channel(self, channel):

        plot = self.plots.pop(channel.name, None)

        if plot is None:
            return

        self.plot_area.remove_plot(plot)

    def clear(self):

        for plot in list(self.plots.values()):
            self.plot_area.remove_plot(plot)

        self.plots.clear()
