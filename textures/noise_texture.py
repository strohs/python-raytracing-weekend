from __future__ import annotations

import math
from dataclasses import dataclass, field

from common import Point3, ColorRgb, clamp
from textures import Texture, Perlin


@dataclass
class NoiseTexture(Texture):
    """
    A "noisy" marble like texture that's created using Perlin noise
    """
    # noise is the noise generation Class to use
    noise: Perlin
    # the amount to scale the noise
    scale: float

    def __init__(self, scale: float):
        """

        :param scale: the amount to scale the noise by
        """
        self.noise = Perlin()
        self.scale = scale

    def value(self, u: float, v: float, p: Point3) -> ColorRgb:
        # this should generate a marble like noisy texture
        color = ColorRgb(1.0, 1.0, 1.0)
        noise_amt = 1.0 + math.sin(self.scale * p.z + 10.0 * self.noise.turb(p, 7))
        return color * 0.5 * noise_amt


