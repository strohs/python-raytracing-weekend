from __future__ import annotations

import random
from dataclasses import dataclass
from typing import List, Optional

from common import Ray
from hittables import Hittable, Aabb, HittableList, HitRecord


@dataclass
class BvhNode(Hittable):
    """Bounded Volume Hierarchy (BVH)
    A BVH is `Hittable` but it’s really a container. It's a binary "tree like" structure that can
    respond to the question, “does this ray hit you?”.
    It recursively sorts and subdivides the `Hittable`s in the "world" into smaller and smaller
    groups, based on a Hittable's bounding box. Each "level" of the BVH will contain Hittables
    such that their bounding boxes are contained within their parent bounding box.
    The "leaves" of the BVH contain a single primitive, such as a sphere or cube etc...
    """
    left: Hittable
    right: Hittable
    bbox: Aabb

    @staticmethod
    def from_hittable_list(hit_list: HittableList, time0: float, time1: float) -> BvhNode:
        """
        returns a BvhNode built from the given list of Hittables. The returned
        BvhNode will be the root node of the BVH
        """
        return BvhNode._split_volumes(hit_list.objects, time0, time1)

    @staticmethod
    def _split_volumes(objects: List[Hittable], time0: float, time1: float) -> BvhNode:
        """
        Constructs a BVH from a list of Hittable objects.
        As long as the list of objects in a BvhNode gets divided into two sub-lists, the hit
        function will work. It will work best if the division is done well, so that the two
        children have smaller bounding boxes than their parent’s bounding box, but that is for
        speed not correctness. This function chooses the middle ground, at each node, split
        the list along one axis.
        1. randomly choose an axis
        2. sort the (hittable) primitives
        3. put half in each subtree
        :param objects: list of hittable objects
        :param time0: time start
        :param time1: time end
        :return: the root node of the constructed BVH
        """
        # randomly choose an x,y,z axis for sorting, 0=x, 1=y, 2=z
        axis = random.randint(0, 2)
        node: BvhNode

        if len(objects) == 1:
            # if there is only one element put a reference to it in each subtree and end recursion
            node = BvhNode(objects[0], objects[0], Aabb())
        elif len(objects) == 2:
            # if objects only has two elements, put one in each subtree and end recursion
            # We are generating the bounding box for each hittable and then comparing their
            # "min" field, using either the x,y,or z coordinate as specified by axis
            if objects[0].bounding_box(0.0, 0.0).min[axis] < objects[1].bounding_box(0.0, 0.0).min[axis]:
                node = BvhNode(objects[0], objects[1], Aabb())
            else:
                node = BvhNode(objects[1], objects[0], Aabb())
        else:
            # recursively partition the remaining hittables into BVH nodes using their bounding
            # box axis' to sort them into left and right children
            objects.sort(key=lambda hittable: hittable.bounding_box(0.0, 0.0).min[axis])
            mid = len(objects) // 2
            left = BvhNode._split_volumes(objects[0:mid], time0, time1)
            right = BvhNode._split_volumes(objects[mid:], time0, time1)
            node = BvhNode(left, right, Aabb())

        # construct a bounding box encompassing this node's left and right children
        box_left = node.left.bounding_box(time0, time1)
        box_right = node.right.bounding_box(time0, time1)
        if box_left is None or box_right is None:
            raise RuntimeError("a hittable did not have a bounding box during BVH construction")
        node.bbox = Aabb.surrounding_box(box_left, box_right)
        return node

    def hit(self, r: Ray, t_min: float, t_max: float) -> Optional[HitRecord]:
        """
        Check if the bounding box for a node is hit, and if so, recursively check its children
        to determine which child was hit (if any).
        Returns a `HitRecord` for the deepest node that was hit
        :param r: the Ray to check
        :param t_min: minimum ray parameter for a hit to be valid
        :param t_max: maximum ray parameter for a hit to be valid
        :return:
        """
        # first check if the hittable's bounding box was hit
        if self.bbox.hit(r, t_min, t_max):
            # check if the left and right children are hit. The hittable being checked could be a BvhNode
            # or some other Hittable, like a sphere, box, etc...
            hit_left = self.left.hit(r, t_min, t_max)
            hit_right = self.right.hit(r, t_min, hit_left.t) if hit_left else self.right.hit(r, t_min, t_max)

            if hit_right:
                return hit_right
            elif hit_left:
                return hit_left
            else:
                return None
        else:
            return None

    def bounding_box(self, t0: float, t1: float) -> Optional[Aabb]:
        """
        Returns an Aabb which is the axis-aligned bounding box that encompasses **all** of
        the `Hittables` contained by this `BvhNode`
        :param t0: time interval begin
        :param t1: time interval end
        """
        return self.bbox

