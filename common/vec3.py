# annotations import is so that we can use Vec3 as a return type in method typings
from __future__ import annotations
from dataclasses import dataclass

import common
import math
import random


@dataclass
class Vec3:
    """
    Vec3 is the main mathematical class of the raytracer.
    It holds data about points, vectors, and colors in the 3D scene.
    The `Point3` and `ColorRgb` types alias Vec3 since they all share
    most of the same functionality.
    """
    x: float
    y: float
    z: float

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        self.x = x
        self.y = y
        self.z = z

    # r,g,b are convenience getters for the ColorRgb type to make it clearer that
    # we are getting R,G,B color values instead of x,y,z coordinates. Ideally, if we
    # wanted to use Solid Object-Oriented principles, we would create an Abstract Base
    # Class and inherit from that; however, the book uses the design implemented here,
    # and its fast and easy.
    @property
    def r(self):
        return self.x

    @property
    def g(self):
        return self.y

    @property
    def b(self):
        return self.z

    def to_tuple(self) -> (float, float, float):
        """
        returns the x,y,z values of this Vec3 as a tuple: (x,y,z)
        """
        return self.x, self.y, self.z

    def cross(self, other: Vec3) -> Vec3:
        """
        returns a new Vec3 that is the cross product of this Vec3 and other
        """
        if not isinstance(other, Vec3):
            return NotImplemented
        return Vec3(
            (self.y * other.z) - (self.z * other.y),
            (self.z * other.x) - (self.x * other.z),
            (self.x * other.y) - (self.y * other.x)
        )

    def clamped(self, cmin: float, cmax: float):
        """
        modifies this Vec3 so that each x,y,z field is between cmin and cmax
        :param cmin: minimum clamp value
        :param cmax: maximum clamp value
        :return: None
        """
        self.x = common.clamp(self.x, cmin, cmax)
        self.y = common.clamp(self.y, cmin, cmax)
        self.z = common.clamp(self.z, cmin, cmax)

    def dot(self, other: object) -> float:
        """
        :param other: Vec3 to dot against
        :return: the dot product of this Vec3 with other
        """
        if not isinstance(other, Vec3):
            return NotImplemented
        return self.x * other.x + self.y * other.y + self.z * other.z

    def length(self) -> float:
        """
        :return: this Vec3's *magnitude* a.k.a *length*: `∥⃗v∥=√x2+y2+z2`
        """
        return math.sqrt(self.length_squared())

    def length_squared(self) -> float:
        """
        :return: the square of this Vec3's length, which is equal to this Vec3 dotted with itself
        """
        return self.dot(self)

    @staticmethod
    def random() -> Vec3:
        """
        returns a `Vec3` with it's `x,y,z` fields set to a random f64 in the range `0..1`
        """
        return Vec3(
            random.random(),
            random.random(),
            random.random()
        )

    @staticmethod
    def random_range(rmin: float, rmax: float) -> Vec3:
        """
        returns a `Vec3` with it's `x,y,z` fields set to a random f64 in the range `rmin...rmax`
        """
        return Vec3(
            random.uniform(rmin, rmax),
            random.uniform(rmin, rmax),
            random.uniform(rmin, rmax)
        )

    @staticmethod
    def random_unit_sphere() -> Vec3:
        """
        returns a random `Vec3` that is within the bounds of a (imaginary) unit sphere.
        Uses "rejection method" algorithm that loops continuously until x,y,z coordinates
        are generated that lie within a unit sphere
        """
        while True:
            p = Vec3.random_range(-1.0, 1.0)
            if p.length_squared() < 1.0:
                return p

    @staticmethod
    def random_unit_vector() -> Vec3:
        """
        :return: a random `Vec3` using
        [Lambertian Diffuse](https://en.wikipedia.org/wiki/Lambert%27s_cosine_law) to generate
        a vector that is more uniformly distributed
        """
        a = random.uniform(0.0, 2.0 * math.pi)
        z = random.uniform(-1.0, 1.0)
        r = math.sqrt(1.0 - z * z)
        return Vec3(
            r * math.cos(a),
            r * math.sin(a),
            z
        )

    @staticmethod
    def random_in_hemisphere(normal: Vec3) -> Vec3:
        """
        an alternative Vec3 generation function that returns a random vector within the same
        hemisphere of the passed in `normal`. This type of method was commonly used before
        Lambertian Diffuse implemented in [`Vec3::random_unit_vector`]
        """
        in_unit_sphere = Vec3.random_unit_sphere()
        if in_unit_sphere.dot(normal) > 0.0:
            # in the same hemisphere as the normal
            return in_unit_sphere
        else:
            return -in_unit_sphere

    @staticmethod
    def random_in_unit_disk() -> Vec3:
        """
        :return: a random vector within a "unit disk". Essentially a unit vector with
        a random x,y value and z=0.0
        """
        while True:
            p = Vec3(random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0), 0.0)
            if p.length_squared() < 1.0:
                return p

    def unit_vector(self) -> Vec3:
        """
        :return: computes the unit vector of this Vec3 and returns a new Vec3
        """
        length = self.length()
        return self / length

    def __add__(self, other: Vec3):
        """
        adds each field of this Vec3 to the corresponding fields of the other Vec3 and returns a new Vec3
        :param other: Vec3 to add to this Vec3
        :return: Vec3
        """
        if not isinstance(other, Vec3):
            return NotImplemented
        return Vec3(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z
        )

    def __iadd__(self, other: Vec3):
        """
        add assign the corresponding fields of this Vec3 and other. store the results in this Vec3
        :param other: the Vec3 to add
        """
        if not isinstance(other, Vec3):
            return NotImplemented
        return Vec3(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z
        )

    def __pow__(self, other: Vec3) -> Vec3:
        """
        multiplies the corresponding fields of this Vec3 and other
        :param other: Vec3
        :return: a new Vec3 containing the results of the multiplication
        """
        if not isinstance(other, Vec3):
            return NotImplemented
        return Vec3(
            self.x * other.x,
            self.y * other.y,
            self.z * other.z
        )

    def __mul__(self, other: float) -> Vec3:
        """
        multiplies each field of this Vec3 by other and returns a new Vec3
        """
        if not isinstance(other, float):
            return NotImplemented
        return Vec3(
            self.x * other,
            self.y * other,
            self.z * other
        )

    def __rmul__(self, other: float) -> Vec3:
        """
        multiplies other by this Vec3 and returns a new Vec3
        """
        if not isinstance(other, float):
            return NotImplemented
        return Vec3(
            self.x * other,
            self.y * other,
            self.z * other
        )

    def __imul__(self, other: float) -> Vec3:
        """
        multiplies each field of this Vec3 by other and stores the result in this Vec3
        """
        if not isinstance(other, float):
            return NotImplemented
        return Vec3(
            self.x * other,
            self.y * other,
            self.z * other
        )

    def __neg__(self) -> Vec3:
        """
        returns a new Vec3 which each field of this Vec3 negated
        """
        return Vec3(
            self.x * -1.0,
            self.y * -1.0,
            self.z * -1.0
        )

    def __sub__(self, other: Vec3) -> Vec3:
        """
        subtracts corresponding fields of other from fields of this Vec3 and returns a new Vec3
        """
        if not isinstance(other, Vec3):
            return NotImplemented
        return Vec3(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z
        )

    def __truediv__(self, other: float) -> Vec3:
        """
        :param other: the float value (divisor)
        :return: divide each x,y,z field of this Vec3 by a scalar (float) value and return a new Vec3
        """
        if not isinstance(other, float):
            return NotImplemented
        return Vec3(self.x / other, self.y / other, self.z / other)

    def __idiv__(self, other: float):
        """
        divide each x,y,z field of this Vec3 by a scalar f64 value and store the result in the Vec3
        :param other: a float value to divide by
        :return:
        """
        if not isinstance(other, float):
            return NotImplemented
        return Vec3(
            self.x / other,
            self.y / other,
            self.z / other,
        )

    def __getitem__(self, item) -> float:
        """
        makes this Vec3 "indexable"
        returns the value of the x, y, or z property depending on the value of item
        0 = x
        1 = y
        2 = z
        :param item: integer index
        :return:
        """
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        elif item == 2:
            return self.z
        else:
            raise RuntimeError("Vec3 getitem index out of bounds, must be either 0, 1, or 2")

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        elif key == 2:
            self.z = value
        else:
            raise RuntimeError("Vec3 setitem index out of bounds, must be either 0, 1, or 2")


# Point3 piggybacking on top of Vec3. Mainly we use its x,y,z coordinates
Point3 = Vec3
ColorRgb = Vec3
