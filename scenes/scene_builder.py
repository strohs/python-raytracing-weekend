"""
Functions for generating a camera and a list of hittable primitives that make up one of the
pre-built scenes from the Raytracing in a Weekend series of books.
"""
import random

from common import Camera, CameraBuilder, Point3, Vec3, ColorRgb
from hittables import HittableList, FlipFace, RotateY, Hittable
from hittables.bvh_node import BvhNode
from hittables.primitives import Sphere, XZRect, YZRect, XYRect, BoxInst, MovingSphere
from hittables.translate import Translate
from hittables.volumes import ConstantMedium
from materials import Lambertian, Dielectric, Metal
from materials.diffues_light import DiffuseLight
from renderer import BackgroundType, LinearInterpBackground, SolidBackground
from textures import SolidColor, ImageTexture, NoiseTexture
from textures.checker_texture import CheckerTexture

# path to the earth texture file
EARTH_TEXTURE_PATH = "./earthmap.jpg"


def build_scene_cornell_box_with_two_boxes(image_width: float, aspect_ratio: float) -> (Camera, HittableList, BackgroundType):
    """
    builds the standard cornell box scene

    :param image_width:
    :param aspect_ratio:
    :return:
    """
    # build the camera
    camera = CameraBuilder()\
        .look_from(Point3(278.0, 278.0, -800.0))\
        .look_at(Point3(278.0, 278.0, 0.0))\
        .up_direction(Vec3(0.0, 1.0, 0.0))\
        .focus_distance(10.0)\
        .aspect_ratio(aspect_ratio) \
        .image_width(image_width) \
        .aperture(0.0) \
        .vertical_field_of_view(40.0) \
        .open_close_time(0.0, 1.0) \
        .build()

    # build solid color materials
    red = SolidColor.from_rgb(0.65, 0.05, 0.05)
    white = SolidColor.from_rgb(0.73, 0.73, 0.73)
    green = SolidColor.from_rgb(0.12, 0.45, 0.15)
    red_mat = Lambertian(red)
    white_mat = Lambertian(white)
    green_mat = Lambertian(green)

    # build the walls of the room
    green_wall = FlipFace(YZRect(0.0, 555.0, 0.0, 555.0, 555.0, green_mat))
    red_wall = YZRect(0.0, 555.0, 0.0, 555.0, 0.0, red_mat)
    floor = FlipFace(XZRect(0.0, 555.0, 0.0, 555.0, 555.0, white_mat))
    ceiling = XZRect(0.0, 555.0, 0.0, 555.0, 0.0, white_mat)
    back_wall = FlipFace(XYRect(0.0, 555.0, 0.0, 555.0, 555.0, white_mat))

    # build the rectangular light at the top
    light = build_xz_diff_light(ColorRgb(16.0, 16.0, 16.0), 183.0, 373.0, 137.0, 302.0, 554.0)

    # build a white rectangular box
    rect_box1 = BoxInst.from_material(Point3(0.0, 0.0, 0.0), Point3(165.0, 330.0, 165.0), white_mat)
    rect_box2 = RotateY.from_hittable(rect_box1, 15.0)
    rect_box = Translate(rect_box2, Vec3(265.0, 0.0, 295.0))

    # build a square box
    square_box1 = BoxInst.from_material(Point3(0.0, 0.0, 0.0), Point3(165.0, 165.0, 165.0), white_mat)
    square_box2 = RotateY.from_hittable(square_box1, -18.0)
    square_box = Translate(square_box2, Vec3(130.0, 0.0, 100.0))

    # build a perlin sphere on top of the square box
    # per_sphere = build_perlin_sphere(Point3(0.0, 0.0, 0.0),60.0, 0.2)
    # per_sphere = Translate(per_sphere, Vec3(175.0, 225.0, 170.0))

    world = HittableList()
    world.add(green_wall)
    world.add(red_wall)
    world.add(light)
    world.add(floor)
    world.add(ceiling)
    world.add(back_wall)
    world.add(rect_box)
    world.add(square_box)

    # black background
    background = SolidBackground(ColorRgb())

    return camera, world, background


