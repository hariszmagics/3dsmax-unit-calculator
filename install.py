"""Per-user installation. No administrator privileges or external dependencies."""
from pathlib import Path
import shutil
import sys
import traceback


def install(source, rt):
    source = Path(source).resolve()
    destination = Path(str(rt.getDir(rt.Name("userScripts")))) / "HMediaUnitConverter"
    macros = Path(str(rt.getDir(rt.Name("userMacros"))))
    icons = Path(str(rt.getDir(rt.Name("userIcons"))))
    files = [source / "launch.py"] + list((source / "hmedia_units").rglob("*.py")) + list((source / "hmedia_units" / "icons").glob("*.png"))
    # Verify the complete payload before modifying an existing installation.
    for required in ("launch.py", "UnitConverter.mcr", "hmedia_units/ui.py", "hmedia_units/core.py", "hmedia_units/host.py", "hmedia_units/icons/tape_64.png"):
        if not (source / required).is_file():
            raise RuntimeError("Installation is incomplete: " + required)
    for path in files:
        target = destination / path.relative_to(source)
        target.parent.mkdir(parents=True, exist_ok=True)
        if path.resolve() != target.resolve():
            shutil.copy2(path, target)
    for theme in ("Dark", "Light"):
        target = icons / theme / "HMedia3D"
        target.mkdir(parents=True, exist_ok=True)
        for path in (source / "hmedia_units" / "icons").glob("tape_*.png"):
            shutil.copy2(path, target / path.name)
    macros.mkdir(parents=True, exist_ok=True)
    macro_path = macros / "HMedia3D-UnitConverter.mcr"
    shutil.copy2(source / "UnitConverter.mcr", macro_path)
    rt.fileIn(str(macro_path))
    return destination


def main():
    from pymxs import runtime as rt
    try:
        destination = install(Path(__file__).parent, rt)
        # Close/reload only this plugin's modules when updating in the same session.
        old_ui = sys.modules.get("hmedia_units.ui")
        if old_ui is not None and getattr(old_ui, "_dialog", None) is not None:
            try:
                old_ui._dialog.close()
            except RuntimeError:
                pass
        for name in list(sys.modules):
            if name == "hmedia_units" or name.startswith("hmedia_units."):
                del sys.modules[name]
        sys.path.insert(0, str(destination))
        from hmedia_units.ui import show
        dialog = show()
        dialog.status.setText("Installed. Toolbar category: H MEDIA 3D ACADEMY. Restart Max if the icon is cached.")
    except Exception:
        details = traceback.format_exc()
        print(details)
        rt.messageBox(details, title="H MEDIA Unit Converter - Installation error")


if __name__ == "__main__":
    main()
