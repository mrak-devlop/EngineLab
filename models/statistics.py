from dataclasses import dataclass


@dataclass(slots=True)
class Statistics:
    name: str

    minimum: object
    maximum: object
    average: object
