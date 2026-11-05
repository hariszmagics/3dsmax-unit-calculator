"""Modeless Qt interface. Qt imports support Max's bundled Qt 5 and Qt 6."""
from pathlib import Path
import math
import traceback

try:
    from PySide6 import QtCore, QtGui, QtWidgets
except ImportError:
    from PySide2 import QtCore, QtGui, QtWidgets

from .core import UNITS, MODES, convert, number, equivalent_input, display, evaluate


class ConverterDialog(QtWidgets.QDialog):
    def __init__(self, host, parent=None):
        super().__init__(parent)
        self.host = host
        self.signature = None
        self.items = []
        self.manual_input = False
        self.last_mm = None
        self.result_mm = None
        self.loaded_value = None
        self.loaded_text = None
        self.setWindowTitle("H MEDIA 3D ACADEMY | Unit Calculator 3.2")
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        icon = Path(__file__).parent / "icons" / "tape_64.png"
        self.setWindowIcon(QtGui.QIcon(str(icon)))
        self.setMinimumWidth(660)
        self.setStyleSheet("""
            QDialog { background: #22262c; color: #e9edf3; }
            QLabel, QGroupBox { color: #e9edf3; }
            QGroupBox { border: 1px solid #464b55; border-radius: 8px;
                        margin-top: 12px; padding: 18px 12px 12px; font-weight: 600; }
            QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 5px; }
            QLineEdit, QComboBox { background: #303640; color: #f4f6fa;
                border: 1px solid #555d68; border-radius: 4px; padding: 7px; }
            QComboBox QAbstractItemView { background: #303640; color: #f4f6fa; }
            QPushButton { background: #3b424e; color: #f4f6fa; border: 1px solid #555d68;
                          border-radius: 5px; padding: 9px; }
            QPushButton:hover { background: #4b5462; }
            QPushButton:disabled { background: #30343b; color: #737a84; }
            QPushButton#apply { background: #ffca28; color: #20242a; border: none; font-weight: 700; }
            QPushButton#apply:disabled { background: #4c4735; color: #938969; }
            QLabel#brand { color: #ffca28; font-weight: 700; }
            QLabel#value { font-size: 23px; font-weight: 700; color: #ffda66; }
            QLabel#muted { color: #aab3c0; }
        """)
        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(20, 18, 20, 16)
        root.setSpacing(12)
        header = QtWidgets.QHBoxLayout()
        image = QtWidgets.QLabel()
        image.setPixmap(QtGui.QPixmap(str(icon)).scaled(48, 48, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        header.addWidget(image)
        titles = QtWidgets.QVBoxLayout()
        brand = QtWidgets.QLabel("H MEDIA 3D ACADEMY")
        brand.setObjectName("brand")
        titles.addWidget(brand)
        title = QtWidgets.QLabel("Unit Calculator")
        title.setStyleSheet("font-size: 21px; font-weight: 600;")
        titles.addWidget(title)
        header.addLayout(titles)
        header.addStretch()
        root.addLayout(header)
        columns = QtWidgets.QHBoxLayout()
        left = QtWidgets.QGroupBox("SELECTED OBJECT")
        right = QtWidgets.QGroupBox("CONVERTER")
        columns.addWidget(left, 1)
        columns.addWidget(right, 1)
        root.addLayout(columns)
        object_layout = QtWidgets.QVBoxLayout(left)
        self.object_label = QtWidgets.QLabel("No object selected")
        self.object_label.setWordWrap(True)
        object_layout.addWidget(self.object_label)
        object_layout.addWidget(QtWidgets.QLabel("Parameter"))
        self.parameters = QtWidgets.QComboBox()
        object_layout.addWidget(self.parameters)
        object_layout.addWidget(QtWidgets.QLabel("Current value · live"))
        self.current = QtWidgets.QLabel("—")
        self.current.setObjectName("value")
        self.current.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        object_layout.addWidget(self.current)
        self.scene = QtWidgets.QLabel("")
        self.scene.setObjectName("muted")
        self.scene.setWordWrap(True)
        object_layout.addWidget(self.scene)
        object_layout.addStretch()
        self.read_button = QtWidgets.QPushButton("Use current value →")
        object_layout.addWidget(self.read_button)
        converter_layout = QtWidgets.QVBoxLayout(right)
        self.mode = QtWidgets.QComboBox()
        self.mode.addItems(MODES)
        self.mode.setCurrentIndex(2)
        converter_layout.addWidget(self.mode)
        self.input_label = QtWidgets.QLabel("Diameter")
        converter_layout.addWidget(self.input_label)
        self.input = QtWidgets.QLineEdit("1")
        self.input.setPlaceholderText("e.g. 2400 / 3 or (200 + 50) * 2")
        converter_layout.addWidget(self.input)
        keypad = QtWidgets.QGridLayout()
        self.math_buttons = {}
        for index, caption in enumerate(("+", "−", "×", "÷", "(", ")", "C", "=")):
            button = QtWidgets.QPushButton(caption)
            button.setAutoDefault(False)
            button.clicked.connect(lambda checked=False, key=caption: self.math_key(key))
            keypad.addWidget(button, index // 4, index % 4)
            self.math_buttons[caption] = button
        converter_layout.addLayout(keypad)
        self.value_hint = QtWidgets.QLabel("Supports +, −, ×, ÷ and parentheses")
        self.value_hint.setObjectName("muted")
        self.value_hint.setWordWrap(True)
        converter_layout.addWidget(self.value_hint)
        units_layout = QtWidgets.QHBoxLayout()
        self.from_unit = QtWidgets.QComboBox()
        self.to_unit = QtWidgets.QComboBox()
        for combo in (self.from_unit, self.to_unit):
            combo.addItems(UNITS)
        self.from_unit.setCurrentText("m")
        self.from_unit.setToolTip("Input unit: mm, cm, metres, inches or feet")
        self.to_unit.setToolTip("Result unit: mm, cm, metres, inches or feet")
        units_layout.addWidget(self.from_unit)
        units_layout.addWidget(QtWidgets.QLabel("→"))
        units_layout.addWidget(self.to_unit)
        converter_layout.addLayout(units_layout)
        self.reverse_button = QtWidgets.QPushButton("⇄  Swap / Reverse")
        self.reverse_button.setToolTip("Use the result as the new input, swap units, and reverse radius/diameter mode.")
        converter_layout.addWidget(self.reverse_button)
        self.result_label = QtWidgets.QLabel("Radius")
        converter_layout.addWidget(self.result_label)
        self.result = QtWidgets.QLabel()
        self.result.setObjectName("value")
        self.result.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        converter_layout.addWidget(self.result)
        self.copy_button = QtWidgets.QPushButton("Copy result")
        converter_layout.addWidget(self.copy_button)
        self.apply_button = QtWidgets.QPushButton("UPDATE SELECTED PARAMETER")
        self.apply_button.setObjectName("apply")
        root.addWidget(self.apply_button)
        self.status = QtWidgets.QLabel("Converter works without a selection.")
        self.status.setWordWrap(True)
        self.status.setMinimumHeight(34)
        root.addWidget(self.status)
        note = QtWidgets.QLabel("Scene units are preserved.  •  Ctrl+Z to undo an update.")
        note.setObjectName("muted")
        root.addWidget(note)
        for button in self.findChildren(QtWidgets.QPushButton):
            button.setAutoDefault(False)
            button.setDefault(False)
        self.parameters.currentIndexChanged.connect(self.parameter_changed)
        self.input.textEdited.connect(self.edited)
        self.input.textChanged.connect(self.calculate)
        self.input.returnPressed.connect(self.equals)
        self.mode.currentIndexChanged.connect(self.calculate)
        self.from_unit.currentIndexChanged.connect(self.calculate)
        self.to_unit.currentIndexChanged.connect(self.calculate)
        self.read_button.clicked.connect(self.use_parameter)
        self.copy_button.clicked.connect(self.copy_result)
        self.reverse_button.clicked.connect(self.reverse)
        self.apply_button.clicked.connect(self.apply)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.refresh)
        self.timer.start(350)
        self.calculate()
        self.refresh()

    def entry(self):
        index = self.parameters.currentIndex()
        return self.items[index] if 0 <= index < len(self.items) else None

    def edited(self, _text):
        self.manual_input = True
        self.loaded_text = None

    def input_number(self):
        if self.loaded_value is not None and self.input.text() == self.loaded_text:
            return self.loaded_value
        return evaluate(self.input.text(), self.loaded_value)

    def set_number(self, value):
        self.loaded_value = number(value)
        self.loaded_text = display(value)
        self.input.setText(self.loaded_text)
        self.calculate()

    def math_key(self, key):
        if key == "=":
            self.equals()
            return
        if key == "C":
            self.loaded_value = None
            self.loaded_text = None
            self.input.clear()
        else:
            if key in ("+", "−", "×", "÷") and self.loaded_value is not None and self.input.text() == self.loaded_text:
                self.input.setText("value")
                self.input.setCursorPosition(len(self.input.text()))
            self.input.insert(" " + key + " " if key in ("+", "−", "×", "÷") else key)
        self.manual_input = True
        self.input.setFocus()

    def equals(self):
        try:
            self.set_number(self.input_number())
            self.manual_input = True
            self.status.setText("Calculated. Click Update to apply the converted result.")
        except ValueError as exc:
            self.status.setText(str(exc))

    def use_parameter(self):
        # Calculations start in the visible current-value unit, without a radius transform.
        self.mode.setCurrentIndex(2)
        self.from_unit.setCurrentText(self.to_unit.currentText())
        self.load_current()

    def calculate(self, *_args):
        mode = self.mode.currentIndex()
        self.input_label.setText(("Diameter", "Radius", "Length")[mode])
        self.result_label.setText(("Radius", "Diameter", "Result")[mode])
        try:
            value = self.input_number()
            self.result_mm = convert(value, self.from_unit.currentText(), "mm", mode)
            result = convert(value, self.from_unit.currentText(), self.to_unit.currentText(), mode)
            self.result.setText(f"{display(result)} {self.to_unit.currentText()}")
            self.result.setToolTip(str(result) + " " + self.to_unit.currentText())
            self.input.setToolTip("Calculated input: " + str(value))
            self.value_hint.setText("value = " + display(self.loaded_value) + " " + self.from_unit.currentText() if self.loaded_value is not None else "Supports +, −, ×, ÷ and parentheses")
        except ValueError as exc:
            self.result_mm = None
            self.result.setText("—")
            self.input.setToolTip(str(exc))
            self.value_hint.setText(str(exc))
        self.copy_button.setEnabled(self.result_mm is not None)
        self.reverse_button.setEnabled(self.result_mm is not None)
        self.apply_button.setEnabled(self.result_mm is not None and self.entry() is not None and self.last_mm is not None)
        self.show_current()

    def show_current(self):
        if self.last_mm is None:
            self.current.setText("—")
        else:
            result = convert(self.last_mm, "mm", self.to_unit.currentText(), 2)
            self.current.setText(f"{display(result)} {self.to_unit.currentText()}")
            self.current.setToolTip(str(result) + " " + self.to_unit.currentText())

    def parameter_changed(self, *_args):
        self.load_current()

    def read_current(self):
        entry = self.entry()
        self.last_mm = None
        self.scene.clear()
        if entry is not None:
            self.last_mm, scene_text = self.host.read(entry)
            self.scene.setText("Scene display: " + scene_text)
        self.read_button.setEnabled(self.last_mm is not None)
        self.calculate()

    def load_current(self, *_args):
        try:
            self.read_current()
            if self.last_mm is not None:
                value = equivalent_input(self.last_mm, self.from_unit.currentText(), self.mode.currentIndex())
                self.set_number(value)
                self.manual_input = False
                self.status.setText("Equivalent input loaded. The result matches the current parameter.")
        except Exception as exc:
            self.failure(exc)

    def refresh(self):
        try:
            signature, node, targets = self.host.snapshot()
            if signature != self.signature:
                self.signature = signature
                self.items = self.host.entries(targets) if node is not None else []
                self.parameters.blockSignals(True)
                self.parameters.clear()
                self.parameters.addItems([entry.label for entry in self.items])
                self.parameters.blockSignals(False)
                self.status.setText("Choose a measurement and click Update." if self.items else "Converter mode. Select one parametric object to enable Update.")
                self.read_current()
                if self.items and not self.manual_input:
                    self.load_current()
            self.object_label.setText(self.host.name(node) if node is not None else "Select one object" if signature[-1] else "No object selected")
            self.read_current()
        except Exception as exc:
            self.last_mm = None
            self.apply_button.setEnabled(False)
            self.read_button.setEnabled(False)
            self.current.setText("Unavailable")
            self.status.setText(str(exc))

    def copy_result(self):
        if self.result_mm is not None:
            QtWidgets.QApplication.clipboard().setText(self.result.text())
            self.status.setText("Result copied.")

    def reverse(self):
        if self.result_mm is None:
            return
        mode = self.mode.currentIndex()
        source = self.from_unit.currentText()
        target = self.to_unit.currentText()
        # Use the unrounded result, not the visible result label.
        result = convert(self.input_number(), source, target, mode)
        for widget in (self.mode, self.from_unit, self.to_unit, self.input):
            widget.blockSignals(True)
        self.from_unit.setCurrentText(target)
        self.to_unit.setCurrentText(source)
        self.mode.setCurrentIndex({0: 1, 1: 0, 2: 2}[mode])
        self.loaded_value = number(result)
        self.loaded_text = display(result)
        self.input.setText(self.loaded_text)
        for widget in (self.mode, self.from_unit, self.to_unit, self.input):
            widget.blockSignals(False)
        self.manual_input = True
        self.calculate()
        self.status.setText("Reversed: the previous result is now the input.")

    def apply(self):
        entry = self.entry()
        if entry is None or self.result_mm is None:
            return
        try:
            stored = self.host.apply(self.signature, entry, self.result_mm)
            requested = float(self.result_mm)
            self.read_current()
            if not math.isclose(stored, requested, rel_tol=1e-6, abs_tol=1e-7):
                self.status.setText("3ds Max limited the value. Current value shows the stored result.")
            else:
                self.status.setText("Parameter updated. Press Ctrl+Z in 3ds Max to undo.")
        except Exception as exc:
            self.failure(exc)

    def failure(self, exc):
        self.status.setText(str(exc))
        traceback.print_exc()

    def closeEvent(self, event):
        self.timer.stop()
        super().closeEvent(event)


_dialog = None


def show():
    global _dialog
    from .host import MaxHost
    import qtmax
    if _dialog is not None:
        try:
            _dialog.close()
        except RuntimeError:
            pass
    _dialog = ConverterDialog(MaxHost(), qtmax.GetQMaxMainWindow())
    try:
        qtmax.DisableMaxAcceleratorsOnFocus(_dialog, True)
    except (AttributeError, TypeError):
        pass
    _dialog.show()
    _dialog.raise_()
    _dialog.activateWindow()
    return _dialog
