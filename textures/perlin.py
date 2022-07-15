import array as arr
import copy
import math
import random
from dataclasses import dataclass
from typing import List

from common import Vec3, Point3

POINT_COUNT = 256


@dataclass
class Perlin:
    """
    Utility class for generating random perlin noise.

    Textures that wish to add perlin noise to themselves should call the "turb()" method
    """

    def __init__(self):
        perm_x = arr.array('i', [i for i in range(POINT_COUNT)])
        perm_y = arr.array('i', [i for i in range(POINT_COUNT)])
        perm_z = arr.array('i', [i for i in range(POINT_COUNT)])
        rand_vecs = [Vec3.random_range(-1.0, 1.0).unit_vector() for _ in range(POINT_COUNT)]

        random.shuffle(perm_x)
        random.shuffle(perm_y)
        random.shuffle(perm_z)

        self.perm_x = perm_x
        self.perm_y = perm_y
        self.perm_z = perm_z
        self.rand_vecs = rand_vecs

    def turb(self, point: Point3, depth: int) -> float:
        """
        Generates turbulence on a texture via repeated calls to `noise()`.

        :param point: the 3D point to generate noise around
        :param depth: number of times to call the noise() function
        :return:
        """
        accum = 0.0
        temp_p = copy.copy(point)
        weight = 1.0

        for _ in range(depth):
            accum += weight * self._noise(temp_p)
            weight *= 0.5
            temp_p *= 2.0

        return abs(accum)

    def _noise(self, point: Point3) -> float:
        """
        Returns a random perlin noise value.
        It takes a 3D point as input, `point`, and always returns the same "randomish number".
        Nearby points should return similar numbers. Another important part of Perlin noise is
        that it be simple and fast, so it’s usually done as a hack...

        :param point:
        :return: random"ish" perlin noise value
        """
        u = point.x - math.floor(point.x)
        v = point.y - math.floor(point.y)
        w = point.z - math.floor(point.z)

        i = math.floor(point.x)
        j = math.floor(point.y)
        k = math.floor(point.z)

        # 2x2x2 matrix
        c = [[[Vec3() for col in range(2)] for col in range(2)] for row in range(2)]

        for di in range(2):
            for dj in range(2):
                for dk in range(2):
                    idx = self.perm_x[(i + di) & 255] ^ self.perm_y[(j + dj) & 255] ^ self.perm_z[(k + dk) & 255]
                    c[di][dj][dk] = self.rand_vecs[idx]

        return Perlin.perlin_interp(c, u, v, w)

    @staticmethod
    def perlin_interp(c: List[List[List[Vec3]]], u: float, v: float, w: float) -> float:
        """
        trilinear interpolation used to smooth out perlin noise

        :param c:
        :param u:
        :param v:
        :param w:
        :return:
        """
        uu = u * u * (3.0 - 2.0 * u)
        vv = v * v * (3.0 - 2.0 * v)
        ww = w * w * (3.0 - 2.0 * w)

        accum = 0.0
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    weight_v = Vec3(u - float(i), v - float(j), w - float(k))
                    accum += (i * uu + (1.0 - i) * (1.0 - uu)) *\
                             (j * vv + (1.0 - j) * (1.0 - vv)) *\
                             (k * ww + (1.0 - k) * (1.0 - ww)) * \
                             (c[i][j][k]).dot(weight_v)
        return accum

