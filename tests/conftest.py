import sys
from pathlib import Path

# Add project root to path for pytest
project_root = str(Path(__file__).parent.parent.absolute())
if project_root not in sys.path:
    sys.path.insert(0, project_root) 