from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

from common import Ray
from hittables import Aabb, Hittable, HitRecord


@dataclass
class FlipFace(Hittable):
    """
    FlipFace is a wrapper class that wraps another Hittable and 'flips' its
    front face outward normal vector
    """
    wrapped: Hittable

    def hit(self, r: Ray, t_min: float, t_max: float) -> Optional[HitRecord]:
        hit_rec = self.wrapped.hit(r, t_min, t_max)
        if hit_rec:
            hit_rec.front_face = not hit_rec.front_face
            return hit_rec
        else:
            return None

    def bounding_box(self, t0: float, t1: float) -> Optional[Aabb]:
        return self.wrapped.bounding_box(t0, t1)
