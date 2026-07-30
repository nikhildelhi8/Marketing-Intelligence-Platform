"""
Marketing Intelligence Platfrom - core package.
"""

from pathlib import Path

__version__ = "0.1.0"

PROJECT_ROOT: Path = Path(__file__).resolve().parents[2]

print(PROJECT_ROOT)