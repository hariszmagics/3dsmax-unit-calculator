# H MEDIA 3D ACADEMY — Unit Converter 3.2

A free, open-source unit conversion utility for Autodesk 3ds Max.

Developed by **H MEDIA 3D ACADEMY**.

## Overview

Unit Converter 3.2 is a utility designed to support unit conversion workflows in Autodesk 3ds Max.

The project includes MaxScript and Python components, installation scripts, and supporting resources.

## Package Contents

```text
3dsmax-unit-calculator/
├── hmedia_units/
├── Install.ms
├── install.py
├── launch.py
├── manifest.json
├── mzp.run
├── Open Converter.ms
├── UnitConverter.mcr
├── README.md
├── VALIDATION.md
└── LICENSE
```

## Installation

### Requirements

- Autodesk 3ds Max
- Compatible Windows environment
- The complete plugin package, including the `hmedia_units` folder

**Note:** Supported 3ds Max versions and Python requirements should be confirmed through testing.

### Step 1 — Download

1. Open the [GitHub repository](https://github.com/hariszmagics/3dsmax-unit-calculator).
2. Click **Code → Download ZIP**.
3. Extract the ZIP file to a local folder.
4. Keep the original directory structure intact.

### Step 2 — Install

The package includes `Install.ms` and `install.py`.

The exact installation procedure must be verified against these scripts before running them. Do not move or rename the supporting files until their dependencies have been checked.

### Step 3 — Launch

The package includes `Open Converter.ms`, `UnitConverter.mcr`, and `launch.py`.

The correct launch procedure and any toolbar or menu registration steps must be confirmed from the implementation.

## Validation

See `VALIDATION.md` for any documented validation information.

Static code validation and successful execution inside Autodesk 3ds Max are separate checks. Compatibility should not be assumed without testing.

## Project Structure

| File | Purpose |
|---|---|
| `hmedia_units/` | Supporting plugin resources |
| `Install.ms` | MaxScript installation entry point |
| `install.py` | Python installation component |
| `launch.py` | Python launch component |
| `manifest.json` | Package metadata |
| `mzp.run` | Package execution instructions |
| `Open Converter.ms` | MaxScript launcher |
| `UnitConverter.mcr` | 3ds Max MacroScript |
| `README.md` | Project documentation |
| `VALIDATION.md` | Validation documentation |

## License

This project is distributed under the MIT License. See the `LICENSE` file for the full terms.

## Author

**H MEDIA 3D ACADEMY**

GitHub: https://github.com/hariszmagics

## Contributions

Bug reports, installation feedback, documentation improvements, and code contributions are welcome through GitHub Issues and Pull Requests.
