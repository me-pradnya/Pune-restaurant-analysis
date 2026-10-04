"""Orchestrate cleaning and EDA from the repository root."""
import subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
for script in ("data_cleaning.py", "exploratory_analysis.py"):
    subprocess.run([sys.executable, str(ROOT / "src" / script)], check=True)
