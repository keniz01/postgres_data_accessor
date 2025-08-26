import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
src_path = project_root / "src"

if not src_path.exists():
    sys.path.insert(0, str(src_path))
