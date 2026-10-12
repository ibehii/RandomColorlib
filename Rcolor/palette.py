"""Palette management for Rcolor.

Handles lazy loading, caching, validation, and precomputation of ANSI
escape codes from JSON data files, with support for custom palettes,
contrast guards, preset tones, and smooth gradients.
"""
from __future__ import annotations

import functools
import random
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

RESET: str = "\033[0m"


def _distance_sq(c1: Sequence[int], c2: Sequence[int]) -> int:
    """Calculate squared Euclidean distance between two RGB colors."""
    dr = c1[0] - c2[0]
    dg = c1[1] - c2[1]
    db = c1[2] - c2[2]
    return dr * dr + dg * dg + db * db


def _find_nearest_standard_index(
    rgb: Sequence[int],
    standard_rgbs: Sequence[Sequence[int]],
) -> int:
    """Return index of nearest standard ANSI color in RGB space."""
    best_idx = 0
    best_dist = _distance_sq(rgb, standard_rgbs[0])
    if best_dist == 0:
        return 0
    for idx in range(1, len(standard_rgbs)):
        dist = _distance_sq(rgb, standard_rgbs[idx])
        if dist < best_dist:
            best_dist = dist
            best_idx = idx
            if best_dist == 0:
                break
    return best_idx


def _srgb_channel_lum(val: int) -> float:
    s = val / 255.0
    return s / 12.92 if s <= 0.04045 else ((s + 0.055) / 1.055) ** 2.4


_SRGB_LUMINANCE_TABLE: Tuple[float, ...] = tuple(
    _srgb_channel_lum(i) for i in range(256)
)


def relative_luminance(rgb: Sequence[int]) -> float:
    """Calculate WCAG 2.1 relative luminance for an sRGB color (0.0 to 1.0).

    Args:
        rgb: 3-element sequence of integers in range 0-255.

    Returns:
        Relative luminance as a float between 0.0 (pure black) and 1.0 (pure white).
    """
    r_idx = max(0, min(255, int(rgb[0])))
    g_idx = max(0, min(255, int(rgb[1])))
    b_idx = max(0, min(255, int(rgb[2])))
    return (
        0.2126 * _SRGB_LUMINANCE_TABLE[r_idx]
        + 0.7152 * _SRGB_LUMINANCE_TABLE[g_idx]
        + 0.0722 * _SRGB_LUMINANCE_TABLE[b_idx]
    )


