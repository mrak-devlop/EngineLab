from gui.plot_widget import PlotWidget


class PlotManager:
    def __init__(self, plot_area):

        self.plot_area = plot_area

    def show_channel(
        self,
        session,
        channel_name,
    ):

        self.clear()

        channel = session[channel_name]

        plot = PlotWidget()

        plot.show_channel(
            session.timestamps,
            channel,
        )

        self.plot_area.add_plot(plot)

    def clear(self):

        self.plot_area.clear()
