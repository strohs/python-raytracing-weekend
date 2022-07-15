from unittest import TestCase

from common import clamp, save_as_png_image, ColorRgb


class Test(TestCase):

    def test_clamp_in_range(self):
        x = 45.34
        min_v = 20.0
        max_v = 60.0
        self.assertEqual(clamp(x, min_v, max_v), 45.34)

    def test_clamp_below_range(self):
        x = 19.9
        min_v = 20.0
        max_v = 60.0
        self.assertEqual(clamp(x, min_v, max_v), 20.0)

    def test_clamp_above_range(self):
        x = 199.83
        min_v = 20.0
        max_v = 60.0
        self.assertEqual(clamp(x, min_v, max_v), 60.0)

    # def test_save_image_as_png(self):
    #     with Image.open("earthmap.jpg") as image:
    #         self.assertIsNotNone(image, "could not load earthmap.jpg which is needed for image_texture class")
    #         data = list(image.getdata())
    #         width, height = image.size
    #         # convert data to ColorRgb
    #         colors = list(map(lambda tup: ColorRgb(tup[0], tup[1], tup[2]), data))
    #         save_as_png_image("test_earthmap.png", colors, width, height)

