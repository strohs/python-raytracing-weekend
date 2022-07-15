from __future__ import annotations

import copy
import math
from dataclasses import dataclass
from typing import Optional

import common
from common import Point3, Vec3, Ray
from hittables import Hittable, Aabb, HitRecord


@dataclass
class RotateY(Hittable):
    """
    RotateY is a hittable that wraps another hittable and applies a rotation about the
    Y-Axis to the hittable.
    To construct an instance of this class use the class-method *from_hittable(hittable, angle)*
    """
    hittable: Hittable
    sin_theta: float
    cos_theta: float
    bbox: Optional[Aabb]

    @classmethod
    def from_hittable(cls, hittable: Hittable, angle: float) -> RotateY:
        """
        Constructs a RotateY hittable, wrapping the given *hittable*, and then rotating it by *angle*
        degrees about the Y-Axis.
        The wrapped hittable must be able to generate a bounding_box else a RuntimeError will be thrown

        :param hittable: the hittable to be rotated
        :param angle: the rotation amount **in degrees**
        """
        bbox = hittable.bounding_box(0.0, 1.0)
        if not bbox:
            raise RuntimeError("cant construct a RotateY on a hittable that doesnt have a bounding box")

        sin_theta = math.sin(common.degrees_to_radians(angle))
        cos_theta = math.cos(common.degrees_to_radians(angle))
        min_point = Point3(float("inf"), float("inf"), float("inf"))
        max_point = Point3(float("-inf"), float("-inf"), float("-inf"))

        for i in range(2):
            for j in range(2):
                for k in range(2):
                    x = float(i) * bbox.max.x + (1.0 - float(i)) * bbox.min.x
                    y = float(j) * bbox.max.y + (1.0 - float(j)) * bbox.min.y
                    z = float(k) * bbox.max.z + (1.0 - float(k)) * bbox.min.z

                    new_x = cos_theta * x + sin_theta * z
                    new_z = (-sin_theta * x) + (cos_theta * z)
                    tester = Vec3(new_x, y, new_z)

                    for c in range(3):
                        min_point[c] = min(min_point[c], tester[c])
                        max_point[c] = max(max_point[c], tester[c])

        return cls(hittable, sin_theta, cos_theta, Aabb(min_point, max_point))

    def hit(self, r: Ray, t_min: float, t_max: float) -> Optional[HitRecord]:
        origin = copy.copy(r.orig)
        direction = copy.copy(r.dir)

        origin[0] = self.cos_theta * r.orig[0] - self.sin_theta * r.orig[2]
        origin[2] = self.sin_theta * r.orig[0] + self.cos_theta * r.orig[2]

        direction[0] = self.cos_theta * r.dir[0] - self.sin_theta * r.dir[2]
        direction[2] = self.sin_theta * r.dir[0] + self.cos_theta * r.dir[2]

        rotated_r = Ray(origin, direction, r.time)

        hit_rec = self.hittable.hit(rotated_r, t_min, t_max)
        if hit_rec:
            p = copy.copy(hit_rec.p)
            normal = copy.copy(hit_rec.normal)

            p[0] = self.cos_theta * hit_rec.p[0] + self.sin_theta * hit_rec.p[2]
            p[2] = -self.sin_theta * hit_rec.p[0] + self.cos_theta * hit_rec.p[2]
            normal[0] = self.cos_theta * hit_rec.normal[0] + self.sin_theta * hit_rec.normal[2]
            normal[2] = -self.sin_theta * hit_rec.normal[0] + self.cos_theta * hit_rec.normal[2]

            hit_rec.p = p
            hit_rec.set_face_normal(rotated_r, normal)

            return hit_rec
        else:
            return None

    def bounding_box(self, t0: float, t1: float) -> Optional[Aabb]:
        return self.bbox


