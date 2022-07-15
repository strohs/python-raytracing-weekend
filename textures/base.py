from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass

from common import ColorRgb, Point3, Vec3
import math


def get_sphere_uv(p: Vec3) -> (float, float):
    """
    Computes the `u,v` surface coordinates for a sphere given its center point.
    :param: p - the center point of a unit sphere centered at the origin.
    :return: a tuple `(u,v)`, containing the sphere's u,v coordinates
    """
    phi = math.atan2(p.z, p.x)
    theta = math.asin(p.y)
    u = 1.0 - (phi + math.pi) / (2.0 * math.pi)
    v = (theta + math.pi / 2.0) / math.pi
    return u, v


@dataclass
class Texture(ABC):
    """
    A Base class for Hittables that have a texture.
    A texture in graphics is usually a function that makes the colors on a surface procedural.
    This procedure can be synthesis code, or it could be an image lookup, or a combination of both.
    """
    @abstractmethod
    def value(self, u: float, v: float, p: Point3) -> ColorRgb:
        """
        returns the color of the texture at the given 'u,v' coordinate and point 'p'
        :param u:
        :param v:
        :param p:
        :return:
        """
        pass

