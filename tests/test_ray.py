from unittest import TestCase

from common import Vec3, Point3, Ray


class TestRay(TestCase):

    def test_ray_fields_default_to_0(self):
        ray = Ray()
        self.assertEqual(ray.orig, Vec3(0.0, 0.0, 0.0))
        self.assertEqual(ray.dir, Vec3(0.0, 0.0, 0.0))
        self.assertEqual(ray.time, 0.0)

    def test_time(self):
        ray = Ray(Vec3(1.0, 2.0, 3.0), Vec3(5.0, 6.0, 7.0), 12.3)
        self.assertEqual(ray.time, 12.3)

    def test_origin(self):
        ray = Ray(Vec3(1.0, 2.0, 3.0), Vec3(5.0, 6.0, 7.0), 12.3)
        self.assertEqual(ray.orig, Vec3(1.0, 2.0, 3.0))

    def test_direction(self):
        ray = Ray(Vec3(1.0, 2.0, 3.0), Vec3(5.0, 6.0, 7.0), 12.3)
        self.assertEqual(ray.dir, Vec3(5.0, 6.0, 7.0))

    def test_at(self):
        t = 2.0
        ray = Ray(Point3(1.0, 2.0, 3.0), Vec3(4.0, 5.0, 6.0), 1.0)
        self.assertEqual(ray.at(t), Point3(9.0, 12.0, 15.0))
