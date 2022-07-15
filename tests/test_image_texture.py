from unittest import TestCase
from PIL import Image

from textures import ImageTexture


class TestImageTexture(TestCase):

    def test_can_load_earthmap_image(self):
        with Image.open("earthmap.jpg") as image:
            self.assertIsNotNone(image, "could not load earthmap.jpg which is needed for image_texture class")

    def test_get_rgb_value_at_row_100_col_2(self):
        tex = ImageTexture("earthmap.jpg")
        pixel_rgb = tex.data[100][2]
        self.assertEqual(pixel_rgb[0], 1)
        self.assertEqual(pixel_rgb[1], 16)
        self.assertEqual(pixel_rgb[2], 75)

    def test_hit(self):
        tex = ImageTexture("earthmap.jpg")
        color = tex.value(0.91708, 0.02772)
        self.assertIsNotNone(color)
