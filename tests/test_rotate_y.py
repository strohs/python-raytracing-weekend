from unittest import TestCase

from hittables import RotateY
from hittables.primitives import BoxInst
from common import Point3, ColorRgb
from materials import Metal


class TestRotateY(TestCase):

    def test_rotate_y_90_degrees_generates_rotated_bounding_box(self):
        box_inst = BoxInst.from_material(
            Point3(0.0, 0.0, 0.0),
            Point3(1.0, 1.0, 1.0),
            Metal(ColorRgb(0.0, 0.0, 0.0), 0.5)
        )
        rotated = RotateY.from_hittable(box_inst, 90.0)
        self.assertIsNotNone(rotated)
        print(rotated.hittable.bounding_box(0.0, 1.0))
        print(rotated.bbox)
