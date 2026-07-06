from abc import ABC, abstractmethod
from pathlib import Path

from models.session import Session


class LogParser(ABC):
    @abstractmethod
    def parse(self, file_path: Path) -> Session:
        pass
