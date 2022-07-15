import math
from unittest import TestCase

from common import Vec3


class TestVec3(TestCase):

    def test_negation(self):
        v3 = Vec3(1.23, -2.45, 3.67)
        negated = -v3
        self.assertEqual(negated.x, -1.23)
        self.assertEqual(negated.y, 2.45)
        self.assertEqual(negated.z, -3.67)

    def test_add_two_vec3(self):
        v1 = Vec3(1.0, 2.0, 3.0)
        v2 = Vec3(4.0, 5.0, 6.0)
        vsum = v1 + v2
        self.assertEqual(vsum.x, 5.0)
        self.assertEqual(vsum.y, 7.0)
        self.assertEqual(vsum.z, 9.0)

    def test_add_assign_two_vec3(self):
        v1 = Vec3(1.0, 2.0, 3.0)
        v2 = Vec3(4.0, 5.0, 6.0)
        v1 += v2

        self.assertEqual(v1.x, 5.0)
        self.assertEqual(v1.y, 7.0)
        self.assertEqual(v1.z, 9.0)

    def test_sub_two_vec3(self):
        v1 = Vec3(1.0, 2.0, 4.0)
        v2 = Vec3(2.0, 3.0, 3.0)
        vsub = v1 - v2
        self.assertEqual(vsub.x, -1.0)
        self.assertEqual(vsub.y, -1.0)
        self.assertEqual(vsub.z, 1.0)

    def test_multiply_vec3_by_vec3(self):
        v1 = Vec3(1.0, 2.0, 3.0)
        v2 = Vec3(5.0, 6.0, 7.0)
        res = v1 ** v2
        self.assertEqual(res.x, 5.0)
        self.assertEqual(res.y, 12.0)
        self.assertEqual(res.z, 21.0)

    def test_multiply_assign_vec3_by_float(self):
        v1 = Vec3(1.0, 2.0, 3.0)
        v1 *= 5.0
        self.assertEqual(v1.x, 5.0)
        self.assertEqual(v1.y, 10.0)
        self.assertEqual(v1.z, 15.0)

    def test_multiply_vec3_by_float(self):
        v1 = Vec3(1.0, 2.0, 3.0)
        res = v1 * 2.0
        self.assertEqual(res.x, 2.0)
        self.assertEqual(res.y, 4.0)
        self.assertEqual(res.z, 6.0)

    def test_multiply_float_by_vec3(self):
        v1 = Vec3(1.0, 2.0, 3.0)
        res = 2.0 * v1
        self.assertEqual(res.x, 2.0)
        self.assertEqual(res.y, 4.0)
        self.assertEqual(res.z, 6.0)

    def test_divide_vec3_by_float(self):
        v1 = Vec3(4.0, 8.0, 12.0)
        v2 = v1 / 2.0
        self.assertEqual(v2.x, 2.0)
        self.assertEqual(v2.y, 4.0)
        self.assertEqual(v2.z, 6.0)

    def test_divide_assign_vec3_by_float(self):
        v1 = Vec3(4.0, 8.0, 12.0)
        v1 /= 4.0
        self.assertEqual(v1.x, 1.0)
        self.assertEqual(v1.y, 2.0)
        self.assertEqual(v1.z, 3.0)

    def test_vec3_constructor_defaults_to_0(self):
        v1 = Vec3()
        self.assertEqual(v1.x, 0.0)
        self.assertEqual(v1.y, 0.0)
        self.assertEqual(v1.z, 0.0)

    def test_getitem(self):
        v1 = Vec3(4.0, 8.0, 12.0)
        self.assertEqual(v1[0], 4.0)
        self.assertEqual(v1[1], 8.0)
        self.assertEqual(v1[2], 12.0)

    def test_getitem_throws_runtime_error_when_index_out_of_range(self):
        v1 = Vec3(4.0, 8.0, 12.0)
        self.assertRaises(RuntimeError, v1.__getitem__, 4)

    def test_dot(self):
        v1 = Vec3(2.0, 3.0, 4.0)
        v2 = Vec3(1.0, 2.0, 3.0)
        self.assertEqual(v1.dot(v2), 20.0)

    def test_cross(self):
        v1 = Vec3(2.0, 3.0, 4.0)
        v2 = Vec3(5.0, 6.0, 7.0)
        cross_prod = v1.cross(v2)
        self.assertEqual(cross_prod.x, -3.0)
        self.assertEqual(cross_prod.y, 6.0)
        self.assertEqual(cross_prod.z, -3.0)

    def test_clamped(self):
        v1 = Vec3(-10.0, 5.0, 9.0)
        v1.clamped(0.5, 1.0)
        self.assertEqual(v1.x, 0.5)
        self.assertEqual(v1.y, 1.0)
        self.assertEqual(v1.z, 1.0)

    def test_length(self):
        v1 = Vec3(1.0, 2.0, 3.0)
        self.assertEqual(v1.length(), math.sqrt(14.0))

    def test_length_squared(self):
        v1 = Vec3(1.0, 2.0, 3.0)
        self.assertEqual(v1.length_squared(), 14.0)

    def test_unit_vector(self):
        v1 = Vec3(1.0, 2.0, 3.0)  # length = sqrt(14.0)
        unit = v1.unit_vector()
        self.assertEqual(unit.x, 1.0 / math.sqrt(14.0))
        self.assertEqual(unit.y, 2.0 / math.sqrt(14.0))
        self.assertEqual(unit.z, 3.0 / math.sqrt(14.0))

    def test_random(self):
        v1 = Vec3.random()
        self.assertTrue(0.0 <= v1.x < 1.0)
        self.assertTrue(0.0 <= v1.y < 1.0)
        self.assertTrue(0.0 <= v1.z < 1.0)

    def test_random_range(self):
        rmin = 0.5
        rmax = 1.5
        v1 = Vec3.random_range(rmin, rmax)
        self.assertTrue(rmin <= v1.x <= rmax)
        self.assertTrue(rmin <= v1.y <= rmax)
        self.assertTrue(rmin <= v1.z <= rmax)

    def test_random_unit_sphere(self):
        v1 = Vec3.random_unit_sphere()
        self.assertIsNotNone(v1)  # want to ensure this method eventually returns a Vec3
        self.assertTrue(v1.length_squared() < 1.0)

    def test_random_unit_vector(self):
        v1 = Vec3.random_unit_vector()
        self.assertIsNotNone(v1)  # want to ensure this method eventually returns a Vec3

    def test_random_in_hemisphere(self):
        v1 = Vec3.random_in_hemisphere(Vec3(1.0, 2.0, 3.0))
        self.assertIsNotNone(v1)  # want to ensure this method eventually returns a Vec3

    def test_random_in_unit_disk(self):
        v1 = Vec3.random_in_unit_disk()
        self.assertIsNotNone(v1)  # want to ensure this method eventually returns a Vec3
