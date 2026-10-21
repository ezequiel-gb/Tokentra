from PySide6.QtCore import Qt, QSize, QRectF, QSignalBlocker
from PySide6.QtGui import QColor, QPainter, QPainterPath
from PySide6.QtWidgets import (QWidget, QScrollArea, QVBoxLayout, QHBoxLayout, QGridLayout,
                              QFrame, QLabel, QLineEdit, QStackedWidget, QSizePolicy)
from app.core.planning import Allocation, parse_tokens, percent_label
from math import ceil


class ModeStack(QStackedWidget):
    """A hidden planning page must not enlarge the original counter dashboard."""
    def sizeHint(self):
        current = self.currentWidget()
        return current.sizeHint() if current else QSize(0, 100)

    def minimumSizeHint(self):
        return QSize(0, 100)


class AllocationBar(QWidget):
    def __init__(self):
        super().__init__()
        self.allocation = None
        self.setFixedHeight(20)
        self.setAccessibleName("Context allocation bar")

    def set_allocation(self, allocation):
        self.allocation = allocation
        self.setAccessibleDescription("Pending or invalid scenario" if allocation is None else
            f"Transcript {allocation.transcript:,}; allowance {allocation.allowance:,}; "
            f"unallocated {allocation.unallocated:,}; excess {allocation.excess:,} tokens.")
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        bounds = QRectF(0, 0, self.width(), self.height())
        path = QPainterPath()
        path.addRoundedRect(bounds, 7, 7)
        painter.setClipPath(path)
        painter.fillRect(bounds, QColor("#10263d"))
        if self.allocation is not None:
            widths = self.allocation.segments(max(0, self.width()))
            x = 0
            for width, colour in zip(widths, ("#3178C6", "#A8DFFF", "#254660")):
                painter.fillRect(QRectF(x, 0, width, self.height()), QColor(colour))
                x += width


