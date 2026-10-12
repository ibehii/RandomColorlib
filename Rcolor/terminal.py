"""Terminal capability detection and automatic color level downgrading for Rcolor.

Detects terminal support across:
  TRUECOLOR (24-bit) > ANSI256 (8-bit) > ANSI16 (4-bit) > NONE (plain text)

Respects NO_COLOR, FORCE_COLOR, CLICOLOR, CLICOLOR_FORCE, sys.stdout.isatty(),
Windows Terminal, ConEmu, colorama VT, tmux, screen, macOS Terminal, VS Code,
PyCharm, Jupyter, SSH sessions, IDLE, and pipes/redirections.
"""
from __future__ import annotations

import os
import sys
from enum import IntEnum
from typing import Optional


class ColorLevel(IntEnum):
    """Supported terminal color capability levels."""

    NONE = 0
    ANSI16 = 1
    ANSI256 = 2
    TRUECOLOR = 3


_WINDOWS_INITIALIZED = False
_OVERRIDE_COLOR_LEVEL: Optional[ColorLevel] = None
_CACHED_COLOR_LEVEL: Optional[ColorLevel] = None


def _init_windows_console() -> bool:
    """Lazily enable Virtual Terminal Processing on Windows consoles.

    Returns:
        True if VT or colorama was successfully initialized, False otherwise.
    """
    global _WINDOWS_INITIALIZED
    if _WINDOWS_INITIALIZED:
        return True

    # 1. Attempt colorama just_fix_windows_console / init lazily
    try:
        import colorama  # type: ignore

        if hasattr(colorama, "just_fix_windows_console"):
            colorama.just_fix_windows_console()
            _WINDOWS_INITIALIZED = True
            return True
        elif hasattr(colorama, "init"):
            colorama.init()
            _WINDOWS_INITIALIZED = True
            return True
    except Exception:
        pass

    # 2. Attempt native Windows VT processing via ctypes
    if sys.platform == "win32" or os.name == "nt":
        try:
            import ctypes
            from ctypes import wintypes

            kernel32 = ctypes.windll.kernel32  # type: ignore
            # Define 64-bit safe signatures
            kernel32.GetStdHandle.restype = wintypes.HANDLE
            kernel32.GetStdHandle.argtypes = [wintypes.DWORD]
            kernel32.GetConsoleMode.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD)]
            kernel32.SetConsoleMode.argtypes = [wintypes.HANDLE, wintypes.DWORD]

            # STD_OUTPUT_HANDLE = -11 (as unsigned DWORD: 0xFFFFFFF5)
            h_out = kernel32.GetStdHandle(0xFFFFFFF5)
            if h_out and h_out != wintypes.HANDLE(-1).value and h_out != -1:
                mode = wintypes.DWORD()
                if kernel32.GetConsoleMode(h_out, ctypes.byref(mode)):
                    # ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
                    if kernel32.SetConsoleMode(h_out, mode.value | 0x0004):
                        _WINDOWS_INITIALIZED = True
                        return True
        except Exception:
            pass

    return False


