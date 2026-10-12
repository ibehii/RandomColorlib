"""Tests for Rcolor.terminal module."""
import os
import unittest
from unittest.mock import MagicMock, patch

from Rcolor.terminal import (
    ColorLevel,
    detect_color_level,
    get_color_level,
    invalidate_color_level_cache,
    set_color_level,
)


class TestTerminal(unittest.TestCase):
    """Test terminal detection, environment parsing, and downgrade rules."""

    def setUp(self) -> None:
        self.original_env = os.environ.copy()
        set_color_level(None)
        invalidate_color_level_cache()
        self._clean_env()

    def tearDown(self) -> None:
        os.environ.clear()
        os.environ.update(self.original_env)
        set_color_level(None)
        invalidate_color_level_cache()

    def _clean_env(self) -> None:
        """Strip ambient terminal and color variables for deterministic unit testing."""
        keys_to_clean = [
            "NO_COLOR",
            "FORCE_COLOR",
            "CLICOLOR",
            "CLICOLOR_FORCE",
            "COLORTERM",
            "TERM",
            "TERM_PROGRAM",
            "WT_SESSION",
            "ConEmuPID",
            "PYCHARM_HOSTED",
            "TERMINAL_EMULATOR",
            "VTE_VERSION",
            "KONSOLE_VERSION",
            "KONSOLE_DBUS_SERVICE",
            "KITTY_WINDOW_ID",
            "ALACRITTY_WINDOW_ID",
            "ALACRITTY_SOCKET",
            "ALACRITTY_LOG",
            "WEZTERM_PANE",
            "GHOSTTY_RESOURCES_DIR",
            "FOOT_TERMINAL_TITLE",
            "ANSICON",
            "SSH_CONNECTION",
            "SSH_CLIENT",
            "SSH_TTY",
        ]
        for k in keys_to_clean:
            os.environ.pop(k, None)

    def test_no_color_env(self) -> None:
        os.environ["NO_COLOR"] = "1"
        os.environ["COLORTERM"] = "truecolor"
        self.assertEqual(detect_color_level(), ColorLevel.NONE)

    def test_force_color_levels(self) -> None:
        os.environ["FORCE_COLOR"] = "0"
        self.assertEqual(detect_color_level(), ColorLevel.NONE)

        os.environ["FORCE_COLOR"] = "1"
        self.assertEqual(detect_color_level(), ColorLevel.ANSI16)

        os.environ["FORCE_COLOR"] = "2"
        self.assertEqual(detect_color_level(), ColorLevel.ANSI256)

        os.environ["FORCE_COLOR"] = "3"
        self.assertEqual(detect_color_level(), ColorLevel.TRUECOLOR)

        os.environ["FORCE_COLOR"] = "truecolor"
        self.assertEqual(detect_color_level(), ColorLevel.TRUECOLOR)

    def test_clicolor_flags(self) -> None:
        mock_stdout = MagicMock()
        mock_stdout.isatty.return_value = True

        with patch("sys.stdout", mock_stdout):
            # CLICOLOR=0 disables colors on a TTY
            os.environ["CLICOLOR"] = "0"
            os.environ["CLICOLOR_FORCE"] = "0"
            self.assertEqual(detect_color_level(), ColorLevel.NONE)

            # CLICOLOR_FORCE=1 re-enables colors even when CLICOLOR=0
            os.environ["CLICOLOR_FORCE"] = "1"
            os.environ["TERM"] = "xterm-256color"
            self.assertEqual(detect_color_level(), ColorLevel.ANSI256)

    def test_non_tty_redirection(self) -> None:
        mock_stdout = MagicMock()
        mock_stdout.isatty.return_value = False

        with patch("sys.stdout", mock_stdout):
            os.environ["TERM"] = "xterm-256color"
            self.assertEqual(detect_color_level(), ColorLevel.NONE)

    def test_term_dumb(self) -> None:
        mock_stdout = MagicMock()
        mock_stdout.isatty.return_value = True

        with patch("sys.stdout", mock_stdout):
            os.environ["TERM"] = "dumb"
            self.assertEqual(detect_color_level(), ColorLevel.NONE)

    def test_colorterm_truecolor(self) -> None:
        mock_stdout = MagicMock()
        mock_stdout.isatty.return_value = True

        with patch("sys.stdout", mock_stdout):
            os.environ["COLORTERM"] = "truecolor"
            self.assertEqual(detect_color_level(), ColorLevel.TRUECOLOR)

            os.environ["COLORTERM"] = "24bit"
            self.assertEqual(detect_color_level(), ColorLevel.TRUECOLOR)

    def test_term_programs(self) -> None:
        mock_stdout = MagicMock()
        mock_stdout.isatty.return_value = True

        with patch("sys.stdout", mock_stdout):
            os.environ["TERM_PROGRAM"] = "vscode"
            self.assertEqual(detect_color_level(), ColorLevel.TRUECOLOR)

            os.environ["TERM_PROGRAM"] = "iterm.app"
            self.assertEqual(detect_color_level(), ColorLevel.TRUECOLOR)

            os.environ["TERM_PROGRAM"] = "apple_terminal"
            self.assertEqual(detect_color_level(), ColorLevel.ANSI256)

    def test_term_names(self) -> None:
        mock_stdout = MagicMock()
        mock_stdout.isatty.return_value = True

        with patch("sys.stdout", mock_stdout):
            os.environ["TERM"] = "xterm-256color"
            self.assertEqual(detect_color_level(), ColorLevel.ANSI256)

            os.environ["TERM"] = "tmux-256color"
            self.assertEqual(detect_color_level(), ColorLevel.ANSI256)

            os.environ["TERM"] = "xterm"
            self.assertEqual(detect_color_level(), ColorLevel.ANSI16)

            os.environ["TERM"] = "linux"
            self.assertEqual(detect_color_level(), ColorLevel.ANSI16)

    def test_windows_terminal_mock(self) -> None:
        mock_stdout = MagicMock()
        mock_stdout.isatty.return_value = True

        with patch("sys.stdout", mock_stdout):
            with patch("sys.platform", "win32"):
                os.environ["WT_SESSION"] = "some-guid"
                self.assertEqual(detect_color_level(), ColorLevel.TRUECOLOR)

    def test_manual_set_color_level(self) -> None:
        set_color_level(ColorLevel.ANSI256)
        self.assertEqual(get_color_level(), ColorLevel.ANSI256)

        set_color_level(ColorLevel.NONE)
        self.assertEqual(get_color_level(), ColorLevel.NONE)

        set_color_level(None)
        # Should fall back to detect_color_level
        self.assertIn(
            get_color_level(),
            (ColorLevel.NONE, ColorLevel.ANSI16, ColorLevel.ANSI256, ColorLevel.TRUECOLOR),
        )

    def test_clicolor_force_on_non_tty(self) -> None:
        mock_stdout = MagicMock()
        mock_stdout.isatty.return_value = False

        with patch("sys.stdout", mock_stdout):
            os.environ["CLICOLOR_FORCE"] = "1"
            # Even with no TERM or dumb TERM, CLICOLOR_FORCE=1 forces at least ANSI16
            os.environ.pop("TERM", None)
            os.environ.pop("COLORTERM", None)
            self.assertGreaterEqual(detect_color_level(), ColorLevel.ANSI16)

    def test_empty_env_vars_do_not_force_or_disable(self) -> None:
        mock_stdout = MagicMock()
        mock_stdout.isatty.return_value = True

        with patch("sys.stdout", mock_stdout):
            # NO_COLOR="" should not disable colors (per https://no-color.org)
            os.environ["NO_COLOR"] = ""
            os.environ["TERM"] = "xterm-256color"
            self.assertEqual(detect_color_level(), ColorLevel.ANSI256)

            # FORCE_COLOR="" should not force 256 colors
            os.environ["FORCE_COLOR"] = ""
            os.environ["TERM"] = "xterm"
            self.assertEqual(detect_color_level(), ColorLevel.ANSI16)

            # CLICOLOR_FORCE="" should not force colors
            os.environ["CLICOLOR_FORCE"] = ""
            mock_stdout.isatty.return_value = False
            self.assertEqual(detect_color_level(), ColorLevel.NONE)

    def test_idle_environment(self) -> None:
        mock_stdout = MagicMock()
        mock_stdout.isatty.return_value = True

        with patch("sys.stdout", mock_stdout):
            with patch.dict("sys.modules", {"idlelib": MagicMock()}):
                os.environ["TERM"] = "xterm-256color"
                self.assertEqual(detect_color_level(), ColorLevel.NONE)

    def test_jupyter_environment(self) -> None:
        mock_stdout = MagicMock()
        mock_stdout.isatty.return_value = True

        with patch("sys.stdout", mock_stdout):
            with patch.dict("sys.modules", {"ipykernel": MagicMock()}):
                os.environ.pop("TERM", None)
                os.environ.pop("COLORTERM", None)
                self.assertEqual(detect_color_level(), ColorLevel.ANSI256)

    def test_ssh_session_environment(self) -> None:
        mock_stdout = MagicMock()
        mock_stdout.isatty.return_value = True

        with patch("sys.stdout", mock_stdout):
            os.environ["SSH_CONNECTION"] = "192.168.1.1 50000 192.168.1.2 22"
            os.environ["TERM"] = "xterm-256color"
            self.assertEqual(detect_color_level(), ColorLevel.ANSI256)

            # SSH with generic terminal defaults to ANSI16
            os.environ["TERM"] = "xterm"
            self.assertEqual(detect_color_level(), ColorLevel.ANSI16)

    def test_stdout_is_none(self) -> None:
        with patch("sys.stdout", None):
            self.assertEqual(detect_color_level(), ColorLevel.NONE)

    def test_windows_no_vt_or_colorama_falls_back_to_none(self) -> None:
        mock_stdout = MagicMock()
        mock_stdout.isatty.return_value = True

        with patch("sys.stdout", mock_stdout):
            with patch("sys.platform", "win32"):
                with patch("Rcolor.terminal._init_windows_console", return_value=False):
                    with patch("sys.getwindowsversion", side_effect=Exception, create=True):
                        self.assertEqual(detect_color_level(), ColorLevel.NONE)

    def test_windows_vt_builds(self) -> None:
        mock_stdout = MagicMock()
        mock_stdout.isatty.return_value = True

        mock_win10_truecolor = MagicMock(major=10, build=19041)
        mock_win10_256 = MagicMock(major=10, build=10586)
        mock_win_old = MagicMock(major=6, build=7601)

        with patch("sys.stdout", mock_stdout):
            with patch("sys.platform", "win32"):
                with patch("Rcolor.terminal._init_windows_console", return_value=True):
                    with patch(
                        "sys.getwindowsversion", return_value=mock_win10_truecolor, create=True
                    ):
                        self.assertEqual(detect_color_level(), ColorLevel.TRUECOLOR)

                    with patch(
                        "sys.getwindowsversion", return_value=mock_win10_256, create=True
                    ):
                        self.assertEqual(detect_color_level(), ColorLevel.ANSI256)

                    with patch(
                        "sys.getwindowsversion", return_value=mock_win_old, create=True
                    ):
                        self.assertEqual(detect_color_level(), ColorLevel.ANSI16)

    def test_modern_terminals_truecolor(self) -> None:
        mock_stdout = MagicMock()
        mock_stdout.isatty.return_value = True

        with patch("sys.stdout", mock_stdout):
            # VTE version >= 3600 (e.g. GNOME Terminal)
            os.environ["VTE_VERSION"] = "6000"
            self.assertEqual(detect_color_level(), ColorLevel.TRUECOLOR)
            os.environ.pop("VTE_VERSION", None)

            # Konsole
            os.environ["KONSOLE_VERSION"] = "210800"
            self.assertEqual(detect_color_level(), ColorLevel.TRUECOLOR)
            os.environ.pop("KONSOLE_VERSION", None)

            # Kitty window
            os.environ["KITTY_WINDOW_ID"] = "1"
            self.assertEqual(detect_color_level(), ColorLevel.TRUECOLOR)
            os.environ.pop("KITTY_WINDOW_ID", None)

            # Alacritty socket
            os.environ["ALACRITTY_SOCKET"] = "/tmp/alacritty.sock"
            self.assertEqual(detect_color_level(), ColorLevel.TRUECOLOR)
            os.environ.pop("ALACRITTY_SOCKET", None)

            # WezTerm pane
            os.environ["WEZTERM_PANE"] = "0"
            self.assertEqual(detect_color_level(), ColorLevel.TRUECOLOR)
            os.environ.pop("WEZTERM_PANE", None)

            # TERM names: kitty, alacritty, foot, ghostty, wezterm
            for term_name in ("xterm-kitty", "alacritty", "foot", "ghostty", "wezterm"):
                os.environ["TERM"] = term_name
                self.assertEqual(detect_color_level(), ColorLevel.TRUECOLOR)

    def test_ansicon_windows(self) -> None:
        mock_stdout = MagicMock()
        mock_stdout.isatty.return_value = True

        with patch("sys.stdout", mock_stdout):
            with patch("sys.platform", "win32"):
                os.environ["ANSICON"] = "1"
                self.assertEqual(detect_color_level(), ColorLevel.ANSI256)


if __name__ == "__main__":
    unittest.main()
