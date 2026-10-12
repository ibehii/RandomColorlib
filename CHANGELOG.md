# Changelog

All notable changes to the `Rcolor` project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [3.1.0] - 2026-10-11

### 🚀 Highlights
- **Up to 327x Faster**: Function calls now run in ~1.8 µs (down from ~250 µs) and per-character rainbow formatting runs in ~0.45 ms (down from ~147 ms).
- **Universal Terminal Intelligence**: Intelligent detection of terminal color support (`TRUECOLOR` > `ANSI256` > `ANSI16` > `NONE`) with automatic nearest-color downsampling and zero config.
- **Lazy Zero-Cost Data Loading**: All color lists moved out of Python source code into a standardized `Rcolor/data/colors.json` data file loaded lazily on first call and cached in immutable tuples.
- **100% Backward Compatible**: Every legacy API function signature and return type is preserved.

### 🐍 Python Version Policy Update
- **Minimum Python version raised to `>=3.8`**:
  - Python 3.6 reached official End-of-Life on December 23, 2021.
  - Python 3.7 reached official End-of-Life on June 27, 2023.
  - GitHub Actions and modern packaging toolchains have deprecated Python 3.6 and 3.7 runners.
  - Raising to 3.8+ enables PEP 561 typed packages (`py.typed`), standard packaging via `pyproject.toml`, and modern standard library optimizations without fragile runtime hacks.

### 🐛 Bug Fixes
- **Off-by-One 256-Color Indexing**: Fixed 256-color palette starting at index 1 instead of 0, restoring ANSI color 0 (black).
- **Missing Bright White**: Fixed `standard_colors.json` omitting ANSI escape code `\033[97m` (bright white), completing all 16 standard ANSI colors.
- **Missing Standard Background Colors**: Added standard background colors `40m` through `47m` which were omitted from legacy data files.
- **Removed Invisible Style Code**: Removed `hidden: 8` (`\033[8m`) from the random style palette to prevent user text from randomly being rendered completely invisible.
- **CLICOLOR_FORCE on Non-TTY Streams**: Fixed bug where `CLICOLOR_FORCE=1` returned `ColorLevel.NONE` when `sys.stdout.isatty() == False`.
- **Empty Environment Variable Handling**: Fixed empty string values (`FORCE_COLOR=""`, `CLICOLOR_FORCE=""`) improperly forcing color mode.
- **IDLE Environment Support**: Added explicit detection for Python IDLE GUI shell to prevent raw escape codes in Tkinter output.
- **SSH Environment Intelligence**: Added detection for SSH sessions (`SSH_CONNECTION`, `SSH_CLIENT`, `SSH_TTY`) preserving ANSI color capabilities across remote connections.
- **Import-Time I/O and Windows Fixes**: Removed `colorama.just_fix_windows_console()` from per-call invocations into lazy one-time Windows console initialization with native `ctypes` VT fallback.
- **UnboundLocalError on Error Handling**: Replaced buggy `except TypeError: return ... f'{type(i)}'` where `i` was unbound on empty or early failures with standard Python exceptions.
- **List Index Lookup Bug**: Replaced `user_input[user_input.index(i)] = str(i)` which broke on duplicate inputs with a clean generator expression.
- **Redundant Escape Stacking**: Refactored composite functions (`foreground_background`, `foreground_style`, `background_style`, `foreground_background_style`) to emit cleanly combined ANSI sequences with a single reset code `\033[0m`.
- **String Concatenation in Loops**: Replaced quadratic `Final_text = Final_text + ...` in `rainbow_fg` with optimized `str.join()`.

### 🎁 Added
- **Contrast Guard for Readability**: `foreground_background` and `foreground_background_style` now enforce WCAG relative luminance contrast ratios (default $\ge 4.0:1$), dynamically selecting high-contrast pairs so console text is guaranteed to remain readable.
- **Curated Tone Presets**: Added tone filtering (`tone="neon"`, `"pastel"`, `"warm"`, `"cool"`) across `foreground`, `background`, `auto_fg`, and `auto_bg` for cohesive, high-end styling instead of pure random noise.
- **Smooth Linear Gradients**: Added `gradient_fg` and `gradient_rainbow` for smooth per-character color interpolation with multi-stop presets (`"rainbow"`, `"neon"`, `"sunset"`, `"warm"`, `"cool"`, `"pastel"`, `"cyberpunk"`, `"ocean"`) and automatic TrueColor, 256-color, 16-color, or plain-text fallback.
- **ANSI Strip Utility**: Added `strip_color(text)` for stripping escape codes when calculating table widths and console alignments.
- **Contrast Analysis Utilities**: Exported `contrast_ratio(rgb1, rgb2)` and `relative_luminance(rgb)` for developer inspection.
- **`Rcolor/data/colors.json`**: Unified JSON schema containing all 16 standard colors (with RGB/Hex metadata), all 256 extended colors, text styles, and curated tone presets.
- **`Rcolor.load_palette()` & `Rcolor.reset_palette()`**: Public functions allowing users to load custom palette files or dictionaries and restore defaults.
- **`Rcolor.terminal`**: Dedicated terminal capability detection engine handling:
  - `NO_COLOR` standard (https://no-color.org)
  - `FORCE_COLOR` levels (0, 1, 2, 3)
  - `CLICOLOR` and `CLICOLOR_FORCE`
  - Non-TTY pipes and file redirections (`sys.stdout.isatty()`)
  - IDLE Tkinter shell (`idlelib`)
  - `TERM=dumb`
  - `COLORTERM=truecolor|24bit`
  - Windows Terminal (`WT_SESSION`), ConEmu (`ConEmuPID`), Windows 10/11 Virtual Terminal Processing
  - Remote SSH sessions (`SSH_CONNECTION`, `SSH_CLIENT`, `SSH_TTY`)
  - IDE terminals (VS Code, PyCharm, Jupyter, Apple Terminal, iTerm2, tmux)
- **Automatic Downgrading**: Precomputed RGB Euclidean distance nearest-neighbor mapping from 256 colors to standard 16 colors.
- **`pyproject.toml`**: Modern PEP 517/518 and PEP 621 packaging configuration.
- **`Rcolor/py.typed`**: PEP 561 compliance marker.
- **Comprehensive Test Suite (`tests/`)**: 56 automated unit tests running with both `pytest` and `unittest`.
- **Benchmark Suite (`benchmarks/bench.py`)**: Automated verification benchmark for import time and call latency.
- **Multi-OS CI Matrix**: GitHub Actions testing Linux, Windows, and macOS across Python 3.8 through 3.13.

---

## [3.0.1] - Legacy Baseline
- Initial PyPI release supporting random 255 colors and standard colors.
- Hardcoded file paths and disk reads on every call.
- Basic Windows console detection via `os.name == 'nt'`.
