from enum import Enum


class Scene(Enum):
    """
    Enumeration of the pre-built scenes from the first two books of "Raytracing in a Weekend"
    """
    RANDOM_SPHERES = 1
    PERLIN_SPHERES = 2
    EARTH = 3
    CORNELL_BOX = 4
    CORNELL_SMOKE_BOXES = 5
    FINAL = 6

    @staticmethod
    def get_scene_name(number: int):
        match number:
            case Scene.RANDOM_SPHERES.value:
                return Scene.RANDOM_SPHERES.name
            case Scene.PERLIN_SPHERES.value:
                return Scene.PERLIN_SPHERES.name
            case Scene.EARTH.value:
                return Scene.EARTH.name
            case Scene.CORNELL_BOX.value:
                return Scene.CORNELL_BOX.name
            case Scene.CORNELL_SMOKE_BOXES.value:
                return Scene.CORNELL_BOX.name
            case Scene.FINAL.value:
                return Scene.FINAL.name
            case n:
                raise RuntimeError(f"unknown Scene number {n}")

