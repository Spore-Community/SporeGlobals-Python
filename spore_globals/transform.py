#!/usr/bin/env python3

'''Provides Spore "Transform" class.'''

from __future__ import annotations




from enum import IntFlag
from typing import Self
from .matrix import Matrix3, Matrix4
from .quaternion import Quaternion
from .vector import Vector3




class Transform:
    '''A class that represents Spore 3D transformations. It stores the same information as a 4x4
    matrix, but is easier to use.

    Attributes:
        offset (Vector3): The offset vector.
        scale (float): The scale value.
        rotation (Matrix3): The rotation matrix.
    '''
    class TransformFlags(IntFlag):
        '''An enum with int flags for Transform flags.'''
        SCALE = 1
        ROTATION = 2
        OFFSET = 4

    def __init__(self):
        self._flags: int = 0
        self._transform_count: int = 0
        self._offset: Vector3 = Vector3()
        self._scale: float = 1.0
        self._rotation: Matrix3 = Matrix3().set_identity()

    @property
    def offset(self) -> Vector3:
        '''The offset vector.'''
        return self._offset
    @offset.setter
    def offset(self, offset_modified: Vector3 | tuple[float, float, float] | None) -> None:
        if offset_modified is None:
            self._offset = Vector3()
            self._flags &= ~Transform.TransformFlags.OFFSET
        else:
            self._offset = (offset_modified
                            if isinstance(offset_modified, Vector3)
                            else Vector3(*offset_modified))
            self._flags |= Transform.TransformFlags.OFFSET

    @property
    def scale(self) -> float:
        '''The scale value.'''
        return self._scale
    @scale.setter
    def scale(self, scale_modified: float | None) -> None:
        if scale_modified is None:
            self._scale = 1.0
            self._flags &= ~Transform.TransformFlags.SCALE
        else:
            self._scale = scale_modified
            self._flags |= Transform.TransformFlags.SCALE

    @property
    def rotation(self) -> Matrix3:
        '''The rotation matrix.'''
        return self._rotation
    @rotation.setter
    def rotation(self, rotation_modified: Matrix3 | Vector3 | Quaternion | None) -> None:
        if isinstance(rotation_modified, Matrix3):
            # matrix
            self._rotation = rotation_modified
        elif isinstance(rotation_modified, Quaternion):
            # quaternion
            self._rotation = rotation_modified.to_matrix()
        elif isinstance(rotation_modified, Vector3):
            # vector
            self._rotation = Matrix3.from_euler(rotation_modified)
        else:
            # none / smth else
            self._rotation = Matrix3().set_identity()
            self._flags &= ~Transform.TransformFlags.ROTATION
            return
        self._flags |= Transform.TransformFlags.ROTATION

    def to_matrix4(self) -> Matrix4:
        '''Gets the 4x4 matrix representing this transform, which can be applied to vectors
        by multiplying.

        Returns:
            out (Matrix4): The result 4x4 matrix.
        '''
        o: Vector3 = self.offset
        s: float = self.scale
        r: Matrix3 = self.rotation
        out: Matrix4 = Matrix4()
        out.m = [[r[i][j] * s for j in range(3)] + [0] for i in range(3)] + [[o.x, o.y, o.z, 1.0]]

    def invert(self) -> Transform:
        '''Inverts this transform to do the opposite transformation.

        Returns:
            out (Transform): Self.
        '''
        self.scale = 1.0 / self.scale
        self.rotation = self.rotation.transposed()
        self.offset = self.rotation * (-self.scale * self.offset)
        return self

    def pre_transform_by(self, other: Transform) -> Self:
        '''Adds another transform to this.

        Arguments:
            other (Transform): Another transform.
        
        Returns:
            out (Self).
        '''
        self_r: list[list[float]] = self.rotation.m
        other_r: list[list[float]] = other.rotation.m
        o: Vector3 = other.offset * self.scale

        self.offset += Vector3(
            o.x*self_r[0][0] + o.y*self_r[1][0] + o.z*self_r[2][0],
            o.x*self_r[0][1] + o.y*self_r[1][1] + o.z*self_r[2][1],
            o.x*self_r[0][2] + o.y*self_r[1][2] + o.z*self_r[2][2],
        )
        self.rotation.m = [
            [sum(other_r[i][k] * self_r[k][j] for k in range(3)) for j in range(3)]
            for i in range(3)
        ]
        self.scale *= other.scale
        self._flags |= other.flags
        self._transform_count += 1
        return self

    #TODO: smfx-like __str__
