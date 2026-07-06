from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray


@dataclass(slots=True)
class Channel:
    """Один канал логов."""

    name: str
    values: NDArray[np.float64]