def build_scene_cornell_smoke_boxes(image_width: float, aspect_ratio: float) -> (Camera, HittableList, BackgroundType):
    """
    builds a cornell box scene except the two interior boxes are made out of a smoke-like material

    :param image_width:
    :param aspect_ratio:
    :return:
    """
    # build the camera
    camera = CameraBuilder() \
        .look_from(Point3(278.0, 278.0, -800.0)) \
        .look_at(Point3(278.0, 278.0, 0.0)) \
        .up_direction(Vec3(0.0, 1.0, 0.0)) \
        .focus_distance(10.0) \
        .aspect_ratio(aspect_ratio) \
        .image_width(image_width) \
        .aperture(0.0) \
        .vertical_field_of_view(40.0) \
        .open_close_time(0.0, 1.0) \
        .build()

    # build solid color materials
    red = SolidColor.from_rgb(0.65, 0.05, 0.05)
    white = SolidColor.from_rgb(0.73, 0.73, 0.73)
    green = SolidColor.from_rgb(0.12, 0.45, 0.15)
    red_mat = Lambertian(red)
    white_mat = Lambertian(white)
    green_mat = Lambertian(green)

    # build the walls of the room
    green_wall = FlipFace(YZRect(0.0, 555.0, 0.0, 555.0, 555.0, green_mat))
    red_wall = YZRect(0.0, 555.0, 0.0, 555.0, 0.0, red_mat)
    floor = FlipFace(XZRect(0.0, 555.0, 0.0, 555.0, 555.0, white_mat))
    ceiling = XZRect(0.0, 555.0, 0.0, 555.0, 0.0, white_mat)
    back_wall = FlipFace(XYRect(0.0, 555.0, 0.0, 555.0, 555.0, white_mat))

    # build the rectangular light at the top
    light = build_xz_diff_light(ColorRgb(7.0, 7.0, 7.0), 183.0, 373.0, 137.0, 302.0, 554.0)

    # build a white rectangular box
    rect_box1 = BoxInst.from_material(Point3(0.0, 0.0, 0.0), Point3(165.0, 330.0, 165.0), white_mat)
    rect_box2 = RotateY.from_hittable(rect_box1, 15.0)
    rect_box = Translate(rect_box2, Vec3(265.0, 0.0, 295.0))

    # build a square box
    square_box1 = BoxInst.from_material(Point3(0.0, 0.0, 0.0), Point3(165.0, 165.0, 165.0), white_mat)
    square_box2 = RotateY.from_hittable(square_box1, -18.0)
    square_box = Translate(square_box2, Vec3(130.0, 0.0, 100.0))

    # fog box has a black color applied to its fog
    fog_box = ConstantMedium.from_density(rect_box, 0.01, SolidColor.from_rgb(0.0, 0.0, 0.0))
    # smoke box has white color applied for its smoke
    smoke_box = ConstantMedium.from_density(square_box, 0.01, SolidColor.from_rgb(1.0, 1.0, 1.0))

    world = HittableList()
    world.add(green_wall)
    world.add(red_wall)
    world.add(light)
    world.add(floor)
    world.add(ceiling)
    world.add(back_wall)
    world.add(smoke_box)
    world.add(fog_box)

    # black background
    background = SolidBackground(ColorRgb())

    return camera, world, background


def build_scene_two_perlin_spheres(image_width: int, aspect_ratio: float) -> (Camera, HittableList, BackgroundType):
    """
    builds a scene with two "marble" textured sphere on top of each other, and a linear blended blue background
    """
    camera = CameraBuilder() \
        .look_from(Point3(13.0, 2.0, 3.0)) \
        .look_at(Point3(0.0, 0.0, 0.0)) \
        .up_direction(Vec3(0.0, 1.0, 0.0)) \
        .aspect_ratio(aspect_ratio) \
        .image_width(image_width) \
        .focus_distance(10.0) \
        .aperture(0.0) \
        .vertical_field_of_view(40.0) \
        .open_close_time(0.0, 1.0) \
        .build()

    background = LinearInterpBackground(ColorRgb(1.0, 1.0, 1.0), ColorRgb(0.5, 0.5, 1.0))
    sphere1 = build_perlin_sphere(Point3(0.0, -1000.0, 0.0), 1000.0, 0.8)
    sphere2 = build_perlin_sphere(Point3(0.0, 2.0, 0.0), 2.0, 0.5)

    world = HittableList()
    world.add(sphere1)
    world.add(sphere2)

    return camera, world, background


