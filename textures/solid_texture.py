from dataclasses import dataclass

from common import ColorRgb, Point3
from textures import Texture


@dataclass
class SolidColor(Texture):
    """
    A Solid color texture
    """
    color_value: ColorRgb

    @classmethod
    def from_rgb(cls, red: float, green: float, blue: float):
        """
        convenience constructor to build a SolidTexture give individual RGB components
        :param red:
        :param green:
        :param blue:
        """
        return cls(ColorRgb(red, green, blue))

    def value(self, u: float, v: float, p: Point3) -> ColorRgb:
        return self.color_value
