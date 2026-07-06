from dataclasses import dataclass, field


@dataclass(slots=True)
class Channel:
    name: str

    values: list

    unit: str = ""

    color: str = ""

    visible: bool = True
