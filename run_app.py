from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
app = ROOT / "app" / "ui" / "myapp.py"

subprocess.run(
    [sys.executable, "-m", "streamlit", "run", str(app)],
    cwd=ROOT,
    check=False,
)
