from dataclasses import dataclass

from models.channel_type import ChannelType


@dataclass(slots=True)
class ChannelInfo:
    type: ChannelType = ChannelType.FLOAT

    unit: str = ""

    color: str | None = None

    precision: int = 2

    visible_by_default: bool = False
