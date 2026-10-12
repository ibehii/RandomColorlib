"""Random Color library (Rcolor).

Provides fast, terminal-aware functions to style console output with random
foreground/background colors, text formatting, per-character rainbow effects,
readability contrast guards, preset tones, and smooth gradients.
"""
from __future__ import annotations

import random
import re
from pathlib import Path
from typing import Any, Optional, Sequence, Tuple, Union

from .palette import (
    GRADIENT_PRESETS,
    RESET,
    Palette,
    contrast_ratio,
    get_palette,
    interpolate_multi,
    interpolate_rgb,
    load_palette,
    parse_color,
    relative_luminance,
    reset_palette,
)
from .terminal import ColorLevel, detect_color_level, get_color_level, set_color_level

# Backward-compatible path reference (now points to package data folder)
data_path: Path = Path(__file__).parent / "data"
colors_path: Path = data_path

_ANSI_REGEX: re.Pattern[str] = re.compile(r"\033\[[0-9;]*[a-zA-Z]")

__all__ = [
    "foreground",
    "background",
    "style",
    "rainbow_fg",
    "standard_fg",
    "standard_bg",
    "standard_rainbow_fg",
    "auto_fg",
    "auto_bg",
    "foreground_background",
    "foreground_style",
    "background_style",
    "foreground_background_style",
    "gradient_fg",
    "gradient_rainbow",
    "contrast_ratio",
    "relative_luminance",
    "strip_color",
    "load_palette",
    "reset_palette",
    "detect_color_level",
    "get_color_level",
    "set_color_level",
    "ColorLevel",
    "RESET",
]


def strip_color(text: Any) -> str:
    """Remove all ANSI color and style escape sequences from a string.

    Args:
        text: String containing ANSI escape sequences (or stringifiable object).

    Returns:
        Clean plain text string without ANSI codes.
    """
    if text is None:
        return ""
    if not isinstance(text, str):
        text = str(text)
    return _ANSI_REGEX.sub("", text)


def _normalize_input(*user_input: Any) -> str:
    """Validate and stringify variable user inputs.

    Raises:
        TypeError: If an argument is of an unsupported type.
    """
    count = len(user_input)
    if count == 0:
        return ""
    if count == 1:
        item = user_input[0]
        if isinstance(item, str):
            return item
        if isinstance(item, (int, float, bool)):
            return str(item)
        raise TypeError(
            f"Unsupported input type '{type(item).__name__}'. "
            "Expected str, int, float, or bool."
        )

    parts: list[str] = []
    for item in user_input:
        if isinstance(item, str):
            parts.append(item)
        elif isinstance(item, (int, float, bool)):
            parts.append(str(item))
        else:
            raise TypeError(
                f"Unsupported input type '{type(item).__name__}'. "
                "Expected str, int, float, or bool."
            )
    return "".join(parts)


def foreground(*user_input: Any, tone: Optional[str] = None) -> str:
    """Apply a random foreground color from 256 colors with automatic terminal downgrade.

    Args:
        *user_input: Stringifiable elements to colorize.
        tone: Optional curated tone preset ('neon', 'pastel', 'warm', 'cool').

    Returns:
        ANSI-formatted string or plain text if colors are disabled.

    Raises:
        TypeError: If an input element cannot be safely formatted.
        ValueError: If an unrecognized tone name is supplied.
    """
    text = _normalize_input(*user_input)
    if not text:
        return ""

    level = get_color_level()
    if level == ColorLevel.NONE:
        return text

    palette = get_palette()
    if tone is not None:
        codes = palette.get_tone_codes(
            tone, is_bg=False, is_standard=(level == ColorLevel.ANSI16)
        )
        color = random.choice(codes)
        return f"{color}{text}{RESET}"

    idx = random.randrange(len(palette.extended_fg_codes))
    if level == ColorLevel.ANSI16:
        color = palette.map_256_to_16_fg[idx]
    else:
        color = palette.extended_fg_codes[idx]

    return f"{color}{text}{RESET}"


def background(*user_input: Any, tone: Optional[str] = None) -> str:
    """Apply a random background color from 256 colors with automatic terminal downgrade.

    Args:
        *user_input: Stringifiable elements to colorize.
        tone: Optional curated tone preset ('neon', 'pastel', 'warm', 'cool').

    Returns:
        ANSI-formatted string or plain text if colors are disabled.

    Raises:
        TypeError: If an input element cannot be safely formatted.
        ValueError: If an unrecognized tone name is supplied.
    """
    text = _normalize_input(*user_input)
    if not text:
        return ""

    level = get_color_level()
    if level == ColorLevel.NONE:
        return text

    palette = get_palette()
    if tone is not None:
        codes = palette.get_tone_codes(
            tone, is_bg=True, is_standard=(level == ColorLevel.ANSI16)
        )
        color = random.choice(codes)
        return f"{color}{text}{RESET}"

    idx = random.randrange(len(palette.extended_bg_codes))
    if level == ColorLevel.ANSI16:
        color = palette.map_256_to_16_bg[idx]
    else:
        color = palette.extended_bg_codes[idx]

    return f"{color}{text}{RESET}"


