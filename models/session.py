from dataclasses import dataclass, field

import numpy as np
from numpy.typing import NDArray

from .channel import Channel
from .marker import Marker


@dataclass(slots=True)
class Session:
    """Одна запись логов."""

    name: str

    timestamps: NDArray[np.float64]

    channels: dict[str, Channel] = field(default_factory=dict)

    marker_a: Marker = field(default_factory=Marker)
    marker_b: Marker = field(default_factory=Marker)

    def add_channel(self, channel: Channel) -> None:
        self.channels[channel.name] = channel

    def get_channel(self, name: str) -> Channel | None:
        return self.channels.get(name)

    def __getitem__(self, name: str):
        return self.channels[name]

    def __contains__(self, name: str):
        return name in self.channels

    def values_at(self, index: int) -> dict[str, float]:

        values = {}

        for channel in self.channels.values():
            values[channel.name] = channel.values[index]

        return values
