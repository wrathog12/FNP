"""
================================================================
  FNP Premium Ad Pipeline - Utility Functions
  Shared helpers for logging, file I/O, and JSON operations.
================================================================
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime

# Fix Windows console encoding for Unicode
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


# -- Styled Console Logging --

def log_header(title: str):
    """Print a styled pipeline header."""
    width = 60
    print()
    print(f"  +{'=' * width}+")
    print(f"  |{'FNP PREMIUM AD AUTOMATION PIPELINE':^{width}}|")
    print(f"  |{'Event Intelligence Layer':^{width}}|")
    print(f"  +{'=' * width}+")
    print(f"  |{title:^{width}}|")
    print(f"  +{'=' * width}+")
    print()


def log_agent_start(agent_name: str, emoji: str = ">>"):
    """Print agent start banner."""
    print(f"\n  {emoji} +--- {agent_name} ---------------------------------")


def log_agent_complete(agent_name: str, emoji: str = "[OK]"):
    """Print agent completion banner."""
    print(f"  {emoji} +--- {agent_name} Complete -------------------------\n")


def log_step(message: str, indent: int = 2):
    """Print an indented step message."""
    prefix = "  " * indent + "| "
    print(f"  {prefix}{message}")


def log_result(key: str, value: str, indent: int = 2):
    """Print a key-value result."""
    prefix = "  " * indent + "| "
    print(f"  {prefix}-> {key}: {value}")


def log_divider():
    """Print a section divider."""
    print(f"  {'-' * 55}")


def log_error(message: str):
    """Print an error message."""
    print(f"\n  [ERROR] {message}\n")


def log_warning(message: str):
    """Print a warning message."""
    print(f"  [WARN] {message}")


def log_success(message: str):
    """Print a success message."""
    print(f"\n  [SUCCESS] {message}\n")


# -- JSON I/O --

def save_json(data: dict, filepath: Path):
    """Save a dictionary as formatted JSON."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False, default=str)


def load_json(filepath: Path) -> dict:
    """Load a JSON file into a dictionary."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


# -- Timing --

class Timer:
    """Simple context manager for timing operations."""

    def __init__(self, label: str = "Operation"):
        self.label = label
        self.start_time = None
        self.elapsed = 0

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, *args):
        self.elapsed = time.time() - self.start_time
        log_step(f"[Timer] {self.label} completed in {self.elapsed:.1f}s")


# -- File Helpers --

def get_timestamp_filename(prefix: str, extension: str = "png") -> str:
    """Generate a timestamped filename."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.{extension}"


def ensure_dir(path: Path) -> Path:
    """Ensure a directory exists and return the path."""
    path.mkdir(parents=True, exist_ok=True)
    return path
