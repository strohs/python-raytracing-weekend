from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

from common import Point3, Ray


@dataclass(order=True)
class Aabb:
    """
    An Axis Aligned Bounding Box that can be used to surround a Hittable
    """
    min: Point3 = Point3(float('inf'), float('inf'), float('inf'))
    max: Point3 = Point3(float('-inf'), float('-inf'), float('-inf'))

    def hit(self, r: Ray, t_min: float, t_max: float) -> Optional[(float, float)]:
        """
        tests if a Ray hit this bounding box.
        This hit function was developed by Andrew Kensler at Pixar
        :param r: the Ray to test
        :param t_min:  the positions on the Ray that "intersected" the bounding box.
        :param t_max:  the positions on the Ray that "intersected" the bounding box.
        :return: `(tmin, tmax)` if this bounding box was hit by the Ray `r`, else `None`.
        """
        tmin = t_min
        tmax = t_max
        for a in range(3):
            inv_d = 0.0
            t0 = 0.0
            t1 = 0.0
            if a == 0:
                inv_d = 1.0 / r.dir.x
                t0 = (self.min.x - r.orig.x) * inv_d
                t1 = (self.max.x - r.orig.x) * inv_d
            if a == 1:
                inv_d = 1.0 / r.dir.y
                t0 = (self.min.y - r.orig.y) * inv_d
                t1 = (self.max.y - r.orig.y) * inv_d
            if a == 2:
                inv_d = 1.0 / r.dir.z
                t0 = (self.min.z - r.orig.z) * inv_d
                t1 = (self.max.z - r.orig.z) * inv_d

            if inv_d < 0.0:
                temp = t0
                t0 = t1
                t1 = temp

            tmin = t0 if t0 > tmin else tmin
            tmax = t1 if t1 < tmax else tmax

            if tmax <= tmin:
                return None

        return tmin, tmax

    @staticmethod
    def surrounding_box(box0: Aabb, box1: Aabb) -> Aabb:
        """
        :param box0:
        :param box1:
        :return: an axis-aligned bounding box, that surrounds `box0` **and** `box1`
        """
        small: Point3 = Point3(
            min(box0.min.x, box1.min.x),
            min(box0.min.y, box1.min.y),
            min(box0.min.z, box1.min.z))
        big = Point3(
            max(box0.max.x, box1.max.x),
            max(box0.max.y, box1.max.y),
            max(box0.max.z, box1.max.z))

        return Aabb(small, big)
