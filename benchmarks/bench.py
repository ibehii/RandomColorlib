#!/usr/bin/env python3
"""Benchmark suite for Rcolor comparing performance before and after optimization.

Measures:
1. Module import time (fresh imports).
2. foreground() function call latency.
3. rainbow_fg() throughput on a 1,000 character string.
"""
from pathlib import Path
import sys
import timeit
from typing import Dict, Tuple

# Ensure repository root is on sys.path
REPO_ROOT = str(Path(__file__).resolve().parent.parent)
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

# Baseline measurements from Rcolor 3.0.1 (before optimization):
# - JSON parsed from disk on every function call
# - Repeated string concatenation in rainbow_fg
# - Inefficient import-time checks
BEFORE_METRICS: Dict[str, Tuple[float, str]] = {
    "import_time": (0.673, "ms"),
    "foreground_call": (250.91, "µs"),
    "rainbow_1000char": (147.40, "ms"),
}


def measure_import_time(iterations: int = 200) -> float:
    """Measure fresh import time in milliseconds."""
    stmt = (
        "for k in list(sys.modules):\n"
        "    if k == 'Rcolor' or k.startswith('Rcolor.'):\n"
        "        sys.modules.pop(k, None)\n"
        "import Rcolor"
    )
    setup = f"import sys\nif '{REPO_ROOT}' not in sys.path:\n    sys.path.insert(0, '{REPO_ROOT}')"
    timer = timeit.Timer(stmt=stmt, setup=setup)
    total_time = timer.timeit(number=iterations)
    return (total_time / iterations) * 1000.0


def measure_foreground(iterations: int = 10000) -> float:
    """Measure single foreground() call time in microseconds."""
    setup = (
        f"import sys\nif '{REPO_ROOT}' not in sys.path:\n    sys.path.insert(0, '{REPO_ROOT}')\n"
        "import Rcolor; Rcolor.set_color_level(Rcolor.ColorLevel.ANSI256)"
    )
    stmt = "Rcolor.foreground('Hello, World!')"
    timer = timeit.Timer(stmt=stmt, setup=setup)
    total_time = timer.timeit(number=iterations)
    return (total_time / iterations) * 1_000_000.0


def measure_rainbow(iterations: int = 200) -> float:
    """Measure rainbow_fg() on 1,000 characters in milliseconds."""
    setup = (
        f"import sys\nif '{REPO_ROOT}' not in sys.path:\n    sys.path.insert(0, '{REPO_ROOT}')\n"
        "import Rcolor\n"
        "Rcolor.set_color_level(Rcolor.ColorLevel.ANSI256)\n"
        "sample = 'A' * 1000"
    )
    stmt = "Rcolor.rainbow_fg(sample)"
    timer = timeit.Timer(stmt=stmt, setup=setup)
    total_time = timer.timeit(number=iterations)
    return (total_time / iterations) * 1000.0


def run_benchmark() -> None:
    """Run all benchmarks and print comparison table."""
    print("=" * 72)
    print("  Rcolor Performance Benchmark (Before vs After Optimization)")
    print("=" * 72)
    print("Running benchmarks...")

    # Warm up
    import Rcolor

    Rcolor.set_color_level(Rcolor.ColorLevel.ANSI256)
    _ = Rcolor.foreground("warmup")
    _ = Rcolor.rainbow_fg("warmup" * 10)

    import_ms = measure_import_time()
    fg_us = measure_foreground()
    rainbow_ms = measure_rainbow()

    results = {
        "import_time": (import_ms, "ms"),
        "foreground_call": (fg_us, "µs"),
        "rainbow_1000char": (rainbow_ms, "ms"),
    }

    print()
    header = f"{'Metric':<30} | {'Before (v3.0.1)':<16} | {'After (v3.1.0)':<16} | {'Speedup':<12}"
    print(header)
    print("-" * len(header))

    metrics_labels = {
        "import_time": "Import Time (fresh)",
        "foreground_call": "foreground() call latency",
        "rainbow_1000char": "rainbow_fg() (1,000 chars)",
    }

    for key, label in metrics_labels.items():
        before_val, unit = BEFORE_METRICS[key]
        after_val, _ = results[key]
        speedup = before_val / after_val if after_val > 0 else float("inf")
        speedup_str = f"{speedup:,.1f}x faster" if speedup >= 1.0 else f"{1.0/speedup:.1f}x slower"

        before_str = f"{before_val:.3f} {unit}"
        after_str = f"{after_val:.3f} {unit}"

        print(f"{label:<30} | {before_str:<16} | {after_str:<16} | {speedup_str:<12}")

    print("=" * 72)


if __name__ == "__main__":
    run_benchmark()
