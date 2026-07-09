from dataclasses import dataclass


@dataclass(slots=True)
class Measurement:
    name: str

    value_a: object
    value_b: object

    delta: object = None

    minimum: object = None
    maximum: object = None
