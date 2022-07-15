from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from common import Ray
from hittables import HitRecord, Aabb


@dataclass
class Hittable(ABC):
    """
    A Base class for primitives that can be "hit" by a Ray
    """

    @abstractmethod
    def hit(self, r: Ray, t_min: float, t_max: float) -> Optional[HitRecord]:
        """
        tests if the Ray 'r' has hit this Hittable.
        `t_min` and `t_max` are used to constrain the bounds of the "hit" so that it occurs
        between t_min and t_max

        :param r: the Ray to test
        :param t_min: minimum constraint for the ray parameter
        :param t_max: maximum constraint for the ray parameter
        :return: a HitRecord if the given Ray has hit this hittable else None
        """
        pass

    @abstractmethod
    def bounding_box(self, t0: float, t1: float) -> Optional[Aabb]:
        """
        computes and returns the axis-aligned bounding box (Aabb) of this hittable

        :param t0: time interval begin
        :param t1: time interval end
        :return:
        """
        pass

