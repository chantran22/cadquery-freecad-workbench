import sys
from pathlib import Path
import importlib

# Path to your module
module_path = Path("path/to/your/module")

# Add the module directory to sys.path if not already added
if str(module_path.parent) not in sys.path:
    sys.path.append(str(module_path.parent))

# Reload the module
module_name = module_path.stem
if module_name in sys.modules:
    importlib.reload(sys.modules[module_name])
else:
    __import__(module_name)
