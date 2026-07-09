from enum import Enum, auto


class ChannelType(Enum):
    FLOAT = auto()
    INTEGER = auto()
    BOOLEAN = auto()
    ENUM = auto()
    STRING = auto()
    SUFFIX_INTEGER = auto()
