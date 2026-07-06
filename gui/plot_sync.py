class PlotSyncManager:
    def __init__(self):
        self.plots = []

    def register(self, plot):
        self.plots.append(plot)

    def unregister(self, plot):
        if plot in self.plots:
            self.plots.remove(plot)
