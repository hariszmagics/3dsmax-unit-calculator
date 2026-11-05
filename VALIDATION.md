# Verification — version 3.2.0

## Passed

- All six Python source files compile using the installed **3ds Max 2025 Python 3.11.8** interpreter.
- **7 conversion/host-adapter tests** passed using that interpreter. These exercise known conversions, all unit round-trips, equivalent-input initialization, invalid input, scene-unit scaling, stale selection rejection and preservation of read-only errors through an Undo context.
- **26 Qt/interface/installer tests** passed using a separate **PySide6 6.8.3** test runtime. These construct and operate the real Qt dialog with a simulated scene adapter. They cover standalone conversion, selection/deselection, safe initial values, Update, external changes, invalid input, stale selection, read-only failures, unit changes, timer shutdown, installer copying/reinstallation and icon metadata.
- The interface was rendered and visually inspected. The preview uses a simulated Cylinder001 with a 50 mm radius; it is not a screenshot of a live Max scene.
- The yellow tape icon is a genuine **64×64 RGBA PNG** with transparent corners. Additional PNG sizes were exported from the included SVG.
- Installer payload paths, toolbar category and icon reference were checked in a temporary installation tree.

## Not yet verified

**Live 3ds Max integration is not claimed as tested.** The installed Autodesk Qt runtime hangs when creating a standalone QApplication outside Max; separate Max batch tests did not execute. The passing Qt tests use the isolated standard Qt runtime and simulated Max API behavior. Actual pymxs scene access, Undo in a real scene, MZP execution and toolbar icon discovery still require an in-Max acceptance check.

The delivered plugin does not include or require the isolated test runtime. It uses Max's own pymxs and PySide modules.

## Short acceptance check inside Max

1. Install the MZP or run Install.ms from the extracted folder. Confirm the converter opens without errors.
2. With no selection, enter 200 mm in Diameter → Radius: result 100 mm, Update disabled.
3. Select a Cylinder. Confirm its radius is listed and the left-side current value matches the parameter. The initial result should equal the current value.
4. Enter 200 mm and Update radius. It should become 100 mm. Ctrl+Z in Max should restore the old radius; the current-value display should follow.
5. Change To to cm. The same result should display as 10 cm and apply the same physical size.
6. Change selection immediately before Update. No stale object should be edited.
7. Confirm the action and yellow icon under H MEDIA 3D ACADEMY. Restart Max if its icon cache has not refreshed.

Third-party plugin parameters and earlier/later Max versions have not been certified.

Version 3.1 adds tested default calculator mode, reverse unit conversion, combined unit/diameter reversal, and disabled reversal for invalid input. The host adapter is unchanged from 3.0. Live Max integration remains unverified.


Version 3.2: all 26 tests passed, including standard decimal formatting, arithmetic precedence and parentheses, rejected unsafe expressions, division by zero, calculation plus unit/radius conversion, dividing a loaded parameter and preserving its unrounded value. Source compiles with Max 2025 Python. The supplied screenshot confirms the prior Qt build opened in the user's Max, but does not establish live testing of these new changes.