def standard_fg(*user_input: Any) -> str:
    """Apply a random standard foreground color (16 ANSI colors, universal terminal support).

    Args:
        *user_input: Stringifiable elements to colorize.

    Returns:
        ANSI-formatted string or plain text if colors are disabled.

    Raises:
        TypeError: If an input element cannot be safely formatted.
    """
    text = _normalize_input(*user_input)
    if not text:
        return ""

    level = get_color_level()
    if level == ColorLevel.NONE:
        return text

    palette = get_palette()
    color = random.choice(palette.standard_fg_codes)
    return f"{color}{text}{RESET}"


def standard_bg(*user_input: Any) -> str:
    """Apply a random standard background color (16 ANSI colors, universal terminal support).

    Args:
        *user_input: Stringifiable elements to colorize.

    Returns:
        ANSI-formatted string or plain text if colors are disabled.

    Raises:
        TypeError: If an input element cannot be safely formatted.
    """
    text = _normalize_input(*user_input)
    if not text:
        return ""

    level = get_color_level()
    if level == ColorLevel.NONE:
        return text

    palette = get_palette()
    color = random.choice(palette.standard_bg_codes)
    return f"{color}{text}{RESET}"


def style(*user_input: Any) -> str:
    """Apply a random text style (bold, dim, italic, underline, etc.).

    Args:
        *user_input: Stringifiable elements to format.

    Returns:
        ANSI-formatted string or plain text if formatting is disabled.

    Raises:
        TypeError: If an input element cannot be safely formatted.
    """
    text = _normalize_input(*user_input)
    if not text:
        return ""

    level = get_color_level()
    if level == ColorLevel.NONE:
        return text

    palette = get_palette()
    text_style = random.choice(palette.style_codes)
    return f"{text_style}{text}{RESET}"


def auto_fg(*user_input: Any, tone: Optional[str] = None) -> str:
    """Automatically detect terminal capability and apply optimal random foreground color.

    Chooses 256-color when supported, standard 16-color on restricted terminals,
    or plain text if output is redirected / NO_COLOR is active.

    Args:
        *user_input: Stringifiable elements to colorize.
        tone: Optional curated tone preset ('neon', 'pastel', 'warm', 'cool').

    Returns:
        ANSI-formatted string or plain text.
    """
    text = _normalize_input(*user_input)
    if not text:
        return ""

    level = get_color_level()
    if level == ColorLevel.NONE:
        return text

    palette = get_palette()
    if tone is not None:
        codes = palette.get_tone_codes(
            tone, is_bg=False, is_standard=(level == ColorLevel.ANSI16)
        )
        color = random.choice(codes)
        return f"{color}{text}{RESET}"

    if level == ColorLevel.ANSI16:
        color = random.choice(palette.standard_fg_codes)
    else:
        color = random.choice(palette.extended_fg_codes)

    return f"{color}{text}{RESET}"


def auto_bg(*user_input: Any, tone: Optional[str] = None) -> str:
    """Automatically detect terminal capability and apply optimal random background color.

    Chooses 256-color when supported, standard 16-color on restricted terminals,
    or plain text if output is redirected / NO_COLOR is active.

    Args:
        *user_input: Stringifiable elements to colorize.
        tone: Optional curated tone preset ('neon', 'pastel', 'warm', 'cool').

    Returns:
        ANSI-formatted string or plain text.
    """
    text = _normalize_input(*user_input)
    if not text:
        return ""

    level = get_color_level()
    if level == ColorLevel.NONE:
        return text

    palette = get_palette()
    if tone is not None:
        codes = palette.get_tone_codes(
            tone, is_bg=True, is_standard=(level == ColorLevel.ANSI16)
        )
        color = random.choice(codes)
        return f"{color}{text}{RESET}"

    if level == ColorLevel.ANSI16:
        color = random.choice(palette.standard_bg_codes)
    else:
        color = random.choice(palette.extended_bg_codes)

    return f"{color}{text}{RESET}"


