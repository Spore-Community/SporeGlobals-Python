#!/usr/bin/env python3

'''Provides Spore bounding boxes (bboxes).'''

from __future__ import annotations




from typing import Self, overload
from .matrix import Matrix3
from .transform import Transform
from .vector import Vector3




class BoundingBox:
    '''A class that represents Spore bounding box, a pair of two Vector3 points (X, Y) that define
    the boundaries of an object (the minimum and maximum points).

    Attributes:
        lower (Vector3): The lower point of the bounding box.
        upper (Vector3): The upper point of the bounding box.
        center (Vector3): The center point of the bounding box.
    '''
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, lower: Vector3, upper: Vector3) -> None: ...
    def __init__(self,
                 lower: Vector3 | None = None,
                 upper: Vector3 | None = None) -> None:
        if lower is None and upper is None:
            self.lower = Vector3(-1.0, -1.0, -1.0)
            self.upper = Vector3(1.0, 1.0, 1.0)
        else:
            self.lower = lower
            self.upper = upper

    @property
    def lower(self) -> Vector3:
        '''The lower point of the bounding box.'''
        return self._lower
    @lower.setter
    def lower(self, lower: Vector3 | None) -> None:
        self._lower: Vector3 = lower if isinstance(lower, Vector3) else Vector3()

    @property
    def upper(self) -> Vector3:
        '''The upper point of the bounding box.'''
        return self._upper
    @upper.setter
    def upper(self, upper: Vector3 | None) -> None:
        self._upper: Vector3 = upper if isinstance(upper, Vector3) else Vector3()

    @property
    def center(self) -> Vector3:
        '''The center point of the bounding box.'''
        return (self.lower+self.upper) / 2.0

    def apply_transform(self, transform: Transform) -> Self:
        '''Recalculates this bounding box to apply a transform.

        Arguments:
            transform (Transform): The transform to apply.
        
        Returns:
            out (Self).
        '''
        # pylint: disable=protected-access
        if not transform._flags & Transform.TransformFlags.ROTATION:
            self.lower *= transform.scale
            self.lower += transform.offset
            self.upper *= transform.scale
            self.upper += transform.offset
            return self
        r: Matrix3 = transform.rotation.transposed()
        r_abs: Matrix3 = Matrix3()
        r_abs.m = [[abs(v) for v in row] for row in r.m]

        extent: Vector3 = r_abs * ((self.upper-self.lower) * (transform.scale/2.0))
        center: Vector3 = r*(self.center*transform.scale) + transform.offset

        self.lower = center - extent
        self.upper = center + extent
        return self

    def contains(self, point: Vector3) -> bool:
        '''Checks if the point is in the bounding box.
        
        Arguments:
            point (Vector3): The point to check for.
        
        Returns:
            out (bool): True if the point belongs in the bounding box area, False otherwise.
        '''
        return (
            self.lower.x <= point.x <= self.upper.x
            and self.lower.y <= point.y <= self.upper.y
            and self.lower.z <= point.z <= self.upper.z
        )

    def intersect(self, other: BoundingBox, dst: BoundingBox | None = None) -> bool:
        '''Finds the intersection between two bounding boxes.
        Also returns True if the resulting intersection has the volume 0, so for bounding boxes that
        only intersect in one point, line or plane, it will return False.
        
        Arguments:
            other (BoundingBox): The other bounding box to intersect with.
            dst (BoundingBox | None): The optional bounding box to write interssection into.
        
        Returns:
            out (bool): True if both bounding boxes intersect anywhere, False otherwise.
        '''
        if dst is None:
            dst = BoundingBox()
        dst.lower.x = max(self.lower.x, other.lower.x)
        dst.upper.x = min(self.upper.x, other.upper.x)
        if dst.lower.x > dst.upper.x:
            return False

        dst.lower.y = max(self.lower.y, other.lower.y)
        dst.upper.y = min(self.upper.y, other.upper.y)
        if dst.lower.y > dst.upper.y:
            return False

        dst.lower.z = max(self.lower.z, other.lower.z)
        dst.upper.z = min(self.upper.z, other.upper.z)
        return dst.lower.z <= dst.upper.z

    def __str__(self) -> str:
        '''Gets a stringified bounding box.
        
        Returns:
            out (str): The formatted bounding box ((x, y, z) (x, y, z)).'''
        return f'({self.lower} {self.upper})'

    def __eq__(self, other: object) -> bool:
        '''Compares two bounding boxes for equality.
        
        Returns:
            out (bool): True if both bounding boxes are equal, False otherwise.
        '''
        if not isinstance(other, BoundingBox):
            return NotImplemented
        return self.lower == other.lower and self.upper == other.upper
