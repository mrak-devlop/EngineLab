from abc import ABC, abstractmethod
from pathlib import Path

from models.session import Session


class LogParser(ABC):
    @staticmethod
    @abstractmethod
    def can_parse(first_line: str) -> bool:
        pass

    @abstractmethod
    def parse(self, file_path: Path) -> Session:
        pass
