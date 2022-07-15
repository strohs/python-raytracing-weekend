import math
from typing import List
from PIL import Image
import numpy as np
import numpy.typing as npt

import common

NDArrayObject = npt.NDArray[object]
NDArrayFloat = npt.NDArray[np.float_]


def clamp(x: float, min: float, max: float) -> float:
    """
    clamps x to the range min..max (inclusive)
    :param x:
    :param min:
    :param max:
    :return:
    """
    if x < min:
        return min
    elif x > max:
        return max
    else:
        return x


def degrees_to_radians(degrees: float) -> float:
    """
    converts degrees to radians
    :param degrees:
    :return:
    """
    return degrees * math.pi / 180.0


def save_as_png_image(filename: str, data: List[common.ColorRgb], width: int, height: int):
    """
    saves a List of ColorRgb objects as a PNG image
    :param filename: the file name to save the image under
    :param data: color data of the image, in row-order, from top left to bottom right
    :param width: the width of the saved image
    :param height: the height of the saved image
    :return:
    """

    # convert ColorRgb data to a sequence of ints
    # then call bytes() to turn that sequence into an immutable sequence of bytes...
    # because this is what the PIL.Image.frombytes() method expects

    byte_list = []
    for color in data:
        byte_list.append(int(color.r))
        byte_list.append(int(color.g))
        byte_list.append(int(color.b))

    byte_arr = bytes(byte_list)
    size = (width, height)
    try:
        image = Image.frombytes("RGB", size, byte_arr)
        image.save(filename, "PNG")
    except ValueError as err:
        print(f"ValueError during image save with {filename}  {err=}")
    except OSError as err:
        print(f"OS Error during image save of file {filename}  {err=}")


def save_as_ppm_image(filename: str, data: NDArrayFloat):
    """
    saves the color data as a PPM image file
    :param filename:
    :param data: a height x width x 3 NDArray containing the RGB data for each pixel. The array must already be
    normalized to values between 0.0 and 255.0 (exclusive)
    """
    filename = filename + ".ppm"
    height, width, color_dim = data.shape
    bytes_arr = data.astype(np.ubyte)
    with open(filename, "wb") as f:
        # write the PPM header
        f.write(b"P3\n")
        f.write(bytes(f"{width} {height}\n", "utf-8"))
        f.write(b"255\n")

        # write color data in reverse row order, it's required by the PPM image format
        for row in np.flip(bytes_arr, axis=0):
            for color in row:
                red, green, blue = color
                line = bytes(f"{red} {green} {blue}\n", "utf-8")
                f.write(bytes(line))
