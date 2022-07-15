from unittest import TestCase

from common import ColorRgb


class TestColorRgb(TestCase):

    def test_add_two_colors(self):
        c1 = ColorRgb(1.0, 2.0, 3.0)
        c2 = ColorRgb(4.0, 5.0, 6.0)
        csum = c1 + c2
        self.assertEqual(csum.r, 5.0)
        self.assertEqual(csum.g, 7.0)
        self.assertEqual(csum.b, 9.0)

    def test_add_assign_two_colors(self):
        c1 = ColorRgb(1.0, 2.0, 3.0)
        c2 = ColorRgb(4.0, 5.0, 6.0)
        c1 += c2
        self.assertEqual(c1.r, 5.0)
        self.assertEqual(c1.g, 7.0)
        self.assertEqual(c1.b, 9.0)

    def test_multiply_color_by_float(self):
        c1 = ColorRgb(1.0, 2.0, 3.0)
        f = 4.0
        res = c1 * f
        self.assertEqual(res.r, 4.0)
        self.assertEqual(res.g, 8.0)
        self.assertEqual(res.b, 12.0)

    def test_multiply_float_by_color(self):
        c1 = ColorRgb(1.0, 2.0, 3.0)
        f = 4.0
        res = f * c1
        self.assertEqual(res.r, 4.0)
        self.assertEqual(res.g, 8.0)
        self.assertEqual(res.b, 12.0)

    def test_multiply_color_by_color(self):
        c1 = ColorRgb(1.0, 2.0, 3.0)
        c2 = ColorRgb(4.0, 5.0, 6.0)
        res = c1 ** c2
        self.assertEqual(res.r, 4.0)
        self.assertEqual(res.g, 10.0)
        self.assertEqual(res.b, 18.0)
