from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Optional

from common import Vec3, Point3, Ray
from materials import Material
from hittables import HitRecord, Aabb, Hittable
import textures


@dataclass
class Sphere(Hittable):
    """
    A sphere primitive with a center and a radius
    """
    center: Point3
    radius: float
    material: Material

    @classmethod
    def from_coords(cls, cx: float, cy: float, cz:float, radius: float, material: Material):
        """
        constructor to create a sphere from specific x,y,x coordinates
        :param cx: sphere's x coordinate
        :param cy: sphere's y coordinate
        :param cz: sphere's z coordinate
        :param radius: sphere's radius
        :param material: Material to apply to the sphere
        :return: a new Sphere
        """
        return cls(Point3(cx, cy, cz), radius, material)

    def hit(self, r: Ray, t_min: float, t_max: float) -> Optional[HitRecord]:
        oc: Vec3 = r.orig - self.center
        a = r.dir.length_squared()
        half_b = oc.dot(r.dir)
        c = oc.length_squared() - self.radius * self.radius
        discriminant = half_b * half_b - a * c

        # if the ray hit some point on this sphere
        if discriminant > 0.0:
            root = math.sqrt(discriminant)
            t_temp = (-half_b - root) / a
            if t_max > t_temp > t_min:
                return self._build_hit_record(r, t_temp)
            t_temp = (-half_b + root) / a
            if t_max > t_temp > t_min:
                return self._build_hit_record(r, t_temp)
        return None

    def bounding_box(self, t0: float, t1: float) -> Optional[Aabb]:
        return Aabb(
            self.center - Vec3(self.radius, self.radius, self.radius),
            self.center + Vec3(self.radius, self.radius, self.radius)
        )

    def _build_hit_record(self, r: Ray, t: float) -> HitRecord:
        """
        builds a HitRecord using the given Ray: r, and time: t
        :param r: ray
        :param t: the ray parameter
        :return: HitRecord
        """
        hit_point = r.at(t)
        outward_normal = (hit_point - self.center) / self.radius
        u, v = textures.get_sphere_uv(outward_normal)
        return HitRecord.with_face_normal(
            r,
            hit_point,
            outward_normal,
            self.material,
            t,
            u,
            v
        )
