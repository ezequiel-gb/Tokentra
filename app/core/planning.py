"""Exact integer context planning, independent of Qt and tokenisation."""
from dataclasses import dataclass
from fractions import Fraction
import re


def parse_tokens(text: str, minimum: int = 0) -> int:
    value = text.strip()
    if not re.fullmatch(r"(?:[0-9]+|[1-9][0-9]{0,2}(?:,[0-9]{3})+)", value):
        raise ValueError("Enter a whole number, with optional thousands separators.")
    try:
        result = int(value.replace(",", ""))
    except ValueError as error:
        raise ValueError("This number has too many digits to display.") from error
    if result < minimum:
        raise ValueError("Enter a positive whole number." if minimum == 1 else "Enter zero or a positive whole number.")
    return result


@dataclass(frozen=True)
class Allocation:
    capacity: int
    transcript: int
    allowance: int

    def __post_init__(self):
        for name, minimum in (("capacity", 1), ("transcript", 0), ("allowance", 0)):
            value = getattr(self, name)
            if type(value) is not int or value < minimum:
                raise ValueError(f"{name} must be an integer greater than or equal to {minimum}")

    @property
    def planned(self):
        return self.transcript + self.allowance

    @property
    def unallocated(self):
        return self.capacity - self.planned

    @property
    def excess(self):
        return max(0, self.planned - self.capacity)

    @property
    def transcript_percent(self):
        return Fraction(self.transcript * 100, self.capacity)

    @property
    def planned_percent(self):
        return Fraction(self.planned * 100, self.capacity)

    def segments(self, pixels: int):
        """Clipped integer pixel widths; excess is reported separately, never hidden."""
        transcript_end = pixels * min(self.transcript, self.capacity) // self.capacity
        allowance_end = pixels * min(self.planned, self.capacity) // self.capacity
        return transcript_end, allowance_end - transcript_end, pixels - allowance_end


def percent_label(value: Fraction) -> str:
    # Round half up to two decimals, without a float conversion or lost totals.
    numerator, denominator = value.numerator * 100, value.denominator
    rounded = (numerator * 2 + denominator) // (denominator * 2)
    return f"{rounded // 100:,}.{rounded % 100:02d}%"
