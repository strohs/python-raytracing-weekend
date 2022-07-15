from unittest import TestCase

from common import Point3
from materials import Lambertian
from hittables.primitives import Sphere
from textures import SolidColor


class TestSphere(TestCase):

    def test_has_a_bounding_box_of_min0_and_max2(self):
        tex = SolidColor.from_rgb(0.5, 0.5, 0.5)
        mat = Lambertian(tex)
        sphere = Sphere(Point3(1.0, 1.0, 1.0), 1.0, mat)
        aabb = sphere.bounding_box(1.0, 1.0)
        self.assertIsNotNone(aabb)
        self.assertEqual(aabb.min, Point3(0.0, 0.0, 0.0))
        self.assertEqual(aabb.max, Point3(2.0, 2.0, 2.0))
