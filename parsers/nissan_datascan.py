from pathlib import Path

import numpy as np

from models.channel import Channel
from models.channel_info import ChannelInfo
from models.channel_type import ChannelType
from models.session import Session
from parsers.parser import LogParser
from parsers.value_converter import ValueConverter

CHANNEL_INFO = {
    "RPM": ChannelInfo(
        type=ChannelType.INTEGER,
        unit="rpm",
        precision=0,
    ),
    "Speed kph": ChannelInfo(
        type=ChannelType.INTEGER,
        unit="km/h",
        precision=0,
    ),
    "Water Temp C": ChannelInfo(
        type=ChannelType.FLOAT,
        unit="°C",
        precision=1,
    ),
    "Air Flow": ChannelInfo(
        type=ChannelType.FLOAT,
        unit="V",
        precision=2,
    ),
    "O2 Sensor": ChannelInfo(
        type=ChannelType.FLOAT,
        unit="V",
        precision=2,
    ),
}


class NissanDataScanParser(LogParser):
    def parse(self, file_path: Path) -> Session:

        with file_path.open(
            "r",
            encoding="cp1251",
        ) as file:
            lines = file.readlines()

        #
        # Заголовки
        #

        headers = [item.strip() for item in lines[0].strip().split(", ")]

        #
        # Каналы пока храним как строки
        #

        channels: dict[str, list[str]] = {}

        for header in headers[1:]:
            channels[header] = []

        timestamps: list[float] = []

        #
        # Чтение файла
        #

        for line in lines[1:]:
            if not line.strip():
                continue

            values = [item.strip() for item in line.strip().split(", ")]

            if len(values) != len(headers):
                print(f"Пропущена строка: ожидалось {len(headers)} полей, получено {len(values)}")

                continue

            #
            # Время
            #

            try:
                timestamps.append(
                    float(
                        values[0].replace(",", "."),
                    )
                )

            except ValueError:
                continue

            #
            # Остальные значения сохраняем как строки
            #

            for header, value in zip(headers[1:], values[1:]):
                channels[header].append(
                    value,
                )

        #
        # Создаем сессию
        #

        session = Session(
            name=file_path.stem,
            timestamps=np.asarray(
                timestamps,
                dtype=np.float64,
            ),
        )

        #
        # Создаем каналы
        #

        for name, values in channels.items():
            #
            # Есть описание?
            #

            info = CHANNEL_INFO.get(
                name,
            )

            #
            # Нет — определяем автоматически
            #

            if info is None:
                info = ChannelInfo(
                    type=ValueConverter.detect_type(
                        values,
                    ),
                )

            #
            # Преобразуем данные
            #

            data = ValueConverter.convert(
                values,
                info.type,
            )

            #
            # Добавляем канал
            #

            session.add_channel(
                Channel(
                    name=name,
                    values=data,
                    info=info,
                )
            )

        return session

    @staticmethod
    def can_parse(first_line: str) -> bool:

        return first_line.startswith("Time, ")
