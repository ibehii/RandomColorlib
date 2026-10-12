"""Tests for Rcolor.palette module."""
import json
import os
import tempfile
import unittest

from Rcolor.palette import (
    Palette,
    get_palette,
    load_palette,
    reset_palette,
    validate_palette_dict,
)


class TestPalette(unittest.TestCase):
    """Test palette loading, validation, and ANSI sequence precomputations."""

    def tearDown(self) -> None:
        reset_palette()

    def test_default_palette_lazy_loading(self) -> None:
        palette = get_palette()
        self.assertIsInstance(palette, Palette)
        # Verify 16 standard colors
        self.assertEqual(len(palette.standard_fg_codes), 16)
        self.assertEqual(len(palette.standard_bg_codes), 16)
        # Verify all 256 extended colors
        self.assertEqual(len(palette.extended_fg_codes), 256)
        self.assertEqual(len(palette.extended_bg_codes), 256)
        # Verify styles
        self.assertGreaterEqual(len(palette.style_codes), 4)
        self.assertIn("\033[1m", palette.style_codes)  # bold
        self.assertIn("\033[4m", palette.style_codes)  # underline

    def test_extended_color_boundaries(self) -> None:
        palette = get_palette()
        # Extended color 0 (black) and 255 (grey)
        self.assertEqual(palette.extended_fg_codes[0], "\033[38;5;0m")
        self.assertEqual(palette.extended_fg_codes[255], "\033[38;5;255m")
        self.assertEqual(palette.extended_bg_codes[0], "\033[48;5;0m")
        self.assertEqual(palette.extended_bg_codes[255], "\033[48;5;255m")

    def test_precomputed_downgrade_map(self) -> None:
        palette = get_palette()
        self.assertEqual(len(palette.map_256_to_16_fg), 256)
        self.assertEqual(len(palette.map_256_to_16_bg), 256)
        # Color 0 (black: 0,0,0) should downgrade to standard black \033[30m
        self.assertEqual(palette.map_256_to_16_fg[0], "\033[30m")
        self.assertEqual(palette.map_256_to_16_bg[0], "\033[40m")
        # Every entry in map_256_to_16_fg should be in standard_fg_codes
        for fg in palette.map_256_to_16_fg:
            self.assertIn(fg, palette.standard_fg_codes)

    def test_validate_palette_valid(self) -> None:
        valid_data = {
            "schema_version": 1,
            "standard": [{"id": 0, "name": "red", "fg": 31, "bg": 41, "rgb": [255, 0, 0]}],
            "extended": [{"id": 0, "name": "red", "hex": "#ff0000", "rgb": [255, 0, 0]}],
            "styles": {"bold": 1},
        }
        # Should not raise
        validate_palette_dict(valid_data)

    def test_validate_palette_invalid_schema(self) -> None:
        # Non-dict
        with self.assertRaises(ValueError):
            validate_palette_dict("not-a-dict")

        # Missing schema_version
        with self.assertRaises(ValueError):
            validate_palette_dict({"standard": [], "extended": []})

        # Missing standard
        with self.assertRaises(ValueError):
            validate_palette_dict({"schema_version": 1, "extended": [{"id": 0}]})

        # Empty standard
        with self.assertRaises(ValueError):
            validate_palette_dict({"schema_version": 1, "standard": [], "extended": [{"id": 0}]})

        # Missing extended
        with self.assertRaises(ValueError):
            validate_palette_dict({
                "schema_version": 1,
                "standard": [{"fg": 31, "bg": 41}],
            })

    def test_load_custom_palette_from_dict(self) -> None:
        custom_data = {
            "schema_version": 1,
            "standard": [
                {"id": 0, "name": "blue", "fg": 34, "bg": 44, "rgb": [0, 0, 255]},
            ],
            "extended": [
                {"id": 10, "name": "light_blue", "rgb": [50, 50, 255]},
            ],
            "styles": {"bold": 1},
        }
        custom_palette = load_palette(custom_data)
        self.assertEqual(len(custom_palette.standard_fg_codes), 1)
        self.assertEqual(custom_palette.standard_fg_codes[0], "\033[34m")
        # Global get_palette() should return the newly loaded custom palette
        self.assertIs(get_palette(), custom_palette)

    def test_load_custom_palette_from_file(self) -> None:
        custom_data = {
            "schema_version": 1,
            "standard": [
                {"id": 0, "name": "green", "fg": 32, "bg": 42, "rgb": [0, 255, 0]},
            ],
            "extended": [
                {"id": 2, "name": "green", "rgb": [0, 255, 0]},
            ],
            "styles": {"dim": 2},
        }
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".json") as tmp:
            json.dump(custom_data, tmp)
            tmp_path = tmp.name

        try:
            palette = load_palette(tmp_path)
            self.assertEqual(palette.standard_fg_codes[0], "\033[32m")
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_load_custom_palette_missing_file(self) -> None:
        with self.assertRaises(FileNotFoundError):
            load_palette("/nonexistent/file/path/colors.json")

    def test_load_custom_palette_corrupt_file(self) -> None:
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".json") as tmp:
            tmp.write("{ invalid json")
            tmp_path = tmp.name

        try:
            with self.assertRaises(ValueError):
                load_palette(tmp_path)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_lazy_loading_verification(self) -> None:
        import Rcolor.palette
        reset_palette()
        self.assertIsNone(Rcolor.palette._CURRENT_PALETTE)
        # Accessing get_palette() triggers the lazy load
        palette = Rcolor.palette.get_palette()
        self.assertIsNotNone(palette)
        self.assertIs(Rcolor.palette._CURRENT_PALETTE, palette)

    def test_schema_inner_field_validation(self) -> None:
        # standard item without 'fg'
        with self.assertRaises(ValueError):
            validate_palette_dict({
                "schema_version": 1,
                "standard": [{"bg": 40}],
                "extended": [{"id": 0}],
            })

        # standard item with non-int 'bg'
        with self.assertRaises(ValueError):
            validate_palette_dict({
                "schema_version": 1,
                "standard": [{"fg": 30, "bg": "40"}],
                "extended": [{"id": 0}],
            })

        # extended item without 'id'
        with self.assertRaises(ValueError):
            validate_palette_dict({
                "schema_version": 1,
                "standard": [{"fg": 30, "bg": 40}],
                "extended": [{"name": "black"}],
            })

    def test_palette_tones_loading(self) -> None:
        palette = get_palette()
        self.assertIn("neon", palette.tones)
        self.assertIn("pastel", palette.tones)
        self.assertIn("warm", palette.tones)
        self.assertIn("cool", palette.tones)

        neon_fg = palette.get_tone_codes("neon", is_bg=False)
        self.assertGreater(len(neon_fg), 0)
        self.assertTrue(all(isinstance(c, str) for c in neon_fg))

        neon_bg = palette.get_tone_codes("neon", is_bg=True)
        self.assertGreater(len(neon_bg), 0)

        # Standard 16 tone mapping
        neon_std_fg = palette.get_tone_codes("neon", is_bg=False, is_standard=True)
        self.assertGreater(len(neon_std_fg), 0)

        # Unknown tone
        with self.assertRaises(ValueError):
            palette.get_tone_codes("unknown_tone_xyz")

    def test_palette_contrast_guard_selection(self) -> None:
        from Rcolor.palette import contrast_ratio

        palette = get_palette()
        # Test on black background (idx 0, rgb [0,0,0])
        fg_code_for_black = palette.get_contrasting_fg_code(0, min_contrast=4.5)
        self.assertTrue(fg_code_for_black.startswith("\033[38;5;"))

        # Test on standard 16 black background (idx 0)
        std_fg_code = palette.get_contrasting_fg_code(0, min_contrast=4.5, is_standard=True)
        self.assertTrue(std_fg_code.startswith("\033["))

    def test_parse_color_helper(self) -> None:
        from Rcolor.palette import parse_color

        self.assertEqual(parse_color("#ff0000"), (255, 0, 0))
        self.assertEqual(parse_color("00ff00"), (0, 255, 0))
        self.assertEqual(parse_color("#00f"), (0, 0, 255))
        self.assertEqual(parse_color((128, 64, 32)), (128, 64, 32))
        self.assertEqual(parse_color([10, 20, 30]), (10, 20, 30))

        with self.assertRaises(ValueError):
            parse_color("invalid_hex")

        with self.assertRaises(ValueError):
            parse_color([1, 2])

    def test_interpolation_helpers(self) -> None:
        from Rcolor.palette import interpolate_multi, interpolate_rgb

        c1 = (0, 0, 0)
        c2 = (100, 200, 50)
        mid = interpolate_rgb(c1, c2, 0.5)
        self.assertEqual(mid, (50, 100, 25))

        stops = [(0, 0, 0), (100, 100, 100), (200, 200, 200)]
        self.assertEqual(interpolate_multi(stops, 0.0), (0, 0, 0))
        self.assertEqual(interpolate_multi(stops, 0.5), (100, 100, 100))
        self.assertEqual(interpolate_multi(stops, 1.0), (200, 200, 200))


if __name__ == "__main__":
    unittest.main()