def build_scene_two_checkered_spheres(image_width: int, aspect_ratio: float) -> (Camera, HittableList, BackgroundType):
    look_from_point = Point3(13.0, 2.0, 3.0)
    look_at_point = Point3(0.0, 0.0, 0.0)
    up_dir = Vec3(0.0, 1.0, 0.0)
    focus_distance = 10.0
    aperture = 0.0
    vertical_fov = 30.0
    open_time = 0.0
    close_time = 1.0

    camera = CameraBuilder()\
        .look_from(look_from_point)\
        .look_at(look_at_point)\
        .up_direction(up_dir)\
        .aspect_ratio(aspect_ratio)\
        .image_width(image_width)\
        .focus_distance(focus_distance)\
        .aperture(aperture)\
        .vertical_field_of_view(vertical_fov)\
        .open_close_time(open_time, close_time)\
        .build()

    # build two checkered spheres
    sphere1 = build_checkered_sphere(
        Point3(0.0, -10.0, 0.0),
        10.0,
        ColorRgb(0.2, 0.3, 0.1),
        ColorRgb(0.9, 0.9, 0.9)
    )
    sphere2 = build_checkered_sphere(
        Point3(0.0, 10.0, 0.0),
        10.0,
        ColorRgb(0.2, 0.2, 0.2),
        ColorRgb(0.8, 0.8, 0.8)
    )

    world = HittableList()
    world.add(sphere1)
    world.add(sphere2)

    background = LinearInterpBackground(ColorRgb(1.0, 1.0, 1.0), ColorRgb(0.5, 0.5, 1.0))

    return camera, world, background


def build_scene_random_spheres(image_width: int, aspect_ratio: float) -> (Camera, HittableList, BackgroundType):
    camera = CameraBuilder() \
        .look_from(Point3(13.0, 2.0, 3.0)) \
        .look_at(Point3(0.0, 0.0, 0.0)) \
        .up_direction(Vec3(0.0, 1.0, 0.0)) \
        .aspect_ratio(aspect_ratio) \
        .image_width(image_width) \
        .focus_distance(10.0) \
        .aperture(0.0) \
        .vertical_field_of_view(30.0) \
        .open_close_time(0.0, 1.0) \
        .build()

    # the radius for all spheres in this scene
    default_radius = 0.2

    world = HittableList()

    # blue at the top, interpolating to white at the bottom
    background_color = LinearInterpBackground(ColorRgb(1.0, 1.0, 1.0), ColorRgb(0.5, 0.5, 1.0))

    # the ground is a giant checkered sphere
    ground_sphere = build_checkered_sphere(
        Point3(0.0, -1000.0, 0.0),
        1000.0,
        ColorRgb(0.1, 0.2, 0.1),
        ColorRgb(0.8, 0.8, 0.8)
    )

    world.add(ground_sphere)

    # generate 484, equal sized spheres, with random materials and colors
    for a in range(-11, 11):
        for b in range(-11, 11):
            # generate a random center point for the sphere, right above the y-plane
            x = a + 0.9 * random.random()
            z = b + 0.9 * random.random()
            center = Point3(x, 0.2, z)

            if (center - Vec3(4.0, 0.2, 0.0)).length() > 0.9:
                # randomly select a material
                prob = random.random()
                if prob < 0.1:
                    # create a moving sphere
                    center2 = center + Vec3(0.0, random.random(), 0.0)
                    random_color = ColorRgb.random() ** ColorRgb.random()
                    moving_sphere = build_solid_moving_sphere(random_color, center, center2, 0.0, 1.0, default_radius)
                    world.add(moving_sphere)
                elif prob < 0.7:
                    # create a solid, random color sphere, offset from the center
                    random_color = ColorRgb.random() ** ColorRgb.random()
                    center_offset = center + Vec3(0.0, random.random(), 0.0)
                    sphere = build_solid_sphere(center_offset, default_radius, random_color)
                    world.add(sphere)
                elif prob < 0.95:
                    # build a metal sphere
                    random_color = ColorRgb.random_range(0.5, 1.0)
                    fuzz = random.uniform(0.0, 0.5)
                    sphere = build_metal_sphere(center, default_radius, random_color, fuzz)
                    world.add(sphere)
                else:
                    # build a dielectric sphere
                    sphere = build_dielectric_sphere(center, default_radius, 1.5)
                    world.add(sphere)

    # add a single large glass sphere
    glass_sphere = build_dielectric_sphere(Point3(0.0, 1.0, 0.0), 1.0, 1.5)
    world.add(glass_sphere)

    # add a single perlin noise sphere
    perlin_sphere = build_perlin_sphere(Point3(-4.0, 1.0, 0.0), 1.0, 0.9)
    world.add(perlin_sphere)

    # add a tan colored sphere
    metal_sphere = build_metal_sphere(Point3(4.0, 1.0, 0.0), 1.0, ColorRgb(0.7, 0.6, 0.5), 0.0)
    world.add(metal_sphere)

    return camera, world, background_color


