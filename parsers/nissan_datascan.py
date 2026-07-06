from pathlib import Path

import numpy as np

from models.channel import Channel
from models.session import Session
from parsers.parser import LogParser


class NissanDataScanParser(LogParser):
    def parse(self, file_path: Path) -> Session:

        with file_path.open("r", encoding="cp1251") as file:
            lines = file.readlines()

        headers = [item.strip() for item in lines[0].strip().split(", ")]

        channels: dict[str, list[float]] = {}

        for header in headers[1:]:
            channels[header] = []

        timestamps: list[float] = []

        for line in lines[1:]:
            if not line.strip():
                continue

            values = [item.strip() for item in line.strip().split(", ")]

            if len(values) != len(headers):
                print(f"Пропущена строка: ожидалось {len(headers)} полей, получено {len(values)}")
                continue

            timestamps.append(float(values[0]))

            for header, value in zip(headers[1:], values[1:]):
                try:
                    number = float(value.replace(",", "."))
                except ValueError:
                    number = np.nan

                channels[header].append(number)

        session = Session(name=file_path.stem, timestamps=np.asarray(timestamps, dtype=np.float64))

        for name, values in channels.items():
            session.add_channel(Channel(name=name, values=np.asarray(values, dtype=np.float64)))

        return session
