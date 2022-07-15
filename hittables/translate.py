from __future__ import annotations

import copy
from dataclasses import dataclass
from typing import Optional

from common import Vec3, Ray
from hittables import Hittable, Aabb, HitRecord


@dataclass
class Translate(Hittable):
    """
    Translates, a.k.a. moves, a hittable from its initial location to a new
    location in the world

    hittable - is the hittable object to wrap
    offset - is the amount to move it by, NOT the new location of translated hittable
    """
    # the wrapped hittable being translated
    hittable: Hittable
    # the amount to offset, or move, by
    offset: Vec3

    def hit(self, r: Ray, t_min: float, t_max: float) -> Optional[HitRecord]:
        moved_r = Ray(r.orig - self.offset, copy.copy(r.dir), r.time)

        hit_rec = self.hittable.hit(moved_r, t_min, t_max)
        if hit_rec:
            hit_rec.p += self.offset
            hit_rec.set_face_normal(moved_r, copy.copy(hit_rec.normal))
            return hit_rec
        else:
            return None

    def bounding_box(self, t0: float, t1: float) -> Optional[Aabb]:
        bbox = self.hittable.bounding_box(t0, t1)
        if bbox:
            return Aabb(bbox.min + self.offset, bbox.max + self.offset)
        else:
            return None