def build_earth_scene(image_width: int, aspect_ratio: float) -> (Camera, HittableList, BackgroundType):
    """
    returns a scene consisting of the camera looking at a single earth textured sphere, against a blue
    background
    :param image_width:
    :param aspect_ratio:
    :return:
    """
    camera = CameraBuilder() \
        .look_from(Point3(13.0, 2.0, 3.0)) \
        .look_at(Point3(0.0, 0.0, 0.0)) \
        .up_direction(Vec3(0.0, 1.0, 0.0)) \
        .aspect_ratio(aspect_ratio) \
        .image_width(image_width) \
        .focus_distance(10.0) \
        .aperture(0.0) \
        .vertical_field_of_view(30.0) \
        .open_close_time(0.0, 1.0) \
        .build()
    earth = build_earth_sphere(Vec3(0.0, 0.0, 0.0), 2.0)

    world = HittableList()
    world.add(earth)

    # blue at the top, interpolating to white at the bottom
    background_color = LinearInterpBackground(ColorRgb(1.0, 1.0, 1.0), ColorRgb(0.5, 0.5, 1.0))
    return camera, world, background_color


def build_scene_final(image_width: int, aspect_ratio: int) -> (Camera, HittableList, BackgroundType):
    """
    builds the "final" scene of the book "Raytracing the Next Week"
    This scene is a ground plane made of 400 green boxes, along with a glass sphere, earth texture sphere,
    perlin noise sphere, metal sphere, a foggy sphere, and then a large box made up of 1000 smaller spheres.
    There is a mist sphere applied to the entire scene
    """
    camera = CameraBuilder() \
        .look_from(Point3(178.0, 278.0, -800.0)) \
        .look_at(Point3(278.0, 278.0, 0.0)) \
        .up_direction(Vec3(0.0, 1.0, 0.0)) \
        .aspect_ratio(aspect_ratio) \
        .image_width(image_width) \
        .focus_distance(10.0) \
        .aperture(0.0) \
        .vertical_field_of_view(40.0) \
        .open_close_time(0.0, 1.0) \
        .build()

    # background is black for this scene
    background = SolidBackground(ColorRgb(0.0, 0.0, 0.0))

    # build a ground layer consisting of ~ 400 boxes of various widths and heights
    ground_boxes = HittableList()
    ground_mat = Lambertian.from_color(0.48, 0.83, 0.53)
    boxes_per_side = 20
    for i in range(boxes_per_side):
        for j in range(boxes_per_side):
            w = 100.0
            x0 = -1000.0 + i * w
            z0 = -1000.0 + j * w
            y0 = 0.0
            x1 = x0 + w
            y1 = random.uniform(1.0, 101.0)
            z1 = z0 + w
            box = BoxInst.from_material(Point3(x0, y0, z0), Point3(x1, y1, z1), ground_mat)
            ground_boxes.add(box)

    # objects holds all the hittable objects in the scene
    objects = HittableList()
    objects.add(BvhNode.from_hittable_list(ground_boxes, 0.0, 1.0))

    # build a light source at the top of the scene
    light = build_xz_diff_light(ColorRgb(7.0, 7.0, 7.0), 123.0, 423.0, 147.0, 412.0, 554.0)
    objects.add(light)

    # build a moving sphere
    center_start = Point3(400.0, 400.0, 200.0)
    mov_sphere = build_solid_moving_sphere(
        ColorRgb(0.7, 0.3, 0.1),
        center_start,
        center_start + Vec3(30.0, 0., 0.),
        0.0,
        1.0,
        50.0
    )
    objects.add(mov_sphere)

    # build a glass sphere
    glass_sphere = build_dielectric_sphere(Point3(260., 150., 45.), 50., 1.5)
    objects.add(glass_sphere)

    # build a metal sphere
    metal_sphere = build_metal_sphere(Point3(0., 150., 145.), 50., ColorRgb(0.8, 0.8, 0.9), 10.0)
    objects.add(metal_sphere)

    # build a blueish, glass sphere, make it foggy
    sphere_boundary = build_dielectric_sphere(Point3(360., 150., 145.), 70., 1.5)
    objects.add(sphere_boundary)
    fog_volume = build_constant_medium(sphere_boundary, 0.2, ColorRgb(0.2, 0.4, 0.9))
    objects.add(fog_volume)

    # build a spherical mist volume throughout the whole scene
    sphere_mist_boundary = build_dielectric_sphere(Point3(), 5000., 1.5)
    mist_volume = build_constant_medium(sphere_mist_boundary, 0.0001, ColorRgb(1., 1., 1.))
    objects.add(mist_volume)

    # build a sphere with the earth texture mapped to it
    earth = build_earth_sphere(Point3(400., 200., 400.), 100.)
    objects.add(earth)

    # build a sphere with perlin noise texture
    perlin_sphere = build_perlin_sphere(Point3(220., 280., 300.), 80., 0.1)
    objects.add(perlin_sphere)

    # build a box composed of ~1000 smaller spheres
    ns = 1000
    box_of_spheres = HittableList()
    for _ in range(ns):
        sphere = build_solid_sphere(Point3.random_range(0.0, 165.0), 10.0, ColorRgb(0.73, 0.73, 0.73))
        box_of_spheres.add(sphere)

    # add the box of spheres to the BVH and then rotate and translate the entire box
    sphere_node = BvhNode.from_hittable_list(box_of_spheres, 0.0, 1.0)
    rotated_spheres = RotateY.from_hittable(sphere_node, 15.0)
    translated_spheres = Translate(rotated_spheres, Vec3(-100., 270., 395.))
    objects.add(translated_spheres)

    return camera, objects, background


