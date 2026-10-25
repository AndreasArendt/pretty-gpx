#!/usr/bin/python3
"""Light/Dark Color Theme."""
from enum import auto
from enum import Enum
from typing import Final
from typing import Self

from matplotlib import colors


class _BaseTheme(Enum):
    """Base Color Theme."""

    @classmethod
    def get_mapping(cls, *, include_modern: bool = False) -> dict[str, Self]:
        """Return the mapping."""
        color_emojis: Final[dict[str, str]] = {
            "BLACK": "⬛",
            "RED": "🟥",
            "GREEN": "🟩",
            "YELLOW": "🟨",
            "BLUE": "🟦",
            "PURPLE": "🟪",
            "WHITE": "⬜"
        }
        mapping = {}
        for theme in cls:
            parts = theme.name.split('_')
            if all(part in color_emojis for part in parts):
                mapping[''.join(color_emojis[part] for part in parts)] = theme
            elif include_modern:
                mapping[theme.name.replace('_', ' ').title()] = theme
        return mapping


class DarkTheme(_BaseTheme):
    """Dark Color Theme."""
    BLACK_GREEN_YELLOW = auto()
    BLACK_RED_WHITE = auto()
    BLACK_BLUE_WHITE = auto()
    BLUE_PURPLE_YELLOW = auto()
    MIDNIGHT_ICE = auto()
    SLATE_CITRUS = auto()


class LightTheme(_BaseTheme):
    """Light Color Theme."""
    YELLOW_GREEN_BLACK = auto()
    WHITE_RED_BLACK = auto()
    WHITE_BLUE_BLACK = auto()
    YELLOW_RED_BLACK = auto()
    WARM_MINIMAL = auto()
    ALPINE_SAGE = auto()
    SAND_COBALT = auto()


def hex_to_rgb(hex_color: str) -> tuple[int, ...]:
    """Convert hexadecimal color string to RGB triplet."""
    rgb_tuple = colors.hex2color(hex_color)
    rgb_int_tuple = tuple(int(x * 255) for x in rgb_tuple)
    return rgb_int_tuple
