import math
from dataclasses import dataclass
from typing import Optional

from common import Ray, Point3, Vec3
from hittables import Hittable, HitRecord, Aabb
import textures
from materials import Material


@dataclass
class MovingSphere(Hittable):
    center0: Point3
    center1: Point3
    time0: float
    time1: float
    radius: float
    material: Material

    def center(self, time: float) -> Point3:
        """
        :param time:
        :return: this sphere's center point at the given time: 'time'
        """
        return self.center0 + ((time - self.time0) / (self.time1 - self.time0)) * (self.center1 - self.center0)

    def hit(self, r: Ray, t_min: float, t_max: float) -> Optional[HitRecord]:
        # oc is this sphere's center point at the given time: t
        oc = r.orig - self.center(r.time)
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
        """
        Rake the box of the sphere at t0, and the box of the sphere at t1, and compute the
        box of those two boxes
        :param t0: time 0
        :param t1: time 1
        :return: an Aabb surrounding this sphere at both times: t0 and t1
        """
        box0 = Aabb(
            self.center(t0) - Vec3(self.radius, self.radius, self.radius),
            self.center(t0) + Vec3(self.radius, self.radius, self.radius),
        )
        box1 = Aabb(
            self.center(t1) - Vec3(self.radius, self.radius, self.radius),
            self.center(t1) + Vec3(self.radius, self.radius, self.radius),
        )
        return Aabb.surrounding_box(box0, box1)

    def _build_hit_record(self, r: Ray, t_temp: float) -> HitRecord:
        """
        helper method to build a hit record for this moving sphere
        """
        hit_point = r.at(t_temp)
        outward_normal: Vec3 = (hit_point - self.center(r.time)) / self.radius
        u, v = textures.get_sphere_uv(outward_normal)
        return HitRecord.with_face_normal(
            r,
            hit_point,
            outward_normal,
            self.material,
            t_temp,
            u,
            v
        )
