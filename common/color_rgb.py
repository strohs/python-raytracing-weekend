from __future__ import annotations

import random
from dataclasses import dataclass


@dataclass
class ColorRgb:
    """
    A RGB Color component.

    The default implementation returns the color black (0.0, 0.0, 0.0) if no color values
    are supplied
    """
    r: float = 0.0
    g: float = 0.0
    b: float = 0.0

    def to_tuple(self) -> (float, float, float):
        """
        returns the r,g,b values of this ColorRgb as a tuple: (r,g,b)
        """
        return self.r, self.g, self.b

    @staticmethod
    def random() -> ColorRgb:
        """
        returns a `ColorRgb` with it's `r,g,b` fields set to a random f64 in the range `0..1`
        """
        return ColorRgb(
            random.random(),
            random.random(),
            random.random()
        )

    @staticmethod
    def random_range(min: float, max: float) -> ColorRgb:
        """
        returns a `ColorRgb` with each `r,g,b` field set to a random f64 in the range `[min..max]`
        """
        return ColorRgb(
            random.uniform(min, max),
            random.uniform(min, max),
            random.uniform(min, max)
        )

    def __add__(self, other: ColorRgb):
        """
        adds each field of this ColorRgb to the corresponding fields of the other ColorRgb
        :param other: ColorRgb to add to this ColorRgb
        :return: ColorRgb
        """
        if not isinstance(other, ColorRgb):
            return NotImplemented
        return ColorRgb(
            self.r + other.r,
            self.g + other.g,
            self.b + other.b
        )

    def __iadd__(self, other: ColorRgb):
        """
        add assign the corresponding fields of this ColorRgb and other, storing the results in this ColorRgb
        :param other: the ColorRgb to add
        """
        if not isinstance(other, ColorRgb):
            return NotImplemented
        return ColorRgb(
            self.r + other.r,
            self.g + other.g,
            self.b + other.b
        )

    def __mul__(self, other: float) -> ColorRgb:
        """
        multiplies each field of this ColorRgb by other and returns a new ColorRgb
        """
        if not isinstance(other, float):
            return NotImplemented
        return ColorRgb(
            self.r * other,
            self.g * other,
            self.b * other
        )

    def __rmul__(self, other: float) -> ColorRgb:
        """
        multiplies other by this ColorRgb and returns a new ColorRgb
        """
        if not isinstance(other, float):
            return NotImplemented
        return ColorRgb(
            self.r * other,
            self.g * other,
            self.b * other
        )

    def __pow__(self, other: ColorRgb) -> ColorRgb:
        """
        multiplies the corresponding fields of this ColorRgb and other
        :param other: ColorRgb
        :return: a new ColorRgb containing the results of the multiplication
        """
        if not isinstance(other, ColorRgb):
            return NotImplemented
        return ColorRgb(
            self.r * other.r,
            self.g * other.g,
            self.b * other.b
        )
