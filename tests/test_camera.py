from unittest import TestCase

import common
from common import CameraBuilder
from common import Vec3, Point3


class TestCamera(TestCase):

    def test_camera_builder(self):
        builder = CameraBuilder()
        camera = builder \
            .look_from(Point3(13.0, 2.0, 3.0)) \
            .look_at(Point3(0.0, 0.0, 0.0)) \
            .up_direction(Vec3(0.0, 1.0, 0.0)) \
            .vertical_field_of_view(25.0) \
            .aspect_ratio(1.77) \
            .image_width(2560) \
            .aperture(0.0) \
            .focus_distance(10.0) \
            .open_close_time(0.0, 1.0) \
            .build()
        self.assertIsNotNone(camera)
