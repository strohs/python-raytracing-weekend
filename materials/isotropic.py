from dataclasses import dataclass

from common import ColorRgb, Point3, Ray, Vec3
from materials import Material, ScatterRecord

from textures import Texture


@dataclass
class Isotropic(Material):
    """
    An Isotropic material has properties that are identical in all directions
    """
    albedo: Texture

    def scatter(self, r_in: Ray, p: Point3, normal: Vec3, t: float, u: float, v: float,
                front_face: bool) -> ScatterRecord | None:
        scattered = Ray(p, Vec3.random_unit_sphere(), r_in.time)
        attenuation = self.albedo.value(u, v, p)
        return ScatterRecord(
            attenuation,
            scattered
        )

    def emitted(self, u: float, v: float, p: Point3) -> ColorRgb:
        return super().emitted(u, v, p)

