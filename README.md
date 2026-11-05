# H MEDIA 3D ACADEMY — Unit Converter 3.2

## Install

1. Run **HMedia-UnitConverter-3.2.mzp** using **Scripting → Run Script**, or drag it into a Max viewport.
2. The installer copies the tool and icons to your current Max user's folders and opens the converter.
3. Under **Customize User Interface → Toolbars**, choose **H MEDIA 3D ACADEMY** and drag **Unit Converter** onto a toolbar.
4. If an old button still opens version 2, remove that button and add the installed action again. Restart Max if the icon remains cached.

ZIP alternative: extract the entire folder and run **Install.ms**. To try it without installing, run **Open Converter.ms**, keeping it beside launch.py and the hmedia_units folder.

Do not run the old UnitConverter.ms from earlier downloads. Version 3 uses the small launcher files included in this package.

## Use

- **Units only** is selected by default: **1 m → 1000 mm**. Choose **Diameter → Radius** for **200 mm → 100 mm**.
- Select one parametric object. The left panel shows its current parameter value; radius is offered first when available.
- Choose a parameter, enter your measurement on the right, then click **Update Selected Parameter**.
- **Use current measurement** loads the equivalent input for the chosen conversion. A 50 mm radius loads a 100 mm diameter, so clicking Update immediately leaves the radius unchanged.
- **Radius → Diameter** and **Units only** are also available.
- Supported units: **mm, cm, m, inches and feet**. Enter decimal values or calculations, e.g. 25.4, 2400 / 3, or (200 + 50) * 2. Do not include unit suffixes in the field.
- With no object selected, the converter and **Copy result** still work.
- The current value follows external edits and Undo. Live updates do not overwrite typed measurements.

The output-unit selector changes how results and current values are displayed. Applied values retain the correct physical size in the scene's system units. The tool does not change scene unit settings.

## Supported parameters

The tool lists common scalar length properties of the base object and modifiers: radius, length, width, height, thickness and related names. It does not claim to discover every parameter in every third-party plugin. Confirm that a third-party property represents a length before applying a measurement.

Editable Poly/Mesh objects often have no primitive dimensions. The tool edits stored parameters, not world-space bounding-box dimensions after object scaling. Instanced objects/modifiers share changes. Animation follows the current frame and Max's Auto Key behavior.

An Update is recorded in Max's Undo stack. A changed selection is rechecked immediately before writing. Read-only properties and invalid input report errors rather than writing arbitrary values.

## Files and icon

- `hmedia_units/core.py`: conversion and numeric validation.
- `hmedia_units/host.py`: 3ds Max API integration.
- `hmedia_units/ui.py`: Qt interface.
- `Install.ms`, `install.py`: per-user installer.
- `UnitConverter.mcr`: minimal toolbar launcher.
- `hmedia_units/icons/tape_64.png`: requested **64×64 transparent yellow tape-measure icon**.
- PNGs at 16, 20, 24, 30, 32, 36, 40, 48, 96 and 128 pixels support toolbar scaling. Editable SVG source is included.

## Requirements and validation

Uses Python 3, pymxs and PySide6/PySide2 supplied by 3ds Max. Built for the installed Max 2025 environment, with a Qt 5 fallback for earlier Python 3 releases. No pip packages or external Python installation are needed by the plugin.

See VALIDATION.md for exactly what passed and which in-Max tests remain outstanding. Passing standalone tests is not equivalent to verifying all Max versions or third-party object plugins.

## Uninstall

Remove the toolbar button. With Max closed, remove only `HMediaUnitConverter` from your Max userScripts folder, `HMedia3D-UnitConverter.mcr` from userMacros, and `HMedia3D` under userIcons/Dark and userIcons/Light. The installer does not delete older third-party or version-2 files automatically.

## Autodesk API references

- [Python in 3ds Max](https://help.autodesk.com/cloudhelp/2025/ENU/MAXDEV-Python/files/MAXDEV_Python_about_the_3ds_max_python_api_html.html)
- [Python user interfaces](https://help.autodesk.com/cloudhelp/2025/ENU/MAXDEV-Python/files/MAXDEV_Python_creating_python_uis_html.html)
- [MacroScript and multi-resolution icons](https://help.autodesk.com/cloudhelp/2019/ENU/3DSMax-MAXScript/files/GUID-6E21C768-7256-4500-AB1F-B144F492F055.htm)
- [MZP packaging](https://help.autodesk.com/cloudhelp/2022/ENU/MAXScript-Help/files/MAXScript-Tools-and-Interaction/File-Access/Zip-file-Packaging-and-Drag-And/GUID-A085EFDD-A397-41D6-9391-421344294422.html)

## Reverse any conversion
Click **Swap / Reverse** to put the unrounded result in the input, swap From and To, and reverse Diameter → Radius / Radius → Diameter. Units-only conversions stay in Units only. Examples: 2.5 m → 2500 mm → 2.5 m; 50 mm radius → 100 mm diameter → 50 mm radius.


## Arithmetic calculator and short decimals
Values display up to 3 decimal places, with trailing zeros removed: 20.22439957 becomes 20.224; 2500 stays 2500. Hover the current value or result for full precision. Display rounding does not alter an untouched loaded parameter or the internal result used by Update.

To divide a parameter:
1. Select the object and parameter.
2. Click **Use current value**. This selects Units only and uses the current display unit for input.
3. Click **÷**, type **3**, then **=** (or Enter).
4. Click **Update Selected Parameter**. A 2400 mm value becomes 800 mm.

The +, −, × and ÷ buttons, keyboard expressions and parentheses are supported. C clears the input. Enter calculates; it does not apply to the object. Dividing by zero disables Update.

When using an operator button on a loaded value, the input uses the word **value**, e.g. `value / 3`. This refers to the exact measurement captured when you loaded it, preserving precision. The small hint shows its formatted value. External object changes do not change this captured value until you load it again. If you manually edit the displayed number, your entered number is used instead.

Arithmetic runs first, then the selected unit and radius/diameter conversion. Example: 2.4 / 3 in metres gives 800 mm in Units only, or a 400 mm radius in Diameter → Radius mode.

This divides a parameter's measurement; it does not cut a mesh into separate objects.
