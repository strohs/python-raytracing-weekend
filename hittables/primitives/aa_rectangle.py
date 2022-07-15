from __future__ import annotations

from dataclasses import dataclass

from common import Vec3, Point3, Ray
from hittables import Hittable, HitRecord, Aabb
from materials import Material
from typing import Optional


@dataclass
class XYRect(Hittable):
    """
    A two-dimensional hittable rectangle that's aligned on the **xy plane**
    """
    x0: float
    x1: float
    y0: float
    y1: float
    # k is the planes z value
    k: float
    mat: Material

    def hit(self, r: Ray, t_min: float, t_max: float) -> Optional[HitRecord]:
        t: float = (self.k - r.orig.z) / r.dir.z
        if t < t_min or t > t_max:
            return None
        x = r.orig.x + t * r.dir.x
        y = r.orig.y + t * r.dir.y

        if x < self.x0 or x > self.x1 or y < self.y0 or y > self.y1:
            return None

        return HitRecord.with_face_normal(
            r,
            r.at(t),
            Vec3(0.0, 0.0, 1.0),
            self.mat,
            t,
            (x - self.x0) / (self.x1 - self.x0),
            (y - self.y0) / (self.y1 - self.y0))

    def bounding_box(self, t0: float, t1: float) -> Optional[Aabb]:
        # The bounding box will have non-zero width in each dimension, so pad the Z
        # dimension a small amount
        return Aabb(
            Point3(self.x0, self.y0, self.k - 0.001),
            Point3(self.x1, self.y1, self.k + 0.001)
        )


@dataclass
class XZRect(Hittable):
    """
    a 2D, `Hittable` rectangle, that's aligned on the **xz plane**
    """
    x0: float
    x1: float
    z0: float
    z1: float
    # k is the planes y value
    k: float
    mat: Material

    def hit(self, r: Ray, t_min: float, t_max: float) -> Optional[HitRecord]:
        t: float = (self.k - r.orig.y) / r.dir.y
        if t < t_min or t > t_max:
            return None

        x = r.orig.x + t * r.dir.x
        z = r.orig.z + t * r.dir.z

        if x < self.x0 or x > self.x1 or z < self.z0 or z > self.z1:
            return None

        return HitRecord.with_face_normal(
            r,
            r.at(t),
            Vec3(0.0, 1.0, 0.0),
            self.mat,
            t,
            (x - self.x0) / (self.x1 - self.x0),
            (z - self.z0) / (self.z1 - self.z0)
        )

    def bounding_box(self, t0: float, t1: float) -> Optional[Aabb]:
        # The bounding box will have non-zero width in each dimension, so pad the Y
        # dimension a small amount.
        return Aabb(
            Point3(self.x0, self.k - 0.001, self.z0),
            Point3(self.x1, self.k + 0.001, self.z1),
        )


@dataclass
class YZRect(Hittable):
    """
    a 2D, `Hittable` rectangle, that's aligned on the **yz plane**
    """
    y0: float
    y1: float
    z0: float
    z1: float
    # k is the planes y value
    k: float
    mat: Material

    def hit(self, r: Ray, t_min: float, t_max: float) -> Optional[HitRecord]:
        t: float = (self.k - r.orig.x) / r.dir.x
        if t < t_min or t > t_max:
            return None

        y = r.orig.y + t * r.dir.y
        z = r.orig.z + t * r.dir.z

        if y < self.y0 or y > self.y1 or z < self.z0 or z > self.z1:
            return None

        return HitRecord.with_face_normal(
            r,
            r.at(t),
            Vec3(1.0, 0.0, 0.0),
            self.mat,
            t,
            (y - self.y0) / (self.y1 - self.y0),
            (z - self.z0) / (self.z1 - self.z0)
        )

    def bounding_box(self, t0: float, t1: float) -> Optional[Aabb]:
        # The bounding box will have non-zero width in each dimension, so pad the X
        # dimension a small amount.
        return Aabb(
            Point3(self.k - 0.001, self.y0, self.z0),
            Point3(self.k + 0.001, self.y1, self.z1),
        )