def contrast_ratio(rgb1: Sequence[int], rgb2: Sequence[int]) -> float:
    """Calculate WCAG contrast ratio between two RGB colors (1.0 to 21.0).

    Args:
        rgb1: First RGB color sequence (0-255).
        rgb2: Second RGB color sequence (0-255).

    Returns:
        Contrast ratio from 1.0 (identical) to 21.0 (black vs white).
    """
    l1 = relative_luminance(rgb1)
    l2 = relative_luminance(rgb2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


@functools.lru_cache(maxsize=256)
def _parse_hex_color(hex_str: str) -> Tuple[int, int, int]:
    """Parse and cache hex color strings like '#ff007f', '00f0ff', or '#fff'."""
    cleaned = hex_str.strip().lstrip("#")
    if len(cleaned) == 3:
        cleaned = "".join(ch * 2 for ch in cleaned)
    if len(cleaned) == 6:
        try:
            return (
                int(cleaned[0:2], 16),
                int(cleaned[2:4], 16),
                int(cleaned[4:6], 16),
            )
        except ValueError as err:
            raise ValueError(f"Invalid hex color string {hex_str!r}") from err

    raise ValueError(
        f"Invalid hex color string: {hex_str!r}. Expected '#RRGGBB', 'RRGGBB', or '#RGB'."
    )


def parse_color(c: Union[str, Sequence[int]]) -> Tuple[int, int, int]:
    """Parse hex color string or RGB sequence to (R, G, B) tuple.

    Args:
        c: Hex color like "#ff007f", "00f0ff", "#fff" or 3-int sequence (R, G, B).

    Returns:
        3-tuple of integers in range [0, 255].

    Raises:
        ValueError: If color format cannot be parsed.
    """
    if isinstance(c, str):
        return _parse_hex_color(c)

    if isinstance(c, (list, tuple)) and len(c) == 3:
        try:
            return (int(c[0]), int(c[1]), int(c[2]))
        except (ValueError, TypeError) as err:
            raise ValueError(f"Invalid RGB sequence {c!r}") from err

    raise ValueError(
        f"Invalid color format: {c!r}. Expected hex string (e.g. '#ff007f') or (R, G, B) tuple."
    )


def interpolate_rgb(
    c1: Sequence[int], c2: Sequence[int], t: float
) -> Tuple[int, int, int]:
    """Linearly interpolate between two RGB colors.

    Args:
        c1: Starting RGB color.
        c2: Ending RGB color.
        t: Progress from 0.0 to 1.0.

    Returns:
        Interpolated (R, G, B) tuple.
    """
    if t <= 0.0:
        return (c1[0], c1[1], c1[2])
    if t >= 1.0:
        return (c2[0], c2[1], c2[2])
    return (
        int(round(c1[0] + (c2[0] - c1[0]) * t)),
        int(round(c1[1] + (c2[1] - c1[1]) * t)),
        int(round(c1[2] + (c2[2] - c1[2]) * t)),
    )


def interpolate_multi(
    stops: Sequence[Sequence[int]], t: float
) -> Tuple[int, int, int]:
    """Interpolate across a multi-stop color gradient.

    Args:
        stops: Sequence of at least one RGB color stop.
        t: Progress from 0.0 to 1.0.

    Returns:
        Interpolated (R, G, B) tuple.
    """
    if not stops:
        return (255, 255, 255)
    if len(stops) == 1:
        return (stops[0][0], stops[0][1], stops[0][2])

    t = max(0.0, min(1.0, float(t)))
    num_segments = len(stops) - 1
    scaled = t * num_segments
    idx = int(scaled)
    if idx >= num_segments:
        return (stops[-1][0], stops[-1][1], stops[-1][2])

    seg_t = scaled - idx
    return interpolate_rgb(stops[idx], stops[idx + 1], seg_t)


# Built-in gradient stop presets
GRADIENT_PRESETS: Dict[str, Tuple[Tuple[int, int, int], ...]] = {
    "rainbow": (
        (255, 0, 0),      # Red
        (255, 127, 0),    # Orange
        (255, 255, 0),    # Yellow
        (0, 255, 0),      # Green
        (0, 255, 255),    # Cyan
        (0, 0, 255),      # Blue
        (139, 0, 255),    # Violet
        (255, 0, 128),    # Pink
    ),
    "neon": (
        (0, 240, 255),    # Electric Cyan
        (176, 0, 255),    # Electric Purple
        (255, 0, 128),    # Neon Pink
    ),
    "sunset": (
        (128, 0, 255),    # Deep Violet
        (255, 0, 128),    # Magenta
        (255, 128, 0),    # Orange
        (255, 255, 0),    # Yellow
    ),
    "warm": (
        (255, 0, 0),      # Red
        (255, 95, 0),     # Orange Red
        (255, 175, 0),    # Amber
        (255, 255, 0),    # Yellow
    ),
    "cool": (
        (0, 50, 255),     # Deep Blue
        (0, 175, 255),    # Dodger Blue
        (0, 255, 255),    # Cyan
        (127, 255, 212),  # Aquamarine
    ),
    "pastel": (
        (255, 179, 186),  # Pastel Pink
        (255, 223, 186),  # Pastel Peach
        (255, 255, 186),  # Pastel Yellow
        (186, 255, 201),  # Pastel Green
        (186, 225, 255),  # Pastel Blue
    ),
    "cyberpunk": (
        (255, 0, 127),    # Hot Pink
        (0, 240, 255),    # Neon Cyan
        (255, 230, 0),    # Neon Yellow
    ),
    "ocean": (
        (10, 25, 47),     # Midnight Navy
        (0, 128, 255),    # Ocean Blue
        (0, 255, 200),    # Seafoam Green
    ),
}


class Palette:
    """Immutable, precomputed palette storing ANSI escape sequences."""

    __slots__ = (
        "_standard_fg_codes",
        "_standard_bg_codes",
        "_extended_fg_codes",
        "_extended_bg_codes",
        "_style_codes",
        "_styles_map",
        "_map_256_to_16_fg",
        "_map_256_to_16_bg",
        "_standard_rgbs",
        "_extended_rgbs",
        "_standard_luminances",
        "_extended_luminances",
        "_tones",
        "_tone_extended_fg",
        "_tone_extended_bg",
        "_tone_standard_fg",
        "_tone_standard_bg",
        "_raw_data",
    )

    def __init__(self, data: Dict[str, Any]) -> None:
        validate_palette_dict(data)
        self._raw_data = data

        # Precompute standard escape sequences and RGBs
        std_list: List[Dict[str, Any]] = data["standard"]
        std_fg: List[str] = [f"\033[{item['fg']}m" for item in std_list]
        std_bg: List[str] = [f"\033[{item['bg']}m" for item in std_list]
        self._standard_fg_codes: Tuple[str, ...] = tuple(std_fg)
        self._standard_bg_codes: Tuple[str, ...] = tuple(std_bg)

        std_rgbs: List[Tuple[int, int, int]] = [
            tuple(item.get("rgb", (0, 0, 0))) for item in std_list  # type: ignore
        ]
        self._standard_rgbs: Tuple[Tuple[int, int, int], ...] = tuple(std_rgbs)
        self._standard_luminances: Tuple[float, ...] = tuple(
            relative_luminance(rgb) for rgb in self._standard_rgbs
        )

        # Precompute extended 256 escape sequences and RGBs
        ext_list: List[Dict[str, Any]] = data["extended"]
        ext_fg: List[str] = [f"\033[38;5;{item['id']}m" for item in ext_list]
        ext_bg: List[str] = [f"\033[48;5;{item['id']}m" for item in ext_list]
        self._extended_fg_codes: Tuple[str, ...] = tuple(ext_fg)
        self._extended_bg_codes: Tuple[str, ...] = tuple(ext_bg)

        ext_rgbs: List[Tuple[int, int, int]] = [
            tuple(item.get("rgb", (0, 0, 0))) for item in ext_list  # type: ignore
        ]
        self._extended_rgbs: Tuple[Tuple[int, int, int], ...] = tuple(ext_rgbs)
        self._extended_luminances: Tuple[float, ...] = tuple(
            relative_luminance(rgb) for rgb in self._extended_rgbs
        )

        # Precompute styles
        styles_dict: Dict[str, Any] = data.get("styles", {})
        self._styles_map: Dict[str, str] = {
            k: f"\033[{v}m" for k, v in styles_dict.items()
        }
        self._style_codes: Tuple[str, ...] = tuple(self._styles_map.values())

        # Precompute 256 to 16 downgrading maps
        map_fg: List[str] = []
        map_bg: List[str] = []
        for ext_item in ext_list:
            rgb = ext_item.get("rgb")
            if rgb is not None and len(std_rgbs) > 0:
                nearest_idx = _find_nearest_standard_index(rgb, std_rgbs)
            else:
                nearest_idx = ext_item.get("id", 0) % len(std_list)
            map_fg.append(self._standard_fg_codes[nearest_idx])
            map_bg.append(self._standard_bg_codes[nearest_idx])

        self._map_256_to_16_fg: Tuple[str, ...] = tuple(map_fg)
        self._map_256_to_16_bg: Tuple[str, ...] = tuple(map_bg)

        # Precompute preset tones
        raw_tones: Dict[str, List[int]] = data.get("tones", {})
        self._tones: Dict[str, Tuple[int, ...]] = {}
        self._tone_extended_fg: Dict[str, Tuple[str, ...]] = {}
        self._tone_extended_bg: Dict[str, Tuple[str, ...]] = {}
        self._tone_standard_fg: Dict[str, Tuple[str, ...]] = {}
        self._tone_standard_bg: Dict[str, Tuple[str, ...]] = {}

        for tone_name, ids in raw_tones.items():
            valid_ids = [i for i in ids if 0 <= i < len(self._extended_fg_codes)]
            if valid_ids:
                norm_name = tone_name.lower().strip()
                self._tones[norm_name] = tuple(valid_ids)
                self._tone_extended_fg[norm_name] = tuple(
                    self._extended_fg_codes[i] for i in valid_ids
                )
                self._tone_extended_bg[norm_name] = tuple(
                    self._extended_bg_codes[i] for i in valid_ids
                )
                self._tone_standard_fg[norm_name] = tuple(
                    self._map_256_to_16_fg[i] for i in valid_ids
                )
                self._tone_standard_bg[norm_name] = tuple(
                    self._map_256_to_16_bg[i] for i in valid_ids
                )

    @property
    def standard_fg_codes(self) -> Tuple[str, ...]:
        """Precomputed standard foreground escape sequences."""
        return self._standard_fg_codes

    @property
    def standard_bg_codes(self) -> Tuple[str, ...]:
        """Precomputed standard background escape sequences."""
        return self._standard_bg_codes

    @property
    def extended_fg_codes(self) -> Tuple[str, ...]:
        """Precomputed extended (256-color) foreground escape sequences."""
        return self._extended_fg_codes

    @property
    def extended_bg_codes(self) -> Tuple[str, ...]:
        """Precomputed extended (256-color) background escape sequences."""
        return self._extended_bg_codes

    @property
    def style_codes(self) -> Tuple[str, ...]:
        """Precomputed style escape sequences."""
        return self._style_codes

    @property
    def styles_map(self) -> Dict[str, str]:
        """Mapping from style name to escape sequence."""
        return dict(self._styles_map)

    @property
    def map_256_to_16_fg(self) -> Tuple[str, ...]:
        """Lookup table mapping extended color index to nearest standard FG code."""
        return self._map_256_to_16_fg

    @property
    def map_256_to_16_bg(self) -> Tuple[str, ...]:
        """Lookup table mapping extended color index to nearest standard BG code."""
        return self._map_256_to_16_bg

    @property
    def standard_rgbs(self) -> Tuple[Tuple[int, int, int], ...]:
        """Precomputed RGB values for standard 16 ANSI colors."""
        return self._standard_rgbs

    @property
    def extended_rgbs(self) -> Tuple[Tuple[int, int, int], ...]:
        """Precomputed RGB values for extended 256 colors."""
        return self._extended_rgbs

    @property
    def standard_luminances(self) -> Tuple[float, ...]:
        """Precomputed relative luminance for standard colors."""
        return self._standard_luminances

    @property
    def extended_luminances(self) -> Tuple[float, ...]:
        """Precomputed relative luminance for extended colors."""
        return self._extended_luminances

    @property
    def tones(self) -> Dict[str, Tuple[int, ...]]:
        """Available preset tone names and their associated color index IDs."""
        return dict(self._tones)

    @property
    def raw_data(self) -> Dict[str, Any]:
        """Underlying raw dictionary representation."""
        return self._raw_data

    @functools.lru_cache(maxsize=1024)
    def _get_contrasting_candidates(
        self,
        bg_idx: int,
        min_contrast: float = 4.0,
        is_standard: bool = False,
    ) -> Tuple[Tuple[int, ...], int]:
        """Precompute or retrieve contrasting candidates for a background index."""
        lums = self._standard_luminances if is_standard else self._extended_luminances
        bg_lum = lums[bg_idx % len(lums)]
        candidates: List[int] = []
        best_ratio = 1.0
        best_idx = 0

        for idx, fg_lum in enumerate(lums):
            lighter = max(fg_lum, bg_lum)
            darker = min(fg_lum, bg_lum)
            ratio = (lighter + 0.05) / (darker + 0.05)
            if ratio >= min_contrast:
                candidates.append(idx)
            if ratio > best_ratio:
                best_ratio = ratio
                best_idx = idx

        return tuple(candidates), best_idx

    def get_contrasting_fg_code(
        self,
        bg_idx: int,
        min_contrast: float = 4.0,
        is_standard: bool = False,
    ) -> str:
        """Select a foreground color code that guarantees readable contrast against a background.

        Uses WCAG contrast ratio calculation against precomputed color luminances.

        Args:
            bg_idx: Index of the selected background color.
            min_contrast: Minimum WCAG contrast ratio (default 4.0).
            is_standard: If True, uses standard 16 ANSI codes; otherwise extended 256 codes.

        Returns:
            ANSI escape code string for the contrasting foreground color.
        """
        codes = self._standard_fg_codes if is_standard else self._extended_fg_codes
        candidates, best_idx = self._get_contrasting_candidates(
            bg_idx, min_contrast, is_standard
        )
        if candidates:
            return codes[random.choice(candidates)]
        return codes[best_idx]

    def get_tone_codes(
        self,
        tone: str,
        is_bg: bool = False,
        is_standard: bool = False,
    ) -> Tuple[str, ...]:
        """Retrieve precomputed ANSI escape codes for a preset tone.

        Args:
            tone: Name of the tone (e.g. 'neon', 'pastel', 'warm', 'cool').
            is_bg: True for background codes, False for foreground codes.
            is_standard: True for standard 16 ANSI codes, False for 256 colors.

        Returns:
            Tuple of ANSI escape sequences for the tone.

        Raises:
            ValueError: If the tone name is not recognized.
        """
        norm = tone.lower().strip()
        if is_standard:
            mapping = self._tone_standard_bg if is_bg else self._tone_standard_fg
        else:
            mapping = self._tone_extended_bg if is_bg else self._tone_extended_fg

        if norm not in mapping:
            available = ", ".join(sorted(self._tones.keys()))
            raise ValueError(
                f"Unknown tone {tone!r}. Available tones: {available}"
            )
        return mapping[norm]

    @functools.lru_cache(maxsize=1024)
    def find_nearest_256_code(self, rgb: Tuple[int, int, int]) -> str:
        """Find nearest 256-color ANSI escape code for given RGB color."""
        best_idx = 0
        best_dist = _distance_sq(rgb, self._extended_rgbs[0])
        if best_dist == 0:
            return self._extended_fg_codes[0]
        for idx in range(1, len(self._extended_rgbs)):
            dist = _distance_sq(rgb, self._extended_rgbs[idx])
            if dist < best_dist:
                best_dist = dist
                best_idx = idx
                if best_dist == 0:
                    break
        return self._extended_fg_codes[best_idx]

    @functools.lru_cache(maxsize=256)
    def find_nearest_16_fg(self, rgb: Tuple[int, int, int]) -> str:
        """Find nearest standard 16 ANSI foreground escape code for given RGB color."""
        idx = _find_nearest_standard_index(rgb, self._standard_rgbs)
        return self._standard_fg_codes[idx]


def validate_palette_dict(data: Any) -> None:
    """Validate that the palette dictionary conforms to the expected schema.

    Raises:
        ValueError: If data structure or required fields are missing or invalid.
    """
    if not isinstance(data, dict):
        raise ValueError(f"Palette data must be a dict, got {type(data).__name__}")

    if "schema_version" not in data:
        raise ValueError("Palette data missing required 'schema_version' field")

    if not isinstance(data["schema_version"], int):
        raise ValueError("'schema_version' must be an integer")

    if "standard" not in data or not isinstance(data["standard"], list):
        raise ValueError("Palette data missing required 'standard' color list")

    if len(data["standard"]) == 0:
        raise ValueError("'standard' color list must not be empty")

    for i, item in enumerate(data["standard"]):
        if not isinstance(item, dict):
            raise ValueError(f"standard[{i}] must be a dict")
        if "fg" not in item or not isinstance(item["fg"], int):
            raise ValueError(f"standard[{i}] must have integer 'fg' field")
        if "bg" not in item or not isinstance(item["bg"], int):
            raise ValueError(f"standard[{i}] must have integer 'bg' field")

    if "extended" not in data or not isinstance(data["extended"], list):
        raise ValueError("Palette data missing required 'extended' color list")

    if len(data["extended"]) == 0:
        raise ValueError("'extended' color list must not be empty")

    for i, item in enumerate(data["extended"]):
        if not isinstance(item, dict):
            raise ValueError(f"extended[{i}] must be a dict")
        if "id" not in item or not isinstance(item["id"], int):
            raise ValueError(f"extended[{i}] must have integer 'id' field")

    if "styles" in data and not isinstance(data["styles"], dict):
        raise ValueError("'styles' must be a dictionary")

    if "tones" in data:
        if not isinstance(data["tones"], dict):
            raise ValueError("'tones' must be a dictionary")
        for tone_name, ids in data["tones"].items():
            if not isinstance(ids, list) or not all(isinstance(x, int) for x in ids):
                raise ValueError(
                    f"Tone '{tone_name}' must contain a list of integer color IDs"
                )


def _read_default_palette_raw() -> Dict[str, Any]:
    """Read the default colors.json from package resources or filesystem."""
    import json

    # 1. Try importlib.resources (Python 3.9+ files API)
    try:
        import importlib.resources as pkg_resources

        if hasattr(pkg_resources, "files"):
            ref = pkg_resources.files("Rcolor").joinpath("data", "colors.json")
            text = ref.read_text(encoding="utf-8")
            return json.loads(text)
        elif hasattr(pkg_resources, "read_text"):
            text = pkg_resources.read_text("Rcolor.data", "colors.json")
            return json.loads(text)
    except Exception:
        pass

    # 2. Try pkgutil.get_data (Python 3.6 - 3.8 / zip support)
    try:
        import pkgutil

        raw = pkgutil.get_data("Rcolor", "data/colors.json")
        if raw is not None:
            return json.loads(raw.decode("utf-8"))
    except Exception:
        pass

    # 3. Direct filesystem path fallback
    fallback_path = Path(__file__).parent / "data" / "colors.json"
    if fallback_path.is_file():
        with open(fallback_path, "r", encoding="utf-8") as f:
            return json.load(f)

    raise FileNotFoundError(
        "Could not find 'colors.json' in Rcolor package resources or filesystem."
    )


_CURRENT_PALETTE: Optional[Palette] = None


def get_palette() -> Palette:
    """Return the active Palette instance, loading default lazily if needed."""
    global _CURRENT_PALETTE
    if _CURRENT_PALETTE is None:
        raw_data = _read_default_palette_raw()
        _CURRENT_PALETTE = Palette(raw_data)
    return _CURRENT_PALETTE


def load_palette(source: Union[str, Path, Dict[str, Any]]) -> Palette:
    """Load and activate a custom palette from a JSON file path or dictionary.

    Args:
        source: Path to a JSON palette file or a dictionary adhering to the palette schema.

    Returns:
        The newly activated Palette instance.

    Raises:
        FileNotFoundError: If the specified palette file does not exist.
        ValueError: If the palette schema is invalid or cannot be parsed.
    """
    global _CURRENT_PALETTE
    import json

    if isinstance(source, (str, Path)):
        p = Path(source)
        if not p.is_file():
            raise FileNotFoundError(f"Palette file not found: {source}")
        try:
            with open(p, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as err:
            raise ValueError(f"Corrupted JSON in palette file {source}: {err}") from err
    elif isinstance(source, dict):
        data = source
    else:
        raise ValueError(
            f"Expected filepath or dict for palette source, got {type(source).__name__}"
        )

    palette = Palette(data)
    _CURRENT_PALETTE = palette
    return _CURRENT_PALETTE


def reset_palette() -> None:
    """Reset the active palette to None so default will be reloaded on next access."""
    global _CURRENT_PALETTE
    _CURRENT_PALETTE = None
