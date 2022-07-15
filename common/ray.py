from __future__ import annotations
from dataclasses import dataclass
from common import Vec3, Point3


@dataclass
class Ray:
    """
    A three-dimensional Ray consisting of an origin point, a direction, and a
    moment in time that the Ray existed for
    """
    orig: Point3 = Point3()
    dir: Vec3 = Vec3()
    time: float = 0.0

    def at(self, t: float) -> Point3:
        """
        computes the result of the function: P(t) = A + tb
        where A= this Ray's origin point, t= the ray parameter, b = this Ray's direction

        :param t: ray parameter
        :return: the point, on this Ray, "at" the ray parameter "t"
        """
        return self.orig + t * self.dir
