from dataclasses import dataclass

from common import Point3, ColorRgb, Ray, Vec3
from materials import Material, ScatterRecord
from textures import Texture


@dataclass
class DiffuseLight(Material):
    emit: Texture

    def scatter(self, r_in: Ray, p: Point3, normal: Vec3, t: float, u: float, v: float,
                front_face: bool) -> ScatterRecord | None:
        """
        this implementation of DiffuseLight does not emit
        """
        return None

    def emitted(self, u: float, v: float, p: Point3) -> ColorRgb:
        """
        emits this DiffuseLight's textures color value at the given u,v and p
        """
        return self.emit.value(u, v, p)