class PlanningDashboard(QScrollArea):
    def __init__(self, preferences):
        super().__init__()
        self.setObjectName("contextScroll")
        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setAccessibleName("Context Planning dashboard")
        self.tokens = None
        self.count_status = "Waiting for text count…"
        self.allocation = None
        self.body = QWidget(objectName="planningBody")
        self.setWidget(self.body)
        content = QVBoxLayout(self.body)
        content.setContentsMargins(16, 14, 16, 14)
        content.setSpacing(12)
        content.addWidget(QLabel("CONTEXT PLANNING", objectName="eyebrow"))
        self.cards_layout = QGridLayout()
        self.cards_layout.setSpacing(10)
        self.card_frames = []
        self.values = {}
        for key, title in (("transcript", "TRANSCRIPT TOKENS"), ("capacity", "CONTEXT CAPACITY"),
                           ("planned", "PLANNED ALLOCATION"), ("unallocated", "ESTIMATED UNALLOCATED")):
            frame = QFrame(objectName="contextCard")
            frame.setMinimumWidth(0)
            column = QVBoxLayout(frame)
            column.setContentsMargins(12, 10, 12, 10)
            label = QLabel(title, objectName="eyebrow")
            label.setWordWrap(True)
            value = QLabel("…", objectName="planningValue")
            value.setAccessibleName(title.title())
            value.setTextFormat(Qt.TextFormat.PlainText)
            value.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse | Qt.TextInteractionFlag.TextSelectableByKeyboard)
            value.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
            value.setWordWrap(True)
            value.setMinimumWidth(0)
            value.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
            column.addWidget(label)
            column.addWidget(value)
            self.values[key] = value
            self.card_frames.append(frame)
        content.addLayout(self.cards_layout)
        self.inputs_layout = QGridLayout()
        self.inputs_layout.setSpacing(12)
        self.capacity_box, self.capacity = self.input_box("Context capacity (your scenario)", "128,000")
        self.allowance_box, self.allowance = self.input_box("Additional token allowance (optional)", "8,000")
        self.capacity.setAccessibleDescription("Editable example, not a model capacity claim. Positive whole tokens.")
        self.allowance.setAccessibleDescription("Your own reserve, not measured ChatGPT overhead. Zero or positive whole tokens.")
        for control, key, default, minimum in ((self.capacity, "context_capacity", 128000, 1),
                                               (self.allowance, "additional_allowance", 8000, 0)):
            try:
                restored = parse_tokens(str(preferences.value(key, str(default))), minimum)
            except ValueError:
                restored = default
            control.setText(f"{restored:,}")
        content.addLayout(self.inputs_layout)
        self.validation = QLabel("", objectName="planningWarning")
        self.validation.setWordWrap(True)
        self.validation.setAccessibleName("Planning input validation")
        content.addWidget(self.validation)
        self.bar = AllocationBar()
        content.addWidget(self.bar)
        legend = QLabel("● Transcript     ◇ Additional allowance     ▰ Unallocated capacity", objectName="muted")
        legend.setWordWrap(True)
        content.addWidget(legend)
        self.interpretation = QLabel("", objectName="planningInterpretation")
        self.interpretation.setTextFormat(Qt.TextFormat.PlainText)
        self.interpretation.setWordWrap(True)
        self.interpretation.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.interpretation.setAccessibleName("Context allocation interpretation")
        content.addWidget(self.interpretation)
        limitation = QLabel("Context Planning estimates how pasted text compares with a capacity you specify. "
            "It does not measure ChatGPT’s live context or guarantee how much information a model can retain. "
            "Hidden instructions, uncopied messages, compaction and omitted attachments are not measured.", objectName="muted")
        limitation.setWordWrap(True)
        content.addWidget(limitation)
        content.addStretch()
        self.capacity.textChanged.connect(self.refresh)
        self.allowance.textChanged.connect(self.refresh)
        self.capacity.editingFinished.connect(lambda: self.format_input(self.capacity, 1))
        self.allowance.editingFinished.connect(lambda: self.format_input(self.allowance, 0))
        self._columns = None
        self.reflow()
        self.refresh()

    @staticmethod
    def input_box(title, example):
        box = QWidget()
        layout = QVBoxLayout(box)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        label = QLabel(title)
        label.setWordWrap(True)
        control = QLineEdit(example)
        control.setAccessibleName(title)
        control.setAlignment(Qt.AlignmentFlag.AlignRight)
        label.setBuddy(control)
        layout.addWidget(label)
        layout.addWidget(control)
        return box, control

    def sizeHint(self):
        return QSize(700, self.body.layout().sizeHint().height())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, "_columns"):
            self.reflow()

    def reflow(self):
        margins = self.body.layout().contentsMargins()
        available = max(1, self.viewport().width() - margins.left() - margins.right() - 2)
        # Include real styled font metrics, bearings, card padding and borders.
        # Equal column stretches stop a longer heading stealing another card's
        # last digit. Keep the established font size; reflow the cards instead.
        for value in self.values.values():
            value.ensurePolished()
        number_width = max(ceil(max(value.fontMetrics().horizontalAdvance(value.text()),
                                   value.fontMetrics().boundingRect(value.text()).width()))
                           for value in self.values.values())
        required = max(180, number_width + 34)
        gap = self.cards_layout.horizontalSpacing()
        columns = next((n for n in (4, 2) if n * required + (n - 1) * gap <= available), 1)
        if columns != self._columns:
            self._columns = columns
            for frame in self.card_frames:
                self.cards_layout.removeWidget(frame)
            for index, frame in enumerate(self.card_frames):
                self.cards_layout.addWidget(frame, index // columns, index % columns)
            for index in range(4):
                self.cards_layout.setColumnStretch(index, 1 if index < columns else 0)
            for box in (self.capacity_box, self.allowance_box):
                self.inputs_layout.removeWidget(box)
            self.inputs_layout.addWidget(self.capacity_box, 0, 0)
            self.inputs_layout.addWidget(self.allowance_box, 0 if columns == 4 else 1, 1 if columns == 4 else 0)
        value_width = max(1, (available - (columns - 1) * gap) // columns - 34)
        for value in self.values.values():
            # Extremely large integers still display in full, wrapping onto
            # further lines in a single card rather than eliding or shrinking.
            wrap = value.fontMetrics().horizontalAdvance(value.text()) > value_width
            value.setWordWrap(wrap)
            height = value.heightForWidth(value_width) if wrap else value.fontMetrics().height()
            value.setMinimumHeight(max(value.fontMetrics().height(), height) + 4)

    @staticmethod
    def format_input(control, minimum):
        try:
            value = parse_tokens(control.text(), minimum)
        except ValueError:
            return
        with QSignalBlocker(control):
            control.setText(f"{value:,}")

    def set_tokens(self, tokens, status=""):
        self.tokens = tokens
        self.count_status = status or "Waiting for latest text count…"
        self.refresh()

    def refresh(self, *_):
        self.allocation = None
        errors = []
        valid = {}
        for key, control, minimum in (("capacity", self.capacity, 1), ("allowance", self.allowance, 0)):
            try:
                valid[key] = parse_tokens(control.text(), minimum)
                control.setProperty("invalid", False)
            except ValueError as error:
                control.setProperty("invalid", True)
                errors.append(("Context capacity: " if key == "capacity" else "Additional allowance: ") + str(error))
            control.style().unpolish(control)
            control.style().polish(control)
        self.validation.setText(" ".join(errors))
        self.validation.setVisible(bool(errors))
        self.values["transcript"].setText("…" if self.tokens is None else f"{self.tokens:,}")
        self.values["capacity"].setText("—" if "capacity" not in valid else f"{valid['capacity']:,}")
        if self.tokens is not None and not errors:
            self.allocation = Allocation(valid["capacity"], self.tokens, valid["allowance"])
            plan = self.allocation
            self.values["planned"].setText(f"{plan.planned:,}")
            self.values["unallocated"].setText(f"{plan.unallocated:,}")
            lead = f"Transcript: {percent_label(plan.transcript_percent)} of your capacity. Planned: {percent_label(plan.planned_percent)}. "
            if plan.excess:
                message = f"Planned allocation exceeds capacity by {plan.excess:,} tokens. The bar is clipped to capacity; no unallocated space remains."
            else:
                message = f"Estimated unallocated capacity: {plan.unallocated:,} tokens after your {plan.allowance:,}-token allowance."
            self.interpretation.setText(lead + message)
        else:
            self.values["planned"].setText("…" if self.tokens is None else "—")
            self.values["unallocated"].setText("…" if self.tokens is None else "—")
            self.interpretation.setText(self.count_status if self.tokens is None else "Correct the planning inputs to update this scenario.")
        self.bar.set_allocation(self.allocation)
        self.reflow()

    def save_preferences(self, preferences):
        for key, control, minimum in (("context_capacity", self.capacity, 1), ("additional_allowance", self.allowance, 0)):
            try:
                value = parse_tokens(control.text(), minimum)
                preferences.setValue(key, str(value))
            except ValueError:
                pass  # Invalid intermediate edits never replace a valid saved preference.
