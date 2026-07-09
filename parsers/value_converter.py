import numpy as np

from models.channel_type import ChannelType


class ValueConverter:
    TRUE_VALUES = {
        "true",
        "on",
        "yes",
        "enabled",
        "enable",
        "active",
        "open",
        "high",
        "1",
    }

    FALSE_VALUES = {
        "false",
        "off",
        "no",
        "disabled",
        "disable",
        "inactive",
        "closed",
        "close",
        "low",
        "0",
    }

    @staticmethod
    def is_suffix_integer(value: str) -> bool:

        value = value.strip()

        if not value.endswith("u"):
            return False

        try:
            int(value[:-1])
            return True

        except ValueError:
            return False

    @classmethod
    def detect_type(
        cls,
        values: list[str],
    ) -> ChannelType:

        #
        # Удаляем пустые строки
        #

        filtered = [value.strip() for value in values if value.strip() != ""]

        if not filtered:
            return ChannelType.FLOAT

        normalized = [value.lower() for value in filtered]

        #
        # Boolean
        #

        if all(value in cls.TRUE_VALUES | cls.FALSE_VALUES for value in normalized):
            return ChannelType.BOOLEAN

        #
        # Integer
        #

        try:
            for value in filtered:
                int(value)

            return ChannelType.INTEGER

        except ValueError:
            pass

        #
        # Integer + suffix (27u, -15u)
        #

        if all(cls.is_suffix_integer(value) for value in filtered):
            return ChannelType.SUFFIX_INTEGER

        #
        # Float
        #

        try:
            for value in filtered:
                float(
                    value.replace(",", "."),
                )

            return ChannelType.FLOAT

        except ValueError:
            pass

        #
        # String
        #

        return ChannelType.STRING

    @classmethod
    def convert(
        cls,
        values: list[str],
        channel_type: ChannelType,
    ):

        if channel_type == ChannelType.BOOLEAN:
            return np.asarray(
                [value.strip().lower() in cls.TRUE_VALUES for value in values],
                dtype=bool,
            )

        if channel_type == ChannelType.INTEGER:
            return np.asarray(
                [int(value) for value in values],
                dtype=np.int32,
            )

        if channel_type == ChannelType.SUFFIX_INTEGER:
            return np.asarray(
                [int(value[:-1]) for value in values],
                dtype=np.int32,
            )

        if channel_type == ChannelType.FLOAT:
            result = []

            for value in values:
                try:
                    result.append(
                        float(
                            value.replace(",", "."),
                        )
                    )

                except ValueError:
                    result.append(np.nan)

            return np.asarray(
                result,
                dtype=np.float64,
            )

        return np.asarray(
            values,
            dtype=object,
        )
