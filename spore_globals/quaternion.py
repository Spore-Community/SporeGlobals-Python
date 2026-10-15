#!/usr/bin/env python3

'''Provides Spore-like quaternion structure.'''

from __future__ import annotations




from math import atan2, sqrt, sin, cos, copysign, asin, pi
from typing import overload, TYPE_CHECKING
from .vector import Vector3, Vector4, X_AXIS, Y_AXIS
if TYPE_CHECKING:
    from .matrix import Matrix3




class Quaternion(Vector4):
    '''A class that represents Spore vector of four floating point values (X, Y, Z, W),
    which is used to represent a quaternion rotation, similar to a Vector4.
    You can use the Quaternion.from_rotation() and Quaternion.from_euler() to build
    quaternion rotations.

    Attributes:
        x (float): The first (X) value.
        y (float): The second (Y) value.
        z (float): The third (Z) value.
        w (float): The fourth (W) value.
        Default is (0, 0, 0, 1).
    '''
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, x: float, y: float, z: float, w: float) -> None: ...
    def __init__(self,
                 x: float | None = None,
                 y: float | None = None,
                 z: float | None = None,
                 w: float | None = None) -> None:
        if x is None and y is None and z is None and w is None:
            x, y, z, w = 0, 0, 0, 1
        super().__init__(x, y, z, w)

    def inverse(self) -> Quaternion:
        '''Gets the inverse to this quaternion.

        Returns:
            out (Quaternion): The inverse of the quaternion rotation that, when multiplied with
                              this quaternion, gives the identity quaternion (0, 0, 0, 1).
        '''
        a: float = 1.0 / (self.w*self.w + self.x*self.x + self.y*self.y + self.z*self.z)
        return Quaternion(-self.x * a, -self.y * a, -self.z * a, self.w * a)

    def to_matrix(self) -> Matrix3:
        '''Gets the matrix equivalent to the quaternion rotation.

        Returns:
            out (Matrix3): The matrix equivalent to the quaternion rotation.
        '''
        from .matrix import Matrix3 # pylint: disable=import-outside-toplevel
        out: Matrix3 = Matrix3()
        sqw: float = self.w * self.w
        sqx: float = self.x * self.x
        sqy: float = self.y * self.y
        sqz: float = self.z * self.z
        invs: float = 1.0 / (sqx + sqy + sqz + sqw)

        xy: float = self.x * self.y
        zw: float = self.z * self.w
        xz: float = self.x * self.z
        yw: float = self.y * self.w
        yz: float = self.y * self.z
        xw: float = self.x * self.w
        out.m = [
            [(sqx - sqy - sqz + sqw) * invs, 2.0 * (xy - zw) * invs, 2.0 * (xz - yw) * invs],
            [2.0 * (xy + zw) * invs, (-sqx + sqy - sqz + sqw) * invs, 2.0 * (yz - xw) * invs],
            [2.0 * (xz + yw) * invs, 2.0 * (yz + xw) * invs, (-sqx - sqy + sqz + sqw) * invs]
        ]
        return out

    def to_euler(self) -> Vector3:
        '''Gets the euler angles (in radians) equivalent to the quaternion rotation.
        The euler angles are a Vector3 values that represent the rotation around the X, Y, and Z.

        Returns:
            out (Vector3): The euler angles (X, Y, Z) in radians.
        '''
        sinr_cosp: float = 2.0 * (self.w*self.x + self.y*self.z)
        cosr_cosp: float = 1.0 - 2.0*(self.x*self.x + self.y*self.y)
        x: float = atan2(sinr_cosp, cosr_cosp)

        sinp: float = 2.0 * (self.w*self.y - self.z*self.x)
        y: float = copysign(pi / 2.0, sinp) if abs(sinp) >= 1.0 else asin(sinp)

        siny_cosp: float = 2.0 * (self.w*self.z + self.x*self.y)
        cosy_cosp: float = 1.0 - 2.0*(self.y*self.y + self.z*self.z)
        z: float = atan2(siny_cosp, cosy_cosp)

        return Vector3(x, y, z)

    @staticmethod
    def from_rotation(axis: Vector3, angle: float) -> Quaternion:
        '''Constructs a quaternion rotation of the given angle (in radians) around the given axis.

        Arguments:
            axis (Vector3): The axis of rotation. Only the direction matters, the length is ignored.
            angle (float): The angle of rotation, in radians.
        
        Returns:
            out (Quaternion): The quaternion representing the rotation.
        '''
        axis = axis.normalized()
        half_angle: float = angle / 2.0
        half_angle_sin: float = sin(half_angle)
        half_angle_cos: float = cos(half_angle)
        return Quaternion(axis.x * half_angle_sin,
                          axis.y * half_angle_sin,
                          axis.z * half_angle_sin,
                          half_angle_cos)

    @staticmethod
    def from_euler(angles: Vector3) -> Quaternion:
        '''Constructs a quaternion rotation, given in euler angles in radians.

        Arguments:
            angles (Vector3): The euler angles (X, Y, Z) in radians.
        
        Returns:
            out (Quaternion): The quaternion representing the rotation.
        '''
        half_angles: Vector3 = angles / 2.0
        cy: float = cos(half_angles.z)
        sy: float = sin(half_angles.z)
        cp: float = cos(half_angles.y)
        sp: float = sin(half_angles.y)
        cr: float = cos(half_angles.x)
        sr: float = sin(half_angles.x)
        return Quaternion(cy*cp*sr - sy*sp*cr,
                          sy*cp*sr + cy*sp*cr,
                          sy*cp*cr - cy*sp*sr,
                          cy*cp*cr + sy*sp*sr)

    @staticmethod
    def get_rotation_to(vector_from: Vector3,
                        vector_to: Vector3,
                        fallback_axis: Vector3 = Vector3.ZERO) -> Quaternion:
        '''Constructs a quaternion rotation that rotates between two vectors, so applying it to
        the first vector will result in the second one (assuming they have the same length).

        Originates from:
        https://github.com/ehsan/ogre/blob/master/OgreMain/include/OgreVector3.h#L643-L699

        Arguments:
            vector_from (Vector3): The vector to rotate from.
            vector_to (Vector3): The vector to rotate to.
            fallback_axis (Vector3): If both are parallel but opposite, a 180-degree rotation around
                                     the fallback axis will be used. Default: (0, 0, 0).
        
        Returns:
            out (Quaternion): The quaternion representing the rotation.
        '''
        vector_from = vector_from.normalized()
        vector_to = vector_to.normalized()
        d: float = vector_from.dot(vector_to)
        if d >= 1.0:
            return Quaternion()
        if d < (1e-6 - 1.0):
            if fallback_axis == Vector3.ZERO:
                fallback_axis = X_AXIS.cross(vector_from)
                if fallback_axis.length() < 1e-8:
                    fallback_axis = Y_AXIS.cross(vector_to)
                fallback_axis = fallback_axis.normalized()
            return Quaternion.from_rotation(fallback_axis, pi)
        s: float = sqrt((1.0 + d) * 2.0)
        invs: float = 1.0 / s
        c: Vector3 = vector_from.cross(vector_to)
        q: Quaternion = Quaternion(c.x * invs, c.y * invs, c.z * invs, s / 2.0)
        q /= q.length()
        return q

    # these overrides are mostly for custom docstrings
    def __str__(self) -> str:
        '''Gets a stringified quaternion.
        
        Returns:
            out (str): The formatted quaternion (x, y, z, w).'''
        return f'({self.x}, {self.y}, {self.z}, {self.w})'

    def __eq__(self, other: object) -> bool:
        '''Compares two quaternions for equality.
        
        Returns:
            out (bool): True if both quaternions are equal, False otherwise.
        '''
        if not isinstance(other, Quaternion):
            return NotImplemented
        return self.x == other.x and self.y == other.y and self.z == other.z and self.w == other.w

    def __neg__(self) -> Quaternion:
        '''Inverts all floats of the quaternion.

        Returns:
            out (Quaternion): The result quaternion with inverted values.
        '''
        return Quaternion(-self.x, -self.y, -self.z, -self.w)

    @overload
    def __add__(self, other: Quaternion) -> Quaternion: ...
    @overload
    def __add__(self, other: float) -> Quaternion:
        '''Adds a floating point value to all values of a quaternion.

        Arguments:
            other (float): The floating point value.
        
        Returns:
            out (Quaternion): The result quaternion.
        '''
        ...
    def __add__(self, other: Quaternion | Vector4 | float) -> Quaternion:
        '''Adds values of two quaternions.

        Arguments:
            other (Quaternion): Another quaternion.
        
        Returns:
            out (Quaternion): The result quaternion.
        '''
        if isinstance(other, Vector4):
            return Quaternion(self.x + other.x,
                              self.y + other.y,
                              self.z + other.z,
                              self.w + other.w)
        if isinstance(other, float | int):
            return Quaternion(self.x + other,
                              self.y + other,
                              self.z + other,
                              self.w + other)
        return NotImplemented

    @overload
    def __sub__(self, other: Quaternion | Vector4) -> Quaternion: ...
    @overload
    def __sub__(self, other: float) -> Quaternion:
        '''Subtracts a floating point value from all values of a quaternion.

        Arguments:
            other (float): The floating point value.
        
        Returns:
            out (Quaternion): The result quaternion.
        '''
        ...
    def __sub__(self, other: Quaternion | Vector4 | float) -> Quaternion:
        '''Subtracts values of two quaternions.

        Arguments:
            other (Quaternion): Another quaternion.
        
        Returns:
            out (Quaternion): The result quaternion.
        '''
        if isinstance(other, Vector4):
            return Quaternion(self.x - other.x,
                              self.y - other.y,
                              self.z - other.z,
                              self.w - other.w)
        if isinstance(other, float | int):
            return Quaternion(self.x - other,
                              self.y - other,
                              self.z - other,
                              self.w - other)
        return NotImplemented

    @overload
    def __mul__(self, other: Quaternion | Vector4) -> Quaternion: ...
    @overload
    def __mul__(self, other: float) -> Quaternion:
        '''Multiplies all values of a quaternion by a floating point value.

        Arguments:
            other (float): The floating point value.
        
        Returns:
            out (Quaternion): The result quaternion.
        '''
        ...
    def __mul__(self, other: Quaternion | Vector4 | float) -> Quaternion:
        '''Multiplies values of two quaternions.

        Arguments:
            other (Quaternion): Another quaternion.
        
        Returns:
            out (Quaternion): The result quaternion.
        '''
        if isinstance(other, Quaternion):
            return Quaternion(self.w*other.x + self.x*other.w + self.y*other.z - self.z*other.y,
                              self.w*other.y - self.x*other.z + self.y*other.w + self.z*other.x,
                              self.w*other.z + self.x*other.y - self.y*other.x + self.z*other.w,
                              self.w*other.w - self.x*other.x - self.y*other.y - self.z*other.z)
        if isinstance(other, Vector4):
            return Quaternion(self.x * other.x,
                              self.y * other.y,
                              self.z * other.z,
                              self.w * other.w)
        if isinstance(other, float | int):
            return Quaternion(self.x * other,
                              self.y * other,
                              self.z * other,
                              self.w * other)
        return NotImplemented

    @overload
    def __truediv__(self, other: Quaternion | Vector4) -> Quaternion: ...
    @overload
    def __truediv__(self, other: float) -> Quaternion:
        '''Divides all values of a quaternion by a floating point value.

        Arguments:
            other (float): The floating point value.
        
        Returns:
            out (Quaternion): The result quaternion.
        '''
        ...
    def __truediv__(self, other: Quaternion | Vector4 | float) -> Quaternion:
        '''Divides values of two quaternions.

        Arguments:
            other (Quaternion): Another quaternion.
        
        Returns:
            out (Quaternion): The result quaternion.
        '''
        if isinstance(other, Vector4):
            return Quaternion(self.x / other.x,
                              self.y / other.y,
                              self.z / other.z,
                              self.w / other.w)
        if isinstance(other, float | int):
            return Quaternion(self.x / other,
                              self.y / other,
                              self.z / other,
                              self.w / other)
        return NotImplemented

    @overload
    def __iadd__(self, other: Quaternion | Vector4) -> Quaternion: ...
    @overload
    def __iadd__(self, other: float) -> Quaternion:
        '''Adds a floating point value to all values of the quaternion.

        Arguments:
            other (float): The floating point value.
        '''
        ...
    def __iadd__(self, other: Quaternion | Vector4 | float) -> Quaternion:
        '''Adds values of one quaternion to another.

        Arguments:
            other (Quaternion): Another quaternion.
        '''
        if isinstance(other, Vector4):
            self.x += other.x
            self.y += other.y
            self.z += other.z
            self.w += other.w
            return self
        if isinstance(other, float | int):
            self.x += other
            self.y += other
            self.z += other
            self.w += other
            return self
        return NotImplemented

    @overload
    def __isub__(self, other: Quaternion | Vector4) -> Quaternion: ...
    @overload
    def __isub__(self, other: float) -> Quaternion:
        '''Subtracts a floating point value from all values of the quaternion.

        Arguments:
            other (float): The floating point value.
        '''
        ...
    def __isub__(self, other: Quaternion | Vector4 | float) -> Quaternion:
        '''Subtracts values of one quaternion from another.

        Arguments:
            other (Quaternion): Another quaternion.
        '''
        if isinstance(other, Vector4):
            self.x -= other.x
            self.y -= other.y
            self.z -= other.z
            self.w -= other.w
            return self
        if isinstance(other, float | int):
            self.x -= other
            self.y -= other
            self.z -= other
            self.w -= other
            return self
        return NotImplemented

    @overload
    def __imul__(self, other: Quaternion | Vector4) -> Quaternion: ...
    @overload
    def __imul__(self, other: float) -> Quaternion:
        '''Multiplies all values of the quaternion by a floating point value.

        Arguments:
            other (float): The floating point value.
        '''
        ...
    def __imul__(self, other: Quaternion | Vector4 | float) -> Quaternion:
        '''Multiplies values of one quaternion by another.

        Arguments:
            other (Quaternion): Another quaternion.
        '''
        if isinstance(other, Vector4):
            self.x *= other.x
            self.y *= other.y
            self.z *= other.z
            self.w *= other.w
            return self
        if isinstance(other, float | int):
            self.x *= other
            self.y *= other
            self.z *= other
            self.w *= other
            return self
        return NotImplemented

    @overload
    def __itruediv__(self, other: Quaternion | Vector4) -> Quaternion: ...
    @overload
    def __itruediv__(self, other: float) -> Quaternion:
        '''Divides all values of the quaternion by a floating point value.

        Arguments:
            other (float): The floating point value.
        '''
        ...
    def __itruediv__(self, other: Quaternion | Vector4 | float) -> Quaternion:
        '''Divides values of one quaternion by another.

        Arguments:
            other (Quaternion): Another quaternion.
        '''
        if isinstance(other, Vector4):
            self.x /= other.x
            self.y /= other.y
            self.z /= other.z
            self.w /= other.w
            return self
        if isinstance(other, float | int):
            self.x /= other
            self.y /= other
            self.z /= other
            self.w /= other
            return self
        return NotImplemented

    __radd__ = __add__

    __rmul__ = __mul__

    def __rsub__(self, other: float) -> Quaternion:
        '''Subtracts all values of the quaternion from a floating point value.
        
        Arguments:
            other (float): The floating point value.
        '''
        if not isinstance(other, float | int):
            return NotImplemented
        return Quaternion(other - self.x, other - self.y, other - self.z, other - self.w)

    def __rtruediv__(self, other: float) -> Quaternion:
        '''Divides a floating point value by all values of the Quaternion.

        Arguments:
            other (float): The floating point value.
        '''
        if isinstance(other, float | int):
            return Quaternion(other / self.x, other / self.y, other / self.z, other / self.w)
        return NotImplemented
