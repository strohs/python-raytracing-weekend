import argparse
import sys
import os

import scenes

import common
from renderer import MultiprocessRenderer
from scenes import Scene


def parse_args():
    parser = argparse.ArgumentParser(
        description='Generates a raytraced scene from the book "Raytracing in a Weekend"',
        epilog="""The Scene numbers are as follows:
        1 = Random Spheres,
        2 = Two Perlin Spheres,
        3 = Texture mapped earth,
        4 = Cornell Box,
        5 = Cornell Smoke Boxes,
        6 = Final Scene (a bunch of random boxes and spheres in volumetric fog) 
        """
    )
    parser.add_argument('scene_number',
                        type=int,
                        choices=[1, 2, 3, 4, 5, 6],
                        help='the scene number to generate, 1 - 6')
    parser.add_argument('outfile',
                        action='store',
                        nargs='?',
                        help='filename to use for the raytraced image')
    parser.add_argument('-a',
                        action='store',
                        default=1.77,
                        type=float,
                        dest='aspect_ratio',
                        help="the aspect ratio of the generated image, width / height. "
                             "This defaults to 1.77 which is a 16:9 aspect ratio. A 4:3 image is 1.33")
    parser.add_argument('-w',
                        action='store',
                        default=480,
                        type=int,
                        dest='width',
                        help="the width of the generated image, minimum 100"
                             "Image height will be determined automatically based on the aspect ratio")
    parser.add_argument('-c',
                        action='store',
                        default=0,
                        type=int,
                        dest='cores',
                        help="the number of CPU cores to use for rendering. If left unspecified, the raytracer will"
                             "auto-detect your available cores and use half of them for rendering. This is so that it "
                             "doesn't grind your entire system to a halt")
    parser.add_argument('-s',
                        action='store',
                        default=50,
                        type=int,
                        dest='samples_per_pixel',
                        help='the number of samples to take per pixel. Higher values will increase the render time.')

    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parse_args()
    cpu_cores = 0
    if args.width < 100:
        sys.exit(f"width must be >= 100")
    if args.cores <= 0:
        cpu_cores = os.cpu_count() // 2 if os.cpu_count() > 2 else 1

    # build a pre-made scene based on the entered scene number
    match args.scene_number:
        case Scene.RANDOM_SPHERES.value:
            camera, world, background = scenes.build_scene_random_spheres(args.width, args.aspect_ratio)
        case Scene.PERLIN_SPHERES.value:
            camera, world, background = scenes.build_scene_two_perlin_spheres(args.width, args.aspect_ratio)
        case Scene.EARTH.value:
            camera, world, background = scenes.build_earth_scene(args.width, args.aspect_ratio)
        case Scene.CORNELL_BOX.value:
            camera, world, background = scenes.build_scene_cornell_box_with_two_boxes(args.width, args.aspect_ratio)
        case Scene.CORNELL_SMOKE_BOXES.value:
            camera, world, background = scenes.build_scene_cornell_smoke_boxes(args.width, args.aspect_ratio)
        case Scene.FINAL.value:
            camera, world, background = scenes.build_scene_final(args.width, args.aspect_ratio)
        case n:
            sys.exit(f"unknown scene numer: {n}")

    print(f"rendering scene {Scene.get_scene_name(args.scene_number)} at {camera.image_width}x{camera.image_height} "
          f"at {args.samples_per_pixel} samples-per-pixel, using {cpu_cores} cpu cores")

    # build the renderer object with a default bounce-depth of 50
    renderer = MultiprocessRenderer(
        background,
        50,
        args.samples_per_pixel,
        cpu_cores
    )

    colors = renderer.render(camera, world)

    if not args.outfile:
        args.outfile = f"scene_{Scene.get_scene_name(args.scene_number)}_{camera.image_width}x{camera.image_height}"
    common.save_as_ppm_image(args.outfile, colors)
    print(f"final image saved as {args.outfile}")
