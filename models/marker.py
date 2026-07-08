from dataclasses import dataclass


@dataclass(slots=True)
class Marker:
    index: int = -1
    visible: bool = False
