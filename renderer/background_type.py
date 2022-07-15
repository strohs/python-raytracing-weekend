"""The types of background color(s) that should be used by a renderer
Currently only two options are supported:

`Solid(Color)` - a solid color should be used for the background
`LinearInterp(from, to)` - use linear interpolation to render the background color
between from and to
"""
from dataclasses import dataclass

from common import ColorRgb


@dataclass
class SolidBackground:
    """
    A Background consisting of a single color
    """
    color1: ColorRgb


@dataclass
class LinearInterpBackground:
    """
    A Background that uses linear interpolation to render its color between frm and to
    """
    frm: ColorRgb
    to: ColorRgb


BackgroundType = SolidBackground | LinearInterpBackground