def detect_color_level() -> ColorLevel:
    """Inspect environment variables, streams, and OS to detect terminal color level.

    Precedence:
    1. NO_COLOR: if set (non-empty), always disable color (NONE).
    2. FORCE_COLOR: explicit override (0=NONE, 1=ANSI16, 2=ANSI256, 3=TRUECOLOR).
    3. CLICOLOR_FORCE: if != '0', forces at least ANSI16 even when stdout is not a tty.
    4. CLICOLOR: if == '0', disables color (NONE).
    5. stdout.isatty(): if False (and not forced), disable color (NONE).
    6. IDLE: Tkinter shell does not interpret ANSI escapes (NONE).
    7. Windows Terminal (WT_SESSION) / ConEmu (ConEmuPID): TRUECOLOR.
    8. TERM=dumb: disables color (NONE).
    9. COLORTERM=truecolor|24bit: TRUECOLOR.
    10. Jupyter interactive kernel: ANSI256.
    11. macOS / Linux TERM_PROGRAM checks: VS Code, iTerm, Apple Terminal.
    12. IDE terminal emulators: PyCharm, etc.
    13. Windows console checks: Windows 10/11 VT, colorama fallback.
    14. SSH session checks.
    15. TERM string matching: 256color, tmux, xterm, etc.
    16. Fallback: ANSI16 if tty or clicolor_force, else NONE.
    """
    env = os.environ

    # 1. NO_COLOR standard (https://no-color.org)
    no_color = env.get("NO_COLOR")
    if no_color is not None and len(no_color) > 0:
        return ColorLevel.NONE

    # 2. FORCE_COLOR standard
    force_color = env.get("FORCE_COLOR")
    if force_color is not None and len(force_color.strip()) > 0:
        val = force_color.strip().lower()
        if val in ("0", "false", "no", "off"):
            return ColorLevel.NONE
        if val == "1":
            return ColorLevel.ANSI16
        if val == "2":
            return ColorLevel.ANSI256
        if val in ("3", "truecolor", "24bit"):
            return ColorLevel.TRUECOLOR
        # Non-empty truthy value
        return ColorLevel.ANSI256

    # 3. CLICOLOR_FORCE and CLICOLOR
    clicolor_force = env.get("CLICOLOR_FORCE", "0").strip()
    is_clicolor_forced = bool(clicolor_force and clicolor_force != "0")

    clicolor = env.get("CLICOLOR")
    if clicolor is not None and clicolor.strip() == "0" and not is_clicolor_forced:
        return ColorLevel.NONE

    # 4. Stream check: sys.stdout.isatty()
    is_tty = False
    stdout = sys.stdout
    if stdout is not None and hasattr(stdout, "isatty"):
        try:
            is_tty = bool(stdout.isatty())
        except Exception:
            is_tty = False

    if not is_tty and not is_clicolor_forced:
        return ColorLevel.NONE

    # 5. IDLE GUI environment (does not support ANSI escapes in its shell window)
    if "idlelib" in sys.modules and not is_clicolor_forced:
        return ColorLevel.NONE

    # 6. Windows Terminal / ConEmu
    if "WT_SESSION" in env or "ConEmuPID" in env:
        return ColorLevel.TRUECOLOR

    # 7. TERM=dumb
    term = env.get("TERM", "").strip().lower()
    if term == "dumb" and not is_clicolor_forced:
        return ColorLevel.NONE

    # 8. COLORTERM (truecolor / 24bit)
    colorterm = env.get("COLORTERM", "").strip().lower()
    if colorterm in ("truecolor", "24bit"):
        return ColorLevel.TRUECOLOR

    # 9. Jupyter / IPython interactive kernel
    if "ipykernel" in sys.modules:
        return ColorLevel.ANSI256

    # 10. macOS / Linux TERM_PROGRAM checks
    term_program = env.get("TERM_PROGRAM", "").strip().lower()
    if term_program in (
        "vscode",
        "iterm.app",
        "hyper",
        "wezterm",
        "warp",
        "ghostty",
        "rio",
        "alacritty",
        "kitty",
    ):
        return ColorLevel.TRUECOLOR
    if term_program in ("apple_terminal",):
        return ColorLevel.ANSI256

    # 11. Modern terminal environment markers
    if any(
        k in env
        for k in (
            "KITTY_WINDOW_ID",
            "ALACRITTY_WINDOW_ID",
            "ALACRITTY_SOCKET",
            "ALACRITTY_LOG",
            "WEZTERM_PANE",
            "GHOSTTY_RESOURCES_DIR",
            "FOOT_TERMINAL_TITLE",
            "KONSOLE_VERSION",
            "KONSOLE_DBUS_SERVICE",
        )
    ):
        return ColorLevel.TRUECOLOR

    vte_version = env.get("VTE_VERSION")
    if vte_version and vte_version.isdigit() and int(vte_version) >= 3600:
        return ColorLevel.TRUECOLOR

    # 12. IDE terminal emulators
    if "PYCHARM_HOSTED" in env or "TERMINAL_EMULATOR" in env:
        return ColorLevel.ANSI256

    # 13. Windows specific detection
    if sys.platform == "win32" or os.name == "nt":
        if "ANSICON" in env:
            return ColorLevel.ANSI256

        vt_ok = _init_windows_console()

        # Check Windows build version for native VT support
        if hasattr(sys, "getwindowsversion"):
            try:
                win_ver = sys.getwindowsversion()
                # Windows 10 build 14931+ supports 24-bit TrueColor
                if win_ver.major > 10 or (win_ver.major == 10 and win_ver.build >= 14931):
                    return ColorLevel.TRUECOLOR
                # Windows 10 build 10586+ supports 256 colors
                if win_ver.major == 10 and win_ver.build >= 10586:
                    return ColorLevel.ANSI256
            except Exception:
                pass

        # If VT or colorama was enabled on older Windows
        if vt_ok:
            return ColorLevel.ANSI16
        # If neither VT nor colorama could be enabled, disable color to avoid raw escape codes
        return ColorLevel.NONE

    # 14. SSH sessions
    is_ssh = "SSH_CONNECTION" in env or "SSH_CLIENT" in env or "SSH_TTY" in env

    # 15. TERM string matching
    if "direct" in term or "truecolor" in term or "24bit" in term:
        return ColorLevel.TRUECOLOR

    if any(
        sub in term
        for sub in (
            "kitty",
            "alacritty",
            "foot",
            "ghostty",
            "wezterm",
        )
    ):
        return ColorLevel.TRUECOLOR

    if any(
        sub in term
        for sub in (
            "256color",
            "256",
        )
    ):
        return ColorLevel.ANSI256

    if any(
        sub in term
        for sub in (
            "xterm",
            "vt100",
            "vt220",
            "screen",
            "tmux",
            "rxvt",
            "linux",
            "cygwin",
            "ansi",
        )
    ):
        return ColorLevel.ANSI16

    # If SSH session with generic/unspecified terminal, default to ANSI16
    if is_ssh and is_tty:
        return ColorLevel.ANSI16

    # 15. Fallback
    if is_clicolor_forced:
        return ColorLevel.ANSI16
    return ColorLevel.ANSI16 if is_tty else ColorLevel.NONE


