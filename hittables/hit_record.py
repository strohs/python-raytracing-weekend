from __future__ import annotations
from dataclasses import dataclass

from common import Vec3, Point3, Ray
import materials


# @dataclass
# class HitRecordBase:
#     """
#     Just the "base" fields of a hit Record, or everything but the material
#     """
#     p: Point3 = Point3()
#     normal: Vec3 = Vec3()
#     t: float = 0.0
#     u: float = 0.0
#     v: float = 0.0
#     front_face: bool = True


@dataclass
class HitRecord:
    """
    A "record" of where a Ray hit a hittable object.
    """

    def __init__(
            self,
            p: Point3,
            normal: Vec3,
            material: materials.Material,
            t: float,
            u: float,
            v: float,
            front_face: bool):
        """
        :param p: point on the hittable that was hit by a Ray
        :param normal: the normal vector at the point that was hit
        :param material: the type of material that was hit
        :param t: position along the Ray that hit point 'p'
        :param u: texture u coordinate
        :param v: tecture v coordinate
        :param front_face: True if Ray hit a front face of a hittable (ray hit from outside the hittable),
        False if a Ray hit a backward face of a 'hittable' (ray hit from the inside of a hittable)
        """
        self.p = p
        self.normal = normal
        self.material = material
        self.t = t
        self.u = u
        self.v = v
        self.front_face = front_face

    @staticmethod
    def _hit_front_face(ray: Ray, outward_normal: Vec3) -> bool:
        """
        :param ray: the Ray to test
        :param outward_normal: the outward normal of the hittable
        :return: returns True if the given Ray has hit a front face of a Hittable, returns False if
        the Ray hit an "inner face" of a hittable
        """
        return ray.dir.dot(outward_normal) < 0.0

    @classmethod
    def with_face_normal(cls, ray: Ray, point: Point3, outward_normal: Vec3, material: materials.Material, t: float, u: float,
                         v: float) -> HitRecord:
        """
        builds a HitRecord with `front_face` and `normal` direction computed based on the
        given Ray, `ray` and `outward_normal`
        :param ray: the Ray that hit the hittable
        :param point: the point where the Ray hit the hittable
        :param outward_normal: the outward normal of 'p'
        :param material: the type of material that was hit
        :param t: the position on `ray` that hit point 'p'
        :param u: texture u coordinate
        :param v: texture v coordinate
        :return: a new HitRecord
        """
        front_face = HitRecord._hit_front_face(ray, outward_normal)
        normal = outward_normal if front_face else -outward_normal
        return cls(point, normal, material, t, u, v, front_face)

    def set_face_normal(self, ray: Ray, outward_normal: Vec3):
        """
        computes and sets the 'front_face' and 'normal' fields of this HitRecord using the
        given ray and outward_normal
        :param ray:
        :param outward_normal:
        """
        self.front_face = HitRecord._hit_front_face(ray, outward_normal)
        self.normal = outward_normal if self.front_face else -outward_normal
