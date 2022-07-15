from __future__ import annotations
import math
import random
from dataclasses import dataclass
from typing import Optional

from common import Ray, Vec3
from hittables import Hittable, Aabb, HitRecord
from materials import Material, Isotropic
from textures import Texture


@dataclass
class ConstantMedium(Hittable):
    """
    ConstantMedium models a volume of constant density, like smoke, fog, or mist.
    A `Ray` that hits it can either scatter inside the volume or go all the way through it.
    More thin transparent volumes, like a light fog, are more likely to have rays travel
    through it. How far the ray has to travel through the volume will also determine how likely
    it is for it to make it through.
    The probability that a Ray will scatter in any small distance ΔL is:
       `probability = C ⋅ ΔL`
    where `C` is proportional to the optical density of the volume

    use the from_density() classmethod to construct an instance of this class
    """
    boundary: Hittable
    phase_function: Material
    neg_inv_density: float

    @classmethod
    def from_density(cls, boundary: Hittable, density: float, texture: Texture) -> ConstantMedium:
        """
        Returns a new `ConstantMedium` with the given boundary, density, and
        texture
        :param boundary: a hittable that defines the boundary, or "shape", of this medium
        :param density: the density amount of this material, for example 0.01 is smoke
        :param texture: texture to apply to this medium, usually a SolidTexture
        :return: a new ConstantMedium
        """
        phase_function: Material = Isotropic(texture)
        neg_inv_density = -1.0 / density
        return cls(
            boundary,
            phase_function,
            neg_inv_density
        )

    def hit(self, r: Ray, t_min: float, t_max: float) -> Optional[HitRecord]:
        """
        Returns a HitRecord if the ray `r` hits this constant medium. This hit function
        assumes the boundary shape is **convex**. It will not work for shapes like toruses or
        shapes that contain voids.
        """
        rec1 = self.boundary.hit(r, float("-inf"), float("inf"))
        if rec1:
            rec2 = self.boundary.hit(r, rec1.t + 0.00001, float("inf"))
            if rec2:
                if rec1.t < t_min:
                    rec1.t = t_min
                if rec2.t > t_max:
                    rec2.t = t_max
                if rec1.t >= rec2.t:
                    return None
                if rec1.t < 0.0:
                    rec1.t = 0.0

                ray_length = r.dir.length()
                distance_inside_boundary = (rec2.t - rec1.t) * ray_length
                hit_distance = self.neg_inv_density * math.log(random.random())

                if hit_distance > distance_inside_boundary:
                    return None
                else:
                    t = rec1.t + hit_distance / ray_length
                    p = r.at(t)
                    normal = Vec3(1.0, 0.0, 0.0)
                    material = self.phase_function
                    return HitRecord(p, normal, material, t, rec1.u, rec1.v, True)

    def bounding_box(self, t0: float, t1: float) -> Optional[Aabb]:
        # returns the bounding box of this volumes boundary
        return self.boundary.bounding_box(t0, t1)
