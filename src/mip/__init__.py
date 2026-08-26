"""
Marketing Intelligence Platfrom - core package.
"""

from pathlib import Path

__version__ = "0.1.0"



CURRENT_FILE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_FILE_DIR.parents[1]
CSV_PATH = PROJECT_ROOT / "data"/"raw"/"influencer_marketing.csv"

