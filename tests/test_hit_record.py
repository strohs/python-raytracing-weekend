from unittest import TestCase

from common import Point3, Vec3
from textures import SolidColor
from materials import Lambertian
from hittables import HitRecord


class TestHitRecord(TestCase):

    def test_init_hit_record_works(self):
        point = Point3(1.0, 1.0, 1.0)
        normal = Vec3(1.5, 2.3, 3.3)
        text = SolidColor.from_rgb(100.0, 50.0, 50.0)
        mat = Lambertian(text)
        hit_rec = HitRecord(point, normal, mat, 0.0, 0.25, 0.30, True)
        self.assertIsNotNone(hit_rec)
