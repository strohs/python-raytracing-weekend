from dataclasses import dataclass

import common
import materials
from common import Ray, Point3, Vec3
from materials import ScatterRecord


@dataclass
class Metal(materials.Material):
    """
    A metallic material
    """
    albedo: common.ColorRgb
    # fuzziness of the metal
    fuzz: float

    def scatter(self, r_in: Ray, p: Point3, normal: Vec3, t: float, u: float, v: float,
                front_face: bool) -> ScatterRecord | None:
        reflected = materials.reflect(r_in.dir.unit_vector(), normal)
        # set scattered to be fuzzy metallic
        scattered = common.Ray(
            p,
            reflected + self.fuzz * common.Vec3.random_unit_sphere(),
            r_in.time
        )
        return materials.ScatterRecord(self.albedo, scattered) if scattered.dir.dot(normal) > 0.0 else None

    def emitted(self, u: float, v: float, p: common.Point3) -> common.ColorRgb:
        # this implementation of a metal materials is not emissive
        return super().emitted(u, v, p)