def get_color_level() -> ColorLevel:
    """Return the active terminal color capability level.

    Uses override if set via `set_color_level`, otherwise caches result of `detect_color_level`.
    """
    global _CACHED_COLOR_LEVEL
    if _OVERRIDE_COLOR_LEVEL is not None:
        level = _OVERRIDE_COLOR_LEVEL
    else:
        if _CACHED_COLOR_LEVEL is None:
            _CACHED_COLOR_LEVEL = detect_color_level()
        level = _CACHED_COLOR_LEVEL

    # On Windows, ensure console VT is initialized whenever active color level is not NONE
    if level != ColorLevel.NONE and (sys.platform == "win32" or os.name == "nt"):
        _init_windows_console()

    return level


def set_color_level(level: Optional[ColorLevel]) -> None:
    """Manually override or reset terminal color level.

    Args:
        level: Desired ColorLevel enum or None to restore automatic detection.
    """
    global _OVERRIDE_COLOR_LEVEL, _CACHED_COLOR_LEVEL
    _OVERRIDE_COLOR_LEVEL = level
    if level is None:
        _CACHED_COLOR_LEVEL = None


def invalidate_color_level_cache() -> None:
    """Clear cached color level so the next call to get_color_level re-detects."""
    global _CACHED_COLOR_LEVEL
    _CACHED_COLOR_LEVEL = None
