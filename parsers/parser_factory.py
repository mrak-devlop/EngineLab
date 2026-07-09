from pathlib import Path

from parsers.emanage_ultimate import EManageUltimateParser
from parsers.nissan_datascan import NissanDataScanParser


class ParserFactory:
    PARSERS = (
        NissanDataScanParser,
        EManageUltimateParser,
    )

    @classmethod
    def create(cls, file_path: Path):

        with file_path.open(
            "r",
            encoding="cp932",
            errors="ignore",
        ) as file:
            first_line = file.readline()

        for parser_class in cls.PARSERS:
            if parser_class.can_parse(first_line):
                return parser_class()

        raise ValueError("Не удалось определить формат лога.")
