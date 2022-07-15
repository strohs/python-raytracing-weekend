from __future__ import annotations
from abc import ABC, abstractmethod

import math
from dataclasses import dataclass

from common import Vec3, Point3, Ray, ColorRgb
import materials


@dataclass
class ScatterRecord:
    """
    holds the results of how a `Material` scattered an incoming `Ray`.
    `attenuation` contains what `Color` was applied by the material to the incoming Ray
    `scattered` contains the new `Ray` that was scattered
    """
    attenuation: ColorRgb
    scattered: Ray


@dataclass
class Material(ABC):
    @abstractmethod
    def scatter(
            self,
            r_in: Ray,
            p: Point3,
            normal: Vec3,
            t: float,
            u: float,
            v: float,
            front_face: bool
    ) -> ScatterRecord | None:
        """
        Returns a ScatterRecord if this material scattered the incoming Ray `r_in`
        If this material did not scatter `r_in`, `None` is returned
        :param r_in:
        :param p: point where the hittable was hit
        :param normal: normal vector at the hit point
        :param t:
        :param u:
        :param v:
        :param front_face:
        :return:
        """
        pass

    @abstractmethod
    def emitted(self, u: float, v: float, p: Point3) -> ColorRgb:
        """
        Returns a `Color` emitted by this material. The base implementation of this method
        returns black as the default color
        :param u:
        :param v:
        :param p:
        :return:
        """
        return ColorRgb()


def reflect(v: Vec3, n: Vec3) -> Vec3:
    """
    :return: a **reflected** Vec3 between 'v' and 'n' where 'n' is a unit vector
    """
    return v - n * (2.0 * v.dot(n))


def refract(uv: Vec3, n: Vec3, etai_over_etat: float) -> Vec3:
    """
    uses Snell's law to return the direction of a Ray hitting a refractive material
    :param uv: the incoming Ray direction as a unit vector
    :param n: is the normal vector of the point that was hit on the hittable
    :param etai_over_etat: is the refractive index of the material
    """
    cos_theta: float = uv.__neg__().dot(n)
    r_out_parallel: Vec3 = etai_over_etat * (uv + cos_theta * n)
    r_out_perp: Vec3 = -1.0 * math.sqrt(1.0 - r_out_parallel.length_squared()) * n
    return r_out_parallel + r_out_perp


def schlick(cosine: float, refl_idx: float) -> float:
    """
    Schlick's approximation for determining how much light is **reflected** for a glass material
    :param cosine:
    :param refl_idx:
    :return:
    """
    r0 = (1.0 - refl_idx) / (1.0 + refl_idx)
    r0 = r0 * r0
    return r0 + (1.0 - r0) * ((1.0 - cosine) ** 5)