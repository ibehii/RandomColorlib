"""Rcolor - Python library for colorful terminal output.

Supports 256 colors, ANSI standard 16 colors, font styles, per-character
rainbow text, automatic terminal capability detection, custom JSON palettes,
readability contrast guards, preset tones (neon, pastel, warm, cool), and
smooth gradients.
"""
from __future__ import annotations

from .palette import (
    GRADIENT_PRESETS,
    RESET,
    Palette,
    contrast_ratio,
    get_palette,
    load_palette,
    relative_luminance,
    reset_palette,
)
from .rcolor import (
    auto_bg,
    auto_fg,
    background,
    background_style,
    colors_path,
    data_path,
    foreground,
    foreground_background,
    foreground_background_style,
    foreground_style,
    gradient_fg,
    gradient_rainbow,
    rainbow_fg,
    standard_bg,
    standard_fg,
    standard_rainbow_fg,
    strip_color,
    style,
)
from .terminal import ColorLevel, detect_color_level, get_color_level, set_color_level

__version__ = "3.1.0"

__all__ = [
    "foreground",
    "standard_fg",
    "background",
    "standard_bg",
    "style",
    "auto_fg",
    "auto_bg",
    "foreground_background",
    "foreground_style",
    "foreground_background_style",
    "background_style",
    "rainbow_fg",
    "standard_rainbow_fg",
    "gradient_fg",
    "gradient_rainbow",
    "contrast_ratio",
    "relative_luminance",
    "strip_color",
    "GRADIENT_PRESETS",
    "load_palette",
    "reset_palette",
    "get_palette",
    "Palette",
    "detect_color_level",
    "get_color_level",
    "set_color_level",
    "ColorLevel",
    "RESET",
    "colors_path",
    "data_path",
    "__version__",
]