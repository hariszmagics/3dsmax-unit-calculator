"""Run from 3ds Max's Python ExecuteFile launcher."""
from pathlib import Path
import sys
import traceback

root = str(Path(__file__).resolve().parent)
if root not in sys.path:
    sys.path.insert(0, root)

try:
    from hmedia_units.ui import show
    show()
except Exception:
    details = traceback.format_exc()
    print(details)
    try:
        from PySide6 import QtWidgets
    except ImportError:
        from PySide2 import QtWidgets
    QtWidgets.QMessageBox.critical(None, "H MEDIA Unit Converter", details)
