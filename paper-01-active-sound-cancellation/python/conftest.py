import sys
from pathlib import Path

# ensure `import acoustic_enclosure` works when running pytest from anywhere
sys.path.insert(0, str(Path(__file__).resolve().parent))
