#!/usr/bin/python3
"""Mountain Colors."""

from dataclasses import dataclass
from typing import Final

from pretty_gpx.common.drawing.utils.color_theme import DarkTheme
from pretty_gpx.common.drawing.utils.color_theme import LightTheme


@dataclass
class MountainColors:
    """Mountain Colors."""
    dark_mode: bool
    background_color: str
    track_color: str
    peak_color: str
    terrain_shadow_color: str | None = None


MOUNTAIN_COLOR_THEMES: Final[dict[DarkTheme | LightTheme, MountainColors]] = {
    DarkTheme.MIDNIGHT_ICE: MountainColors(dark_mode=True,
                                           background_color="#142331",
                                           track_color="#A8DADC",
                                           peak_color="#F1F4EF"),
    DarkTheme.SLATE_CITRUS: MountainColors(dark_mode=True,
                                          background_color="#252C35",
                                          track_color="#DDE2E5",
                                          peak_color="#D4EB83"),
    LightTheme.WARM_MINIMAL: MountainColors(dark_mode=False,
                                           background_color="#F5F2EB",
                                           track_color="#252A2D",
                                           peak_color="#BC6048"),
    LightTheme.ALPINE_SAGE: MountainColors(dark_mode=False,
                                          background_color="#F2F1E8",
                                          track_color="#284D43",
                                          peak_color="#955638",
                                          terrain_shadow_color="#A8B5A0"),
    LightTheme.SAND_COBALT: MountainColors(dark_mode=False,
                                          background_color="#EDE5D8",
                                          track_color="#3155C6",
                                          peak_color="#242D3C"),
    DarkTheme.BLACK_GREEN_YELLOW:  MountainColors(dark_mode=True,
                                                  background_color="#264653",
                                                  track_color="#2a9d8f",
                                                  peak_color="#e9c46a"),
    DarkTheme.BLACK_RED_WHITE: MountainColors(dark_mode=True,
                                              background_color="#393e41",
                                              track_color="#e94f37",
                                              peak_color="#f6f7eb"),
    DarkTheme.BLACK_BLUE_WHITE: MountainColors(dark_mode=True,
                                               background_color="#4a598c",
                                               track_color="#69a1f7",
                                               peak_color="#e1ebfb"),
    DarkTheme.BLUE_PURPLE_YELLOW: MountainColors(dark_mode=True,
                                                 background_color="#34447d",
                                                 track_color="#8390fa",
                                                 peak_color="#fac748"),
    LightTheme.YELLOW_GREEN_BLACK: MountainColors(dark_mode=False,
                                                  background_color="#e9c46a",
                                                  track_color="#2a9d8f",
                                                  peak_color="#264653"),
    LightTheme.WHITE_RED_BLACK: MountainColors(dark_mode=False,
                                               background_color="#bfdbf7",
                                               track_color="#f87060",
                                               peak_color="#102542"),
    LightTheme.WHITE_BLUE_BLACK: MountainColors(dark_mode=False,
                                                background_color="#cadcfc",
                                                track_color="#69a1f7",
                                                peak_color="#00246b"),
    LightTheme.YELLOW_RED_BLACK: MountainColors(dark_mode=False,
                                                background_color="#eaaa33",
                                                track_color="#840032",
                                                peak_color="#002642")
}
