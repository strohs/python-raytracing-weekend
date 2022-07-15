from __future__ import annotations

import math
import random
from dataclasses import dataclass

import common
from common import Ray
from common import Vec3, Point3


@dataclass
class Camera:
    """
    A positionable `Virtual Camera` with a configurable vertical field of view, aperture,
    focus distance and shutter open/close time.
    All `Ray`s in this ray-tracer originate from the `Camera` via calls to its `get_ray(s,t)`
    function.
    Use the CameraBuilder class to build an instance of Camera
    """
    image_width: int

    image_height: int

    # camera's origin point
    look_from: Point3

    # camera's lens radius, larger value will produce more of a de-focus blur
    lens_radius: float
    lower_left_corner: Point3
    horizontal: Vec3
    vertical: Vec3
    u: Vec3
    v: Vec3
    open_time: float
    close_time: float

    def get_ray(self, s: float, t: float) -> Ray:
        """
        get a Ray based on this camera's properties
        :param s: horizontal offset amount
        :param t: vertical offset amount
        :return: a Ray that originates from this camera's origin, with its direction pointing towards
        the given "s" and "t" offsets
        """
        # generate a random point on the unit disk
        rd = self.lens_radius * Vec3.random_in_unit_disk()
        # compute the ray's offset origin
        offset = self.u * rd.x + self.v * rd.y
        # the direction the camera is "pointing at"
        direction = self.lower_left_corner + (s * self.horizontal) + (t * self.vertical) - self.look_from - offset

        # generate a random amount of time to open this camera's shutter
        shutter_open = random.uniform(self.open_time, self.close_time)

        return Ray(self.look_from + offset, direction, shutter_open)


class CameraBuilder:
    """
    A Builder class for constructing a Camera.
    Call all the provided methods and then lastly call the build() method to build a camera object
    """

    def __init__(self):
        self._look_from: Point3 = Point3()
        self._look_at: Point3 = Point3()
        self._vup: Vec3 = Vec3()
        self._vfov: float = 0.0
        self._aspect_ratio: float = 0.0
        self._image_width: int = 0
        self._aperture: float = 0.0
        self._focus_dist: float = 0.0
        self._open_time: float = 0.0
        self._close_time: float = 0.0

    def look_from(self, look_from: Point3):
        self._look_from = look_from
        return self

    def look_at(self, look_at: Point3):
        self._look_at = look_at
        return self

    def up_direction(self, up_direction: Vec3):
        self._vup = up_direction
        return self

    def vertical_field_of_view(self, vfov_degrees: float):
        self._vfov = vfov_degrees
        return self

    def aspect_ratio(self, aspect_ratio: float):
        self._aspect_ratio = aspect_ratio
        return self

    def image_width(self, image_width: int):
        self._image_width = image_width
        return self

    def aperture(self, aperture: float):
        self._aperture = aperture
        return self

    def focus_distance(self, focus_distance: float):
        self._focus_dist = focus_distance
        return self

    def open_close_time(self, open_time: float, close_time: float):
        self._open_time = open_time
        self._close_time = close_time
        return self

    def build(self) -> Camera:
        w = (self._look_from - self._look_at).unit_vector()
        u = self._vup.cross(w).unit_vector()
        v = w.cross(u)

        vp_width, vp_height = _get_viewport_width_height(self._vfov, self._aspect_ratio)
        horizontal = self._focus_dist * vp_width * u
        vertical = self._focus_dist * vp_height * v
        lower_left_corner = self._look_from - horizontal / 2.0 - vertical / 2.0 - self._focus_dist * w
        lens_radius = self._aperture / 2.0

        return Camera(
            self._image_width,
            int(self._image_width / self._aspect_ratio),
            self._look_from,
            lens_radius,
            lower_left_corner,
            horizontal,
            vertical,
            u,
            v,
            self._open_time,
            self._close_time
        )


def _get_viewport_width_height(vfov: float, aspect_ratio: float) -> (float, float):
    """
    Computes the viewport width and height given a vertical field of view **in degrees**
    and an aspect ratio.
    :param vfov: vertical field of view
    :param aspect_ratio: aspect ratio
    :return: a tuple of `(viewport_width, viewport_height)`
    """
    theta = common.degrees_to_radians(vfov)
    h = math.tan(theta / 2.0)
    viewport_height = 2.0 * h
    viewport_width = aspect_ratio * viewport_height
    return viewport_width, viewport_height
