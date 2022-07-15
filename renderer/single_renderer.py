import math
from dataclasses import dataclass

import common
from common import Vec3, Point3, ColorRgb, Ray, Camera, CameraBuilder
from hittables import Hittable, HittableList
from hittables.primitives import Sphere
from materials import Lambertian
from textures import SolidColor


@dataclass
class SingleRenderer:
    """
    This is a basic, single process renderer, used for troubleshooting bugs
    """

    def ray_color(self, r: Ray, world: HittableList, depth: int) -> ColorRgb:
        if depth <= 0:
            return ColorRgb()

        rec = world.hit(r, 0.001, float("inf"))
        if rec:
            # emitted = rec.material.emitted(rec.u, rec.v, rec.p)
            # scatter_rec = rec.material.scatter(r, rec.p, rec.normal, rec.t, rec.u, rec.v, rec.front_face)
            # if scatter_rec:
            #     return scatter_rec.attenuation + emitted
            # return emitted
            target = rec.p + Vec3.random_in_hemisphere(rec.normal)
            return 0.5 * self.ray_color(Ray(rec.p, target - rec.p), world, depth - 1)

        unit_dir = r.dir.unit_vector()
        t = 0.5 * (unit_dir.y + 1.0)
        blended = (1.0 - t) * ColorRgb(1.0, 1.0, 1.0) + t * ColorRgb(0.5, 0.7, 1.0)
        return blended

    @staticmethod
    def _multi_sample(pixel_color: ColorRgb, samples_per_pixel: int) -> ColorRgb:
        """
        returns a new pixel color using multi-sample color computation

        :param pixel_color: the color to multisample
        :param samples_per_pixel: higher values tend to darken the final color
        """
        r, g, b = pixel_color.to_tuple()

        # divide the color total by the numer of samples and gamma correct for gamma = 2.0
        scale = 1.0 / float(samples_per_pixel)
        r = math.sqrt(scale * r)
        g = math.sqrt(scale * g)
        b = math.sqrt(scale * b)

        return ColorRgb(
            256.0 * common.clamp(r, 0.0, 0.999),
            256.0 * common.clamp(g, 0.0, 0.999),
            256.0 * common.clamp(b, 0.0, 0.999)
        )

    def simple_scene(self):
        samples_per_pixel = 100
        max_depth = 50
        image_width = 400
        aspect_ratio = 16.0 / 9.0
        # camera
        camera = CameraBuilder()\
            .image_width(400)\
            .look_from(Point3(0.0, 0.0, 0.0))\
            .look_at(Point3(0.0, 0.0, -1.0))\
            .up_direction(Vec3(0.0, 1.0, 0.0))\
            .aspect_ratio(aspect_ratio)\
            .vertical_field_of_view(90.0)\
            .open_close_time(0.0, 1.0)\
            .focus_distance(10.0)\
            .aperture(0.0)\
            .build()

        # world
        world = HittableList()

        tex = SolidColor.from_rgb(1.0, 0.0, 0.0)
        mat = Lambertian(tex)
        sphere1 = Sphere(Point3(0.0, 0.0, -1.0), 0.5, mat)

        tex = SolidColor.from_rgb(1.0, 0.8, 0.0)
        mat = Lambertian(tex)
        sphere2 = Sphere(Point3(0.0, -100.5, -1.0), 100.0, mat)

        world.add(sphere1)
        world.add(sphere2)

        colors = []
        # render
        for j in range(camera.image_height):
            print(f"scanline {j} of {camera.image_height}")

            for i in range(image_width):
                pixel_color = ColorRgb()
                for s in range(samples_per_pixel):
                    u = float(i) / (image_width - 1)
                    v = float(j) / (camera.image_height - 1)
                    r = camera.get_ray(u, v)
                    pixel_color += self.ray_color(r, world, max_depth)
                multi_samp_color = SingleRenderer._multi_sample(pixel_color, samples_per_pixel)
                colors.append(multi_samp_color)

        common.save_as_ppm_image("single0", colors, image_width, camera.image_height)