def foreground_background(*user_input: Any, min_contrast: float = 4.0) -> str:
    """Apply both random foreground and background colors with a Contrast Guard for readability.

    Guarantees readable text by choosing a foreground color that achieves at least
    `min_contrast` WCAG contrast ratio against the chosen background.

    Args:
        *user_input: Stringifiable elements to colorize.
        min_contrast: Minimum WCAG contrast ratio (default 4.0).

    Returns:
        ANSI-formatted string or plain text.
    """
    text = _normalize_input(*user_input)
    if not text:
        return ""

    level = get_color_level()
    if level == ColorLevel.NONE:
        return text

    palette = get_palette()
    if level == ColorLevel.ANSI16:
        bg_idx = random.randrange(len(palette.standard_bg_codes))
        bg = palette.standard_bg_codes[bg_idx]
        fg = palette.get_contrasting_fg_code(
            bg_idx, min_contrast=min_contrast, is_standard=True
        )
    else:
        bg_idx = random.randrange(len(palette.extended_bg_codes))
        bg = palette.extended_bg_codes[bg_idx]
        fg = palette.get_contrasting_fg_code(
            bg_idx, min_contrast=min_contrast, is_standard=False
        )

    return f"{fg}{bg}{text}{RESET}"


def foreground_style(*user_input: Any) -> str:
    """Apply both random foreground color and text style in a single clean escape sequence.

    Args:
        *user_input: Stringifiable elements to style.

    Returns:
        ANSI-formatted string or plain text.
    """
    text = _normalize_input(*user_input)
    if not text:
        return ""

    level = get_color_level()
    if level == ColorLevel.NONE:
        return text

    palette = get_palette()
    if level == ColorLevel.ANSI16:
        fg = random.choice(palette.standard_fg_codes)
    else:
        fg = random.choice(palette.extended_fg_codes)
    st = random.choice(palette.style_codes)

    return f"{fg}{st}{text}{RESET}"


def background_style(*user_input: Any) -> str:
    """Apply both random background color and text style in a single clean escape sequence.

    Args:
        *user_input: Stringifiable elements to style.

    Returns:
        ANSI-formatted string or plain text.
    """
    text = _normalize_input(*user_input)
    if not text:
        return ""

    level = get_color_level()
    if level == ColorLevel.NONE:
        return text

    palette = get_palette()
    if level == ColorLevel.ANSI16:
        bg = random.choice(palette.standard_bg_codes)
    else:
        bg = random.choice(palette.extended_bg_codes)
    st = random.choice(palette.style_codes)

    return f"{bg}{st}{text}{RESET}"


def foreground_background_style(
    *user_input: Any, min_contrast: float = 4.0
) -> str:
    """Apply random foreground, background, and text style with a Contrast Guard for readability.

    Args:
        *user_input: Stringifiable elements to style.
        min_contrast: Minimum WCAG contrast ratio (default 4.0).

    Returns:
        ANSI-formatted string or plain text.
    """
    text = _normalize_input(*user_input)
    if not text:
        return ""

    level = get_color_level()
    if level == ColorLevel.NONE:
        return text

    palette = get_palette()
    if level == ColorLevel.ANSI16:
        bg_idx = random.randrange(len(palette.standard_bg_codes))
        bg = palette.standard_bg_codes[bg_idx]
        fg = palette.get_contrasting_fg_code(
            bg_idx, min_contrast=min_contrast, is_standard=True
        )
    else:
        bg_idx = random.randrange(len(palette.extended_bg_codes))
        bg = palette.extended_bg_codes[bg_idx]
        fg = palette.get_contrasting_fg_code(
            bg_idx, min_contrast=min_contrast, is_standard=False
        )
    st = random.choice(palette.style_codes)

    return f"{fg}{bg}{st}{text}{RESET}"


def rainbow_fg(user_input: Any) -> str:
    """Colorize each character with a random foreground color using O(N) optimized join.

    Args:
        user_input: Stringifiable object to convert to rainbow text.

    Returns:
        Per-character rainbow ANSI string or plain text.

    Raises:
        TypeError: If user_input is not a str, int, float, or bool.
    """
    if isinstance(user_input, str):
        text = user_input
    elif isinstance(user_input, (int, float, bool)):
        text = str(user_input)
    else:
        raise TypeError(
            f"Unsupported input type '{type(user_input).__name__}'. "
            "Expected str, int, float, or bool."
        )

    if not text:
        return ""

    level = get_color_level()
    if level == ColorLevel.NONE:
        return text

    palette = get_palette()
    if level == ColorLevel.ANSI16:
        codes = palette.standard_fg_codes
    else:
        codes = palette.extended_fg_codes

    return "".join(f"{random.choice(codes)}{ch}{RESET}" for ch in text)


