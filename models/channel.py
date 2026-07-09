from models.channel_info import ChannelInfo


class Channel:
    def __init__(
        self,
        name,
        values,
        info: ChannelInfo | None = None,
    ):

        self.name = name

        self.values = values

        self.info = info or ChannelInfo()
