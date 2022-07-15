from unittest import TestCase

from common import Point3
from hittables import Aabb


class TestAabb(TestCase):
    def test_aabb_equal(self):
        bb1 = Aabb(Point3(0.5, 1.0, 1.5), Point3(2.5, 3.0, 3.5))
        bb2 = Aabb(Point3(0.5, 1.0, 1.5), Point3(2.5, 3.0, 3.5))
        self.assertEqual(bb1, bb2)
