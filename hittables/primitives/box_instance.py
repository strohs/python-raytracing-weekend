from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

from common import Point3, Ray
from hittables import Hittable, HitRecord, Aabb, FlipFace, HittableList
import hittables.primitives
from materials import Material


@dataclass
class BoxInst(Hittable):
    """
    BoxInst is a 3D box made up of six axis-aligned rectangles
    """
    box_min: Point3
    box_max: Point3
    sides: HittableList

    @classmethod
    def from_material(cls, p0: Point3, p1: Point3, mat: Material):
        """
        returns an axis-aligned BoxInst, applying the given material to all sides of the box
        :param p0: point0 of the box
        :param p1: point1 of the box
        :param mat: the Material to apply to the box
        """
        box_inst = cls(p0, p1, HittableList())

        box_inst.sides.add(hittables.primitives.XYRect(
            p0.x,
            p1.x,
            p0.y,
            p1.y,
            p1.z,
            mat
        ))

        box_inst.sides.add(FlipFace(hittables.primitives.XYRect(
            p0.x,
            p1.x,
            p0.y,
            p1.y,
            p0.z,
            mat
        )))

        box_inst.sides.add(hittables.primitives.XZRect(
            p0.x,
            p1.x,
            p0.z,
            p1.z,
            p1.y,
            mat
        ))

        box_inst.sides.add(FlipFace(hittables.primitives.XZRect(
            p0.x,
            p1.x,
            p0.z,
            p1.z,
            p0.y,
            mat
        )))

        box_inst.sides.add(hittables.primitives.YZRect(
            p0.y,
            p1.y,
            p0.z,
            p1.z,
            p1.x,
            mat
        ))

        box_inst.sides.add(FlipFace(hittables.primitives.YZRect(
            p0.y,
            p1.y,
            p0.z,
            p1.z,
            p0.x,
            mat
        )))

        return box_inst

    def hit(self, r: Ray, t_min: float, t_max: float) -> Optional[HitRecord]:
        return self.sides.hit(r, t_min, t_max)

    def bounding_box(self, t0: float, t1: float) -> Optional[Aabb]:
        return Aabb(self.box_min, self.box_max)
