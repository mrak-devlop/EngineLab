from pathlib import Path

import numpy as np

from models.channel import Channel
from models.channel_info import ChannelInfo
from models.session import Session
from parsers.parser import LogParser
from parsers.value_converter import ValueConverter


class EManageUltimateParser(LogParser):
    @staticmethod
    def can_parse(first_line: str) -> bool:

        headers = first_line.split("\t")

        while headers and headers[-1].strip() == "":
            headers.pop()

        return len(headers) > 2 and headers[0] == "msec" and "Engine Speed(rpm)" in headers

    def parse(
        self,
        file_path: Path,
    ) -> Session:

        with file_path.open(
            "r",
            encoding="cp932",
            errors="ignore",
        ) as file:
            lines = file.readlines()

        #
        # Заголовки
        #

        headers = [item.strip() for item in lines[0].split("\t")]

        while headers and headers[-1] == "":
            headers.pop()

        #
        # Каналы
        #

        channels: dict[str, list[str]] = {}

        for header in headers[1:]:
            channels[header] = []

        timestamps: list[float] = []

        #
        # Чтение строк
        #

        for line in lines[1:]:
            if not line.strip():
                continue

            values = [item.strip() for item in line.split("\t")]

            while values and values[-1] == "":
                values.pop()

            if len(values) != len(headers):
                print(f"Пропущена строка: ожидалось {len(headers)} полей, получено {len(values)}")
                continue

            #
            # Время (мс → сек)
            #

            try:
                timestamps.append(float(values[0]) / 1000.0)

            except ValueError:
                continue

            #
            # Каналы
            #

            for header, value in zip(
                headers[1:],
                values[1:],
            ):
                channels[header].append(value)

        #
        # Session
        #

        session = Session(
            name=file_path.stem,
            timestamps=np.asarray(
                timestamps,
                dtype=np.float64,
            ),
        )

        #
        # Каналы
        #

        for name, values in channels.items():
            channel_type = ValueConverter.detect_type(
                values,
            )

            info = ChannelInfo(
                type=channel_type,
            )

            data = ValueConverter.convert(
                values,
                channel_type,
            )

            session.add_channel(
                Channel(
                    name=name,
                    values=data,
                    info=info,
                )
            )

        return session