def build_solid_sphere(center: Point3, radius: float, color: ColorRgb) -> Sphere:
    """
    returns a lambertian sphere of the specified color
    """
    tex = SolidColor(color)
    mat = Lambertian(tex)
    return Sphere(center, radius, mat)


def build_solid_moving_sphere(color: ColorRgb, c0: Point3, c1: Point3, t0: float, t1: float, radius: float) -> MovingSphere:
    """
    builds a Solid moving sphere of the specified color
    :param color:
    :param c0: sphere's center at start
    :param c1: sphere's center at end
    :param t0: start time
    :param t1: end time
    :param radius:
    :return:
    """
    mat = Lambertian.from_color(color.r, color.g, color.b)
    return MovingSphere(c0, c1, t0, t1, radius, mat)


def build_dielectric_sphere(center: Point3, radius: float, ref_idx: float) -> Sphere:
    """
    builds a dielectric sphere with the specified refractive index
    """
    return Sphere(center, radius, Dielectric(ref_idx))


def build_metal_sphere(center: Point3, radius: float, color: ColorRgb, fuzz: float) -> Sphere:
    """
    builds a metal sphere with the specified color and fuzziness
    """
    metal = Metal(color, fuzz)
    return Sphere(center, radius, metal)


def build_checkered_sphere(center: Point3, radius: float, even: ColorRgb, odd: ColorRgb) -> Sphere:
    """
    Returns a Checkered sphere using the colors in even and odd as the checkerboard colors
    """
    even = SolidColor(even)
    odd = SolidColor(odd)
    tex = CheckerTexture(odd, even)
    mat = Lambertian(tex)
    return Sphere(center, radius, mat)


def build_constant_medium(bound: Hittable, density: float, color: ColorRgb) -> ConstantMedium:
    """
    builds a ConstantMedium from the specified bound, density and color
    """
    return ConstantMedium.from_density(bound, density, SolidColor(color))


def build_earth_sphere(center: Point3, radius: float) -> Sphere:
    """
    builds a sphere with an image of the earth applied to it as its texture
    """
    tex = ImageTexture(EARTH_TEXTURE_PATH)
    mat = Lambertian(tex)
    return Sphere(center, radius, mat)


def build_perlin_sphere(center: Point3, radius: float, noise_scale: float) -> Sphere:
    """
    builds a solid sphere with a Perlin noise as its texture
    :param noise_scale: the amount of noise to generate in the texture. Higher = more noise
    """
    tex = NoiseTexture(noise_scale)
    mat = Lambertian(tex)
    return Sphere(center, radius, mat)


def build_xz_diff_light(light_color: ColorRgb, x0: float, x1: float, z0: float, z1: float, k: float) -> XZRect:
    """
    Returns a XZ-Rectangle diffuse light material with the specified light_color and coordinates
    """
    light_color = SolidColor(light_color)
    diff_light = DiffuseLight(light_color)
    return XZRect(x0, x1, z0, z1, k, diff_light)


def build_xy_diff_light(light_color: ColorRgb, x0: float, x1: float, y0: float, y1: float, k: float) -> XYRect:
    solid_light = SolidColor(light_color)
    diff_light = DiffuseLight(solid_light)
    return XYRect(x0, x1, y0, y1, k, diff_light)
