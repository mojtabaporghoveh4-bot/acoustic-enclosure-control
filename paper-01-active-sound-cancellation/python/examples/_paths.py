"""Shared path helpers so the examples run from any working directory."""
from pathlib import Path
import sys

PAPER_DIR = Path(__file__).resolve().parents[2]
DATA = PAPER_DIR / "data"
PYTHON_DIR = PAPER_DIR / "python"

# allow `python examples/foo.py` without installing the package
if str(PYTHON_DIR) not in sys.path:
    sys.path.insert(0, str(PYTHON_DIR))