def standard_rainbow_fg(user_input: Any) -> str:
    """Colorize each character with a random standard 16 ANSI foreground color.

    Args:
        user_input: Stringifiable object to convert to rainbow text.

    Returns:
        Per-character rainbow ANSI string or plain text.

    Raises:
        TypeError: If user_input is not a str, int, float, or bool.
    """
    if isinstance(user_input, str):
        text = user_input
    elif isinstance(user_input, (int, float, bool)):
        text = str(user_input)
    else:
        raise TypeError(
            f"Unsupported input type '{type(user_input).__name__}'. "
            "Expected str, int, float, or bool."
        )

    if not text:
        return ""

    level = get_color_level()
    if level == ColorLevel.NONE:
        return text

    palette = get_palette()
    codes = palette.standard_fg_codes

    return "".join(f"{random.choice(codes)}{ch}{RESET}" for ch in text)


def gradient_fg(
    user_input: Any,
    start: Union[str, Sequence[int]] = "#ff007f",
    end: Union[str, Sequence[int]] = "#00f0ff",
    preset: Optional[str] = None,
) -> str:
    """Apply a smooth, linear color gradient across characters with terminal capability awareness.

    Interpolates colors smoothly across the string. Output automatically uses:
      - 24-bit TrueColor (\033[38;2;R;G;Bm) on TrueColor terminals.
      - Nearest 256-color codes on 8-bit terminals.
      - Nearest 16-color ANSI codes on 4-bit terminals.
      - Plain text when redirected or NO_COLOR is active.

    Args:
        user_input: Stringifiable object to colorize.
        start: Starting color as hex (e.g. '#ff007f') or RGB tuple (R, G, B).
        end: Ending color as hex (e.g. '#00f0ff') or RGB tuple (R, G, B).
        preset: Optional gradient preset ('rainbow', 'neon', 'sunset', 'warm',
            'cool', 'pastel', 'cyberpunk', 'ocean').

    Returns:
        Smooth gradient styled ANSI string or plain text.

    Raises:
        TypeError: If user_input is not a str, int, float, or bool.
        ValueError: If a preset or color string is invalid.
    """
    if isinstance(user_input, str):
        text = user_input
    elif isinstance(user_input, (int, float, bool)):
        text = str(user_input)
    else:
        raise TypeError(
            f"Unsupported input type '{type(user_input).__name__}'. "
            "Expected str, int, float, or bool."
        )

    n = len(text)
    if n == 0:
        return ""

    level = get_color_level()
    if level == ColorLevel.NONE:
        return text

    if preset is not None:
        norm_preset = preset.lower().strip()
        if norm_preset not in GRADIENT_PRESETS:
            available = ", ".join(sorted(GRADIENT_PRESETS.keys()))
            raise ValueError(
                f"Unknown gradient preset {preset!r}. Available: {available}"
            )
        stops = GRADIENT_PRESETS[norm_preset]
    else:
        stops = (parse_color(start), parse_color(end))

    palette = get_palette()
    if n == 1:
        first_rgb = stops[0]
        if level == ColorLevel.TRUECOLOR:
            return f"\033[38;2;{first_rgb[0]};{first_rgb[1]};{first_rgb[2]}m{text}{RESET}"
        elif level == ColorLevel.ANSI256:
            code = palette.find_nearest_256_code(first_rgb)
            return f"{code}{text}{RESET}"
        else:
            code = palette.find_nearest_16_fg(first_rgb)
            return f"{code}{text}{RESET}"

    inv_n = 1.0 / (n - 1)
    is_two_stop = len(stops) == 2
    c1, c2 = (stops[0], stops[1]) if is_two_stop else ((0, 0, 0), (0, 0, 0))
    parts: list[str] = []

    if level == ColorLevel.TRUECOLOR:
        for i, ch in enumerate(text):
            t = i * inv_n
            r, g, b = interpolate_rgb(c1, c2, t) if is_two_stop else interpolate_multi(stops, t)
            parts.append(f"\033[38;2;{r};{g};{b}m{ch}")
    elif level == ColorLevel.ANSI256:
        for i, ch in enumerate(text):
            t = i * inv_n
            rgb = interpolate_rgb(c1, c2, t) if is_two_stop else interpolate_multi(stops, t)
            code = palette.find_nearest_256_code(rgb)
            parts.append(f"{code}{ch}")
    else:  # ColorLevel.ANSI16
        for i, ch in enumerate(text):
            t = i * inv_n
            rgb = interpolate_rgb(c1, c2, t) if is_two_stop else interpolate_multi(stops, t)
            code = palette.find_nearest_16_fg(rgb)
            parts.append(f"{code}{ch}")

    parts.append(RESET)
    return "".join(parts)


def gradient_rainbow(user_input: Any) -> str:
    """Apply a smooth, high-resolution multi-stop rainbow gradient across characters.

    Args:
        user_input: Stringifiable object to convert to smooth rainbow text.

    Returns:
        Smooth rainbow ANSI string or plain text.
    """
    return gradient_fg(user_input, preset="rainbow")