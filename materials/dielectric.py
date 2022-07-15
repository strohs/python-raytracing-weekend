import math
import random
from dataclasses import dataclass

from common import Point3, ColorRgb, Ray, Vec3
import materials
from materials import Material, ScatterRecord


@dataclass
class Dielectric(Material):
    """
    Dielectric material.

    These are clear materials such as water, glass, and diamonds. Dielectrics can reflect and refract a ray.

    :param ref_idx: the refractive index of this dielectric
    """
    ref_idx: float

    def scatter(self, r_in: Ray, p: Point3, normal: Vec3, t: float, u: float, v: float,
                front_face: bool) -> ScatterRecord | None:
        attenuation = ColorRgb(1.0, 1.0, 1.0)
        etai_over_etat = 1.0 / self.ref_idx if front_face else self.ref_idx

        unit_direction = r_in.dir.unit_vector()
        cos_theta = min((-unit_direction).dot(normal), 1.0)
        sin_theta = math.sqrt(1.0 - cos_theta ** 2)
        reflect_prob = materials.schlick(cos_theta, etai_over_etat)

        # this implementation of dielectric will randomly decide if a ray will reflect or refract
        if etai_over_etat * sin_theta > 1.0 or random.random() < reflect_prob:
            # ray is always reflected OR had a chance to reflect
            reflected = materials.reflect(unit_direction, normal)
            return ScatterRecord(attenuation, Ray(p, reflected, r_in.time))
        else:
            # ray is always refracted
            refracted = materials.refract(unit_direction, normal, etai_over_etat)
            return ScatterRecord(attenuation, Ray(p, refracted, r_in.time))

    def emitted(self, u: float, v: float, p: Point3) -> ColorRgb:
        return super().emitted(u, v, p)

