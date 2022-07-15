from unittest import TestCase

from common import Vec3
from textures import Perlin


class TestPerlin(TestCase):

    def test_perlin_constructs(self):
        perlin = Perlin()
        self.assertIsNotNone(perlin)

    def test_turb_produces_some_float_amount(self):
        perlin = Perlin()
        turb_amount = perlin.turb(Vec3(x=0.6894881403966041, y=0.17639518829650483, z=0.702489033222778), 10)
        self.assertIsNotNone(turb_amount)
