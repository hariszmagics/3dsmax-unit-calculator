"""All calls into 3ds Max are isolated here and run on its main thread."""
from dataclasses import dataclass
import math

LENGTH_NAMES = (
    "radius", "radius1", "radius2", "radius3", "radius4", "diameter",
    "length", "width", "height", "thickness", "amount", "innerRadius",
    "outerRadius", "fillet", "chamfer", "size",
)


@dataclass
class Entry:
    key: tuple
    label: str
    target: object
    prop: object


class MaxHost:
    def __init__(self):
        import pymxs
        self.pymxs = pymxs
        self.rt = pymxs.runtime

    def snapshot(self):
        selected = list(self.rt.selection)
        if len(selected) != 1:
            return ("none", len(selected)), None, []
        node = selected[0]
        if not self.rt.isValidNode(node):
            return ("none", 0), None, []
        targets = [node.baseObject] + list(node.modifiers)
        signature = tuple(int(self.rt.getHandleByAnim(obj)) for obj in [node] + targets)
        return signature, node, targets

    def name(self, node):
        return str(node.name)

    def entries(self, targets):
        entries = []
        for index, target in enumerate(targets):
            available = {str(prop).lower(): prop for prop in self.rt.getPropNames(target)}
            for name in LENGTH_NAMES:
                prop = available.get(name.lower())
                if prop is None:
                    continue
                try:
                    value = self.rt.getProperty(target, prop)
                    if not isinstance(value, float):
                        continue
                    prefix = "" if index == 0 else str(target.name) + " / "
                    entries.append(Entry((int(self.rt.getHandleByAnim(target)), str(prop)),
                                         prefix + str(prop), target, prop))
                except RuntimeError:
                    continue
        return entries

    def mm_scale(self):
        scale = float(self.rt.units.decodeValue("1mm"))
        if not math.isfinite(scale) or scale <= 0:
            raise ValueError("The scene system-unit scale is invalid.")
        return scale

    def read(self, entry):
        raw = float(self.rt.getProperty(entry.target, entry.prop))
        if not math.isfinite(raw):
            raise ValueError("This parameter does not contain a finite value.")
        return raw / self.mm_scale(), str(self.rt.units.formatValue(raw))

    def apply(self, signature, entry, mm_value):
        # Recheck immediately, even if selection changed between timer ticks.
        if self.snapshot()[0] != signature:
            raise ValueError("Selection changed. Select the parameter again before updating.")
        requested = float(mm_value) * self.mm_scale()
        if not math.isfinite(requested) or abs(requested) > 3.4e38:
            raise ValueError("The converted value is outside 3ds Max's numeric range.")
        # pymxs undo contexts can suppress exceptions. Preserve the error explicitly.
        problem = None
        with self.pymxs.undo(True, "H MEDIA - Update measurement"):
            try:
                self.rt.setProperty(entry.target, entry.prop, requested)
            except Exception as exc:
                problem = str(exc)
                raise
        if problem:
            raise RuntimeError(problem)
        self.rt.redrawViews()
        return self.read(entry)[0]
