import math
import random
import time
import concurrent.futures
from dataclasses import dataclass
from typing import List
import numpy as np

import common
from common import Camera, ColorRgb, Ray
from hittables import HittableList, Hittable
from hittables.bvh_node import BvhNode
from renderer import background_type

# RenderResult holds the result of rendering a single row: (row_start, ndarray[[ColorRgb], [ColorRgb], ...])
RenderResult = (int, common.NDArrayFloat)


@dataclass
class MultiprocessRenderer:
    """
    A raytracer that uses python's concurrent.futures.ProcessPoolExecutor to render rows of the image
    on different threads.

     background_color - the BackgroundType to use for the scene's background color(s)
     ray_bounce_depth - the maximum number of bounces that a single Ray can have. This default's to 50.
     Higher values can lead to better looking images, but also increase render times
     samples_per_pixel - the number of samples to take for each pixel rendered. This helps to anti-alias the
     image and produces less "spotty" images. 50 is the default, which will definitely produce a "spotty" image.
     Increasing this to 500 or even 1000 will make a "smoother" image but will **drastically** increase render times,
     especially when using Python
    """
    background_color: background_type.BackgroundType
    ray_bounce_depth: int
    samples_per_pixel: int
    cpu_cores: int

    def render(self, camera: Camera, world: HittableList) -> common.NDArrayFloat:
        """Renders a raytraced image, using the provided `Camera` and `World`.
.
        Returns a ndarray with shape: (height, width, 3), containing the R,G,B color values of each pixel in the image.
        :param camera:the camera object to use for rendering
        :param world: a list of Hittables to render
        """
        start = time.time()

        # build a bvh
        world_bvh = BvhNode.from_hittable_list(world, 0.0, 1.0)

        with concurrent.futures.ProcessPoolExecutor(max_workers=self.cpu_cores) as executor:
            # futures will hold completed render jobs
            futures = []

            # stores the final R,G,B color data of each pixel in a height x width x 3 ndarray
            colors = np.empty((camera.image_height, camera.image_width, 3), dtype=np.float_)

            # iterate over row indices and submit a row to the executor
            for row_idx in range(camera.image_height):
                futures.append(
                    executor.submit(self.render_scanline, row_idx, world_bvh, camera)
                )

            print(f"submitted {camera.image_height:04d} rows to the process pool for rendering...")

            for fut in concurrent.futures.as_completed(futures):
                row_start, row_colors = fut.result()
                colors[row_start] = row_colors
                print(f"row {row_start:04d} of {camera.image_height-1:04d} finished...")

        elapsed_secs = (time.time() - start)
        print("done rendering, total elapsed {0:8.3f}secs".format(elapsed_secs))
        return colors

    def render_scanline(self, row: int, world: HittableList, camera: Camera) -> RenderResult:
        """
        Renders one row (a.k.a. scanline) of pixels

        :param row: the index of the row being rendered, 0-based
        :param world: list of all the Hittables in the world
        :param camera: the camera object
        :return: a list of ColorRgb representing the final pixel colors for the row
        """
        # holds the row of RGB data
        colors: common.NDArrayFloat = np.zeros((camera.image_width, 3))

        # for each pixel in the current row, generate multiple rays from the camera to the current
        # pixel, offset by some u,v amount, and compute the final pixel color via calls to the ray_color()
        # method. The final pixel_color is multi-sampled before being stored in the final colors list
        for col in range(camera.image_width):
            pixel_color = ColorRgb()
            for _ in range(self.samples_per_pixel):
                # u,v are offsets that randomly choose a point close to the current pixel
                u = (float(col) + random.random()) / (camera.image_width - 1)
                v = (float(row) + random.random()) / (camera.image_height - 1)
                r = camera.get_ray(u, v)
                pixel_color += self.ray_color(r, world, self.ray_bounce_depth)
            r, g, b = MultiprocessRenderer._multi_sample(pixel_color, self.samples_per_pixel).to_tuple()
            colors[col][0] = r
            colors[col][1] = g
            colors[col][2] = b
        return row, colors

    def ray_color(self, ray: Ray, world: Hittable, depth: int) -> ColorRgb:
        """
        determines if a Ray has hit a `Hittable` object in the `world` and computes the overall pixel color
        of the given Ray. The Hittable's `Material` is taken into account when performing ray bouncing
        (up to `depth` times) in order to get an accurate color determination. If nothing
        was hit then the `background` color is returned

        :param ray: the Ray to color
        :param world: HittableList of objects in the world
        :param depth: max number of times the ray can bounce off of hittables before we stop coloring
        :return: the final color of the given Ray
        """
        if depth == 0:
            # exceeded the ray bounce limit, no more light is gathered
            return ColorRgb()

        # if a hittable was hit, determine if its material will scatter the incoming ray,
        # AND how much light the material emits
        rec = world.hit(ray, 0.001, float("inf"))
        if rec:
            emitted = rec.material.emitted(rec.u, rec.v, rec.p)
            scatter_rec = rec.material.scatter(ray, rec.p, rec.normal, rec.t, rec.u, rec.v, rec.front_face)
            if scatter_rec:
                return emitted + scatter_rec.attenuation ** self.ray_color(scatter_rec.scattered, world, depth - 1)
            else:
                return emitted
        else:
            # nothing was hit, return the background color
            if isinstance(self.background_color, background_type.SolidBackground):
                return self.background_color.color1
            else:
                # linear interpolate background color
                return MultiprocessRenderer._linear_blend(ray, self.background_color.frm, self.background_color.to)

    @staticmethod
    def _linear_blend(ray: Ray, frm: ColorRgb, to: ColorRgb) -> ColorRgb:
        """
        return a linear blended color between frm and to.

        The input ray's y coordinate is used to determine how much of 'frm' and 'to'
        to apply
        """
        unit_direction = ray.dir.unit_vector()
        t = 0.5 * (unit_direction.y + 1.0)
        return (1.0 - t) * frm + t * to

    @staticmethod
    def _multi_sample(pixel_color: ColorRgb, samples_per_pixel: int) -> ColorRgb:
        """
        returns a new pixel color using multi-sample color computation

        :param pixel_color: the color to multisample
        :param samples_per_pixel:
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

    @staticmethod
    def _index_chunks(max_index: int, size: int) -> List:
        """
        returns a list of indices pairs: (start_index, stop_index), that evenly divide the
        range from 0 to max_index into groups between 0 and max_index
        """
        if max_index <= 0 or size <= 0:
            return []
        index_chunks = []
        stride = max_index // size + max_index % size
        for i in range(0, max_index, stride):
            index_chunks.append((i, min(i+stride, max_index)))
        return index_chunks
