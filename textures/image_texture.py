from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt
from common import Point3, ColorRgb, clamp
from textures import Texture
from PIL import Image

COLOR_SCALE = 1.0 / 255.0


@dataclass
class ImageTexture(Texture):
    # holds the RGB values of each pixel of the image, the shape is (width, height, 3)
    data: npt.NDArray[np.int_]
    # image width
    width: int
    # image height
    height: int

    filename: str

    def __init__(self, filename: str):
        with Image.open(filename) as image:
            width, height = image.size
            self.data = np.asarray(image)
            self.width = width
            self.height = height
            self.filename = filename

    def value(self, u: float, v: float, p: Point3 = Point3()) -> ColorRgb:
        # if no texture data, return solid cyan as a debugging aide
        if len(self.data) == 0:
            return ColorRgb(0.0, 1.0, 1.0)

        # clamp texture coordinates to [0,1] x [1,0]
        u = clamp(u, 0.0, 1.0)
        v = 1.0 - clamp(v, 0.0, 1.0)  # flip v to image coordinates

        u_width = int(u * self.width)
        i = self.width - 1 if u_width >= self.width else u_width

        v_height = int(v * self.height)
        j = self.height - 1 if v_height >= self.height else v_height

        r, g, b = self.data[j][i]

        return ColorRgb(
            r * COLOR_SCALE,
            g * COLOR_SCALE,
            b * COLOR_SCALE
        )
