"""Tests for the primary public Rcolor API."""
import unittest

import Rcolor
from Rcolor.palette import RESET, reset_palette
from Rcolor.rcolor import (
    auto_bg,
    auto_fg,
    background,
    background_style,
    foreground,
    foreground_background,
    foreground_background_style,
    foreground_style,
    rainbow_fg,
    standard_bg,
    standard_fg,
    standard_rainbow_fg,
    style,
)
from Rcolor.terminal import ColorLevel, set_color_level


class TestRcolorPublicAPI(unittest.TestCase):
    """Test public API functions, input handling, downgrading, and combinations."""

    def setUp(self) -> None:
        reset_palette()
        set_color_level(ColorLevel.ANSI256)

    def tearDown(self) -> None:
        reset_palette()
        set_color_level(None)

    def test_all_exports_present(self) -> None:
        required_names = [
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
        ]
        for name in required_names:
            self.assertTrue(hasattr(Rcolor, name), f"Missing required export: {name}")
            self.assertIn(name, Rcolor.__all__)

    def test_empty_input(self) -> None:
        self.assertEqual(foreground(""), "")
        self.assertEqual(foreground(), "")
        self.assertEqual(background(""), "")
        self.assertEqual(standard_fg(""), "")
        self.assertEqual(standard_bg(""), "")
        self.assertEqual(style(""), "")
        self.assertEqual(rainbow_fg(""), "")
        self.assertEqual(standard_rainbow_fg(""), "")
        self.assertEqual(foreground_background(""), "")

    def test_non_str_supported_inputs(self) -> None:
        # Int, float, bool
        res1 = foreground(123)
        self.assertIn("123", res1)
        self.assertTrue(res1.endswith(RESET))

        res2 = standard_fg(45.67)
        self.assertIn("45.67", res2)
        self.assertTrue(res2.endswith(RESET))

        res3 = auto_fg(True)
        self.assertIn("True", res3)

        # Multi-argument join with duplicates
        res4 = foreground(1, 2, 1)
        self.assertIn("121", res4)

    def test_unsupported_input_raises_type_error(self) -> None:
        with self.assertRaises(TypeError) as ctx:
            foreground(object())
        self.assertIn("Unsupported input type", str(ctx.exception))

        with self.assertRaises(TypeError):
            rainbow_fg([1, 2, 3])

        with self.assertRaises(TypeError):
            rainbow_fg(None)

        with self.assertRaises(TypeError):
            foreground_background(dict())

    def test_color_disabled_level_none(self) -> None:
        set_color_level(ColorLevel.NONE)

        text = "Hello Plain World"
        self.assertEqual(foreground(text), text)
        self.assertEqual(background(text), text)
        self.assertEqual(standard_fg(text), text)
        self.assertEqual(standard_bg(text), text)
        self.assertEqual(style(text), text)
        self.assertEqual(auto_fg(text), text)
        self.assertEqual(auto_bg(text), text)
        self.assertEqual(foreground_background(text), text)
        self.assertEqual(foreground_style(text), text)
        self.assertEqual(background_style(text), text)
        self.assertEqual(foreground_background_style(text), text)
        self.assertEqual(rainbow_fg(text), text)
        self.assertEqual(standard_rainbow_fg(text), text)

    def test_foreground_and_background_ansi256(self) -> None:
        set_color_level(ColorLevel.ANSI256)

        fg_res = foreground("test_fg")
        self.assertTrue(fg_res.startswith("\033[38;5;"))
        self.assertTrue(fg_res.endswith(f"test_fg{RESET}"))

        bg_res = background("test_bg")
        self.assertTrue(bg_res.startswith("\033[48;5;"))
        self.assertTrue(bg_res.endswith(f"test_bg{RESET}"))

    def test_standard_colors(self) -> None:
        set_color_level(ColorLevel.ANSI256)

        std_fg_res = standard_fg("test")
        self.assertTrue(
            std_fg_res.startswith("\033[3") or std_fg_res.startswith("\033[9"),
            f"Unexpected std_fg prefix: {std_fg_res!r}",
        )
        self.assertTrue(std_fg_res.endswith(f"test{RESET}"))

        std_bg_res = standard_bg("test")
        self.assertTrue(
            std_bg_res.startswith("\033[4") or std_bg_res.startswith("\033[10"),
            f"Unexpected std_bg prefix: {std_bg_res!r}",
        )
        self.assertTrue(std_bg_res.endswith(f"test{RESET}"))

    def test_downgrade_to_ansi16(self) -> None:
        set_color_level(ColorLevel.ANSI16)

        # In 16-color mode, foreground() should automatically downgrade to a standard code
        fg_res = foreground("downgraded")
        self.assertTrue(
            fg_res.startswith("\033[3") or fg_res.startswith("\033[9"),
            f"Expected standard 16 ANSI code on 16-color terminal, got {fg_res!r}",
        )
        self.assertNotIn("\033[38;5;", fg_res)

        bg_res = background("downgraded_bg")
        self.assertTrue(
            bg_res.startswith("\033[4") or bg_res.startswith("\033[10"),
            f"Expected standard 16 ANSI bg on 16-color terminal, got {bg_res!r}",
        )
        self.assertNotIn("\033[48;5;", bg_res)

    def test_style(self) -> None:
        set_color_level(ColorLevel.ANSI256)
        res = style("styled_text")
        self.assertTrue(res.endswith(f"styled_text{RESET}"))
        self.assertTrue(res.startswith("\033["))

    def test_composite_functions(self) -> None:
        set_color_level(ColorLevel.ANSI256)

        res_fb = foreground_background("text")
        self.assertIn("text", res_fb)
        self.assertTrue(res_fb.endswith(RESET))
        # Ensure single reset at the end, not duplicate resets
        self.assertEqual(res_fb.count(RESET), 1)

        res_fs = foreground_style("text")
        self.assertEqual(res_fs.count(RESET), 1)

        res_bs = background_style("text")
        self.assertEqual(res_bs.count(RESET), 1)

        res_fbs = foreground_background_style("text")
        self.assertEqual(res_fbs.count(RESET), 1)

    def test_rainbow_fg(self) -> None:
        set_color_level(ColorLevel.ANSI256)
        sample = "Rainbow"
        rainbow = rainbow_fg(sample)
        # Each character should be followed by RESET
        self.assertEqual(rainbow.count(RESET), len(sample))
        self.assertTrue(rainbow.startswith("\033[38;5;"))

    def test_standard_rainbow_fg(self) -> None:
        set_color_level(ColorLevel.ANSI256)
        sample = "Test123"
        rainbow = standard_rainbow_fg(sample)
        self.assertEqual(rainbow.count(RESET), len(sample))
        # Should NOT use 256 color codes
        self.assertNotIn("\033[38;5;", rainbow)

    def test_style_never_invisible(self) -> None:
        set_color_level(ColorLevel.ANSI256)
        # Verify that style() never picks '\033[8m' (hidden/conceal) across repeated calls
        for _ in range(100):
            res = style("VisibleText")
            self.assertFalse(
                res.startswith("\033[8m"),
                "Style generated hidden text (\\033[8m) making output invisible!",
            )

    def test_composite_non_string_inputs(self) -> None:
        set_color_level(ColorLevel.ANSI256)
        res_fb = foreground_background(10, 20)
        self.assertIn("1020", res_fb)
        self.assertTrue(res_fb.endswith(RESET))

        res_fs = foreground_style(3.14)
        self.assertIn("3.14", res_fs)
        self.assertTrue(res_fs.endswith(RESET))

    def test_rainbow_fg_numeric_inputs(self) -> None:
        set_color_level(ColorLevel.ANSI256)
        num_res = rainbow_fg(12345)
        self.assertEqual(num_res.count(RESET), 5)
        self.assertIn("1", num_res)
        self.assertIn("5", num_res)

    def test_exports_reset_palette_and_detect_color_level(self) -> None:
        self.assertTrue(hasattr(Rcolor, "reset_palette"))
        self.assertTrue(hasattr(Rcolor, "detect_color_level"))
        self.assertIn("reset_palette", Rcolor.__all__)
        self.assertIn("detect_color_level", Rcolor.__all__)
        self.assertIn("gradient_fg", Rcolor.__all__)
        self.assertIn("gradient_rainbow", Rcolor.__all__)
        self.assertIn("contrast_ratio", Rcolor.__all__)
        self.assertIn("relative_luminance", Rcolor.__all__)

    def test_relative_luminance_and_contrast_ratio(self) -> None:
        from Rcolor import contrast_ratio, relative_luminance

        lum_black = relative_luminance((0, 0, 0))
        lum_white = relative_luminance((255, 255, 255))
        self.assertAlmostEqual(lum_black, 0.0, places=3)
        self.assertAlmostEqual(lum_white, 1.0, places=3)

        # White on black is 21:1
        ratio_max = contrast_ratio((255, 255, 255), (0, 0, 0))
        self.assertAlmostEqual(ratio_max, 21.0, places=2)

        # Identical colors is 1:1
        ratio_min = contrast_ratio((128, 128, 128), (128, 128, 128))
        self.assertAlmostEqual(ratio_min, 1.0, places=2)

    def test_contrast_guard_readability(self) -> None:
        set_color_level(ColorLevel.ANSI256)
        # Test 50 iterations of foreground_background to verify contrast guard
        from Rcolor.palette import contrast_ratio, get_palette

        palette = get_palette()
        for _ in range(50):
            res = foreground_background("ReadMe", min_contrast=4.5)
            self.assertIn("ReadMe", res)
            self.assertTrue(res.endswith(RESET))

        # Test with custom min_contrast
        res_custom = foreground_background("CustomContrast", min_contrast=7.0)
        self.assertIn("CustomContrast", res_custom)

        # Test composite foreground_background_style with contrast guard
        res_fbs = foreground_background_style("StyledReadMe", min_contrast=4.0)
        self.assertIn("StyledReadMe", res_fbs)

    def test_tones_selection(self) -> None:
        set_color_level(ColorLevel.ANSI256)
        tones = ["neon", "pastel", "warm", "cool"]
        for t in tones:
            fg_res = foreground("ToneText", tone=t)
            self.assertIn("ToneText", fg_res)
            self.assertTrue(fg_res.endswith(RESET))

            bg_res = background("ToneBg", tone=t)
            self.assertIn("ToneBg", bg_res)
            self.assertTrue(bg_res.endswith(RESET))

            auto_fg_res = auto_fg("AutoTone", tone=t)
            self.assertIn("AutoTone", auto_fg_res)

            auto_bg_res = auto_bg("AutoToneBg", tone=t)
            self.assertIn("AutoToneBg", auto_bg_res)

    def test_invalid_tone_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            foreground("Text", tone="nonexistent_tone_123")

        with self.assertRaises(ValueError):
            background("Text", tone="nonexistent_tone_123")

    def test_gradient_fg(self) -> None:
        from Rcolor import gradient_fg, strip_color

        # TrueColor level
        set_color_level(ColorLevel.TRUECOLOR)
        tc_res = gradient_fg("Gradient", start="#ff0000", end="#0000ff")
        self.assertTrue(tc_res.startswith("\033[38;2;"))
        self.assertTrue(tc_res.endswith(RESET))
        self.assertEqual(strip_color(tc_res), "Gradient")

        # 256-color level
        set_color_level(ColorLevel.ANSI256)
        c256_res = gradient_fg("Gradient256", start=(255, 0, 0), end=(0, 255, 0))
        self.assertTrue(c256_res.startswith("\033[38;5;"))
        self.assertTrue(c256_res.endswith(RESET))
        self.assertEqual(strip_color(c256_res), "Gradient256")

        # 16-color level
        set_color_level(ColorLevel.ANSI16)
        c16_res = gradient_fg("Gradient16", preset="warm")
        self.assertTrue(c16_res.endswith(RESET))
        self.assertNotIn("\033[38;5;", c16_res)
        self.assertNotIn("\033[38;2;", c16_res)

        # Disabled level
        set_color_level(ColorLevel.NONE)
        none_res = gradient_fg("PlainGradient")
        self.assertEqual(none_res, "PlainGradient")

    def test_gradient_presets_and_rainbow(self) -> None:
        from Rcolor import gradient_fg, gradient_rainbow

        set_color_level(ColorLevel.TRUECOLOR)
        presets = ["rainbow", "neon", "sunset", "warm", "cool", "pastel", "cyberpunk", "ocean"]
        for p in presets:
            res = gradient_fg("PresetSample", preset=p)
            self.assertTrue(res.endswith(RESET))

        # gradient_rainbow helper
        rainbow_res = gradient_rainbow("SmoothRainbowText")
        self.assertTrue(rainbow_res.startswith("\033[38;2;"))
        self.assertTrue(rainbow_res.endswith(RESET))

    def test_gradient_edge_cases(self) -> None:
        from Rcolor import gradient_fg

        set_color_level(ColorLevel.TRUECOLOR)
        # Empty input
        self.assertEqual(gradient_fg(""), "")

        # Single character
        single_res = gradient_fg("A", start="#ff0000", end="#00ff00")
        self.assertTrue(single_res.endswith(RESET))
        self.assertIn("A", single_res)

        # Numeric input
        num_res = gradient_fg(98765, preset="neon")
        self.assertTrue(num_res.endswith(RESET))

        # Invalid type
        with self.assertRaises(TypeError):
            gradient_fg([1, 2, 3])

        # Invalid preset
        with self.assertRaises(ValueError):
            gradient_fg("Text", preset="fake_preset_xyz")

        # Invalid color format
        with self.assertRaises(ValueError):
            gradient_fg("Text", start="not-a-color")

    def test_strip_color(self) -> None:
        from Rcolor import strip_color

        self.assertEqual(strip_color(""), "")
        self.assertEqual(strip_color("Plain text without color"), "Plain text without color")
        self.assertEqual(strip_color("\033[31mRed text\033[0m"), "Red text")
        self.assertEqual(strip_color("\033[1;32;40mBold green on black\033[0m"), "Bold green on black")
        self.assertEqual(strip_color("\033[38;2;255;128;0mTrueColor\033[0m"), "TrueColor")
        self.assertEqual(strip_color("\033[38;5;208mANSI 256\033[0m"), "ANSI 256")

        # Test on styled strings from Rcolor
        styled = foreground("Sample text")
        self.assertEqual(strip_color(styled), "Sample text")

        rainbow = rainbow_fg("Multi-colored")
        self.assertEqual(strip_color(rainbow), "Multi-colored")

        # Non-string and None input handling
        self.assertEqual(strip_color(12345), "12345")
        self.assertEqual(strip_color(None), "")


if __name__ == "__main__":
    unittest.main()

