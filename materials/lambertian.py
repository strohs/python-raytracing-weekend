from dataclasses import dataclass

from common import ColorRgb, Vec3, Point3, Ray

from materials import Material, ScatterRecord
from textures import Texture, SolidColor


@dataclass
class Lambertian(Material):
    """
    Lambertian diffuse material
    """
    albedo: Texture

    def scatter(self, r_in: Ray, p: Point3, normal: Vec3, t: float, u: float, v: float,
                front_face: bool) -> ScatterRecord | None:
        scatter_direction: Vec3 = normal + Vec3.random_unit_vector()
        attenuation = self.albedo.value(u, v, p)
        return ScatterRecord(
            attenuation,
            Ray(p, scatter_direction, r_in.time)
        )

    def emitted(self, u: float, v: float, p: Point3) -> ColorRgb:
        return super().emitted(u, v, p)

    @classmethod
    def from_color(cls, red: float, green: float, blue: float):
        """
        returns a new Lambertian using the specified color values.
        Values should be in the range 0.0(black) to 1.0(white)
        :param red:
        :param green:
        :param blue:
        """
        return Lambertian(SolidColor.from_rgb(red, green, blue))