from dataclasses import dataclass
from typing import List, Optional

from common import Ray
from hittables import Aabb, Hittable, HitRecord


@dataclass
class HittableList(Hittable):
    """
    A list of all Hittable objects in the ray tracer's "world" or scene
    """

    def __init__(self):
        self.objects: List[Hittable] = list()

    def clear(self):
        """
        clears this list of hittable objects
        """
        self.objects.clear()

    def add(self, hittable: Hittable):
        """
        appends the given hittable to this list of Hittables
        :param hittable:
        """
        self.objects.append(hittable)

    def hit(self, r: Ray, t_min: float, t_max: float) -> Optional[HitRecord]:
        # iterate through the list of hittables to determine if a `Ray` has hit some
        # object in this list. If an object was hit, a HitRecord is returned
        # containing details of the **closest hit**. If nothing was hit by the ray,
        # `None` is returned
        closest_so_far = t_max
        hit_anything: Optional[HitRecord] = None

        for hittable in self.objects:
            hit_record = hittable.hit(r, t_min, closest_so_far)
            if hit_record:
                closest_so_far = hit_record.t
                hit_anything = hit_record

        return hit_anything

    def bounding_box(self, t0: float, t1: float) -> Optional[Aabb]:
        # return a single Axis aligned bounding box that surrounds all hittables that were hit by a Ray
        if len(self.objects) == 0:
            return None

        # compute a surrounding AABB for all hittables that return an AABB in self.objects
        output_box = None
        # get a list of all Aabb's for each hittable that returns an Aabb
        aabbs = list(filter(lambda abb: abb, map(lambda hittable: hittable.bounding_box(t0, t1), self.objects)))
        if len(aabbs) > 0:
            output_box = Aabb()
            for bb in aabbs:
                output_box = Aabb.surrounding_box(output_box, bb)

        return output_box
