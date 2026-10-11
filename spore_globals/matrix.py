#!/usr/bin/env python3

'''Provides simple matrix structures and functions.'''

from __future__ import annotations




from math import atan2, sqrt, sin, cos
from typing import overload, TYPE_CHECKING
from .vector import Vector3, Z_AXIS
if TYPE_CHECKING:
    from .quaternion import Quaternion




class Matrix3:
    '''A class that represents a 3x3 matrix.

    Attributes:
        m (list[list[float]]): The 3x3 matrix values.
    '''
    def __init__(self) -> None:
        self.m = None

    @property
    def m(self) -> list[list[float]]:
        '''The 3x3 matrix values.'''
        return self._m
    @m.setter
    def m(self, m_modified: list[list[float]] | None) -> None:
        if (isinstance(m_modified, list)
            and len(m_modified) == 3
            and all(isinstance(row, list) and len(row) == 3 for row in m_modified)):
            self._m: list[list[float]] = m_modified
        else:
            self._m: list[list[float]] = [[0 for _ in range(3)] for _ in range(3)]

    def row(self, index: int) -> list[float]:
        '''Gets a row of the matrix.

        Arguments:
            index (int): The row index (0-2).
        
        Returns:
            out (list[float]): The row values.
        '''
        return self.m[index]

    def column(self, index: int) -> list[float]:
        '''Gets a column of the matrix.

        Arguments:
            index (int): The column index (0-2).
        
        Returns:
            out (list[float]): The column values.
        '''
        return [self.m[i][index] for i in range(3)]

    def set_identity(self) -> None:
        '''Sets the matrix to the identity matrix (1.0s in the diagonal, everything else 0.0s).'''
        self.m = [[1 if i == j else 0 for j in range(3)] for i in range(3)]

    def to_euler(self) -> Vector3:
        '''Gets the euler angles (in radians) equivalent to the matrix rotation.
        The euler angles are a Vector3 values that represent the rotation around the X, Y, and Z.

        Returns:
            out (Vector3): The euler angles (X, Y, Z) in radians.
        '''
        m00: float = self.m[0][0]
        m01: float = self.m[0][1]
        m02: float = self.m[0][2]
        m11: float = self.m[1][1]
        m12: float = self.m[1][2]
        m21: float = self.m[2][1]
        m22: float = self.m[2][2]

        sy: float = sqrt(m00*m00 + m01*m01)
        if sy > 0.001:
            x: float = atan2(m12, m22)
            y: float = atan2(-m02, sy)
            z: float = atan2(m01, m00)
        else:
            x: float = atan2(-m21, m11)
            y: float = atan2(-m02, sy)
            z: float = 0
        return Vector3(x, y, z)

    def to_quaternion(self) -> Quaternion:
        '''Gets the quaternion that represents the matrix rotation.

        Returns:
            out (Quaternion): The quaternion equivalent to the matrix rotation.
        '''
        from .quaternion import Quaternion # pylint: disable=import-outside-toplevel
        m00: float = self.m[0][0]
        m01: float = self.m[0][1]
        m02: float = self.m[0][2]
        m10: float = self.m[1][0]
        m11: float = self.m[1][1]
        m12: float = self.m[1][2]
        m20: float = self.m[2][0]
        m21: float = self.m[2][1]
        m22: float = self.m[2][2]

        trace: float = m00 + m11 + m22
        if trace > 0:
            s: float = 0.5 / sqrt(trace + 1.0)
            return Quaternion((m12 - m21) * s, (m20 - m02) * s, (m01 - m10) * s, 0.25 / s)
        if m00 > m11 and m00 > m22:
            s: float = 2.0 * sqrt(1.0 + m00 - m11 - m22)
            return Quaternion(0.25 * s, (m01 + m10) / s, (m02 + m20) / s, (m21 - m12) / s)
        if m11 > m22:
            s: float = 2.0 * sqrt(1.0 + m11 - m00 - m22)
            return Quaternion((m10 + m01) / s, 0.25 * s, (m21 + m12) / s, (m20 - m02) / s)
        s: float = 2.0 * sqrt(1.0 + m22 - m00 - m11)
        return Quaternion((m20 + m02) / s, (m21 + m12) / s, 0.25 * s, (m01 - m10) / s)

    def transposed(self) -> Matrix3:
        '''Gets the transpose of the matrix (rows and columns swapped).

        Returns:
            out (Matrix3): The transposed matrix.
        '''
        out: Matrix3 = Matrix3()
        out.m = [[self.m[j][i] for j in range(3)] for i in range(3)]
        return out

    @staticmethod
    def from_euler(angles: Vector3) -> Matrix3:
        '''Creates a 3x3 rotation matrix equivalent to euler angles (in radians).
        The euler angles are a Vector3 values that represent the rotation around the X, Y, and Z.

        Arguments:
            angles (Vector3): The euler angles (X, Y, Z) in radians.
        
        Returns:
            out (Matrix3): The matrix equivalent to the euler angles rotation.
        '''
        sx: float = sin(angles.x)
        cx: float = cos(angles.x)
        sy: float = sin(angles.y)
        cy: float = cos(angles.y)
        sz: float = sin(angles.z)
        cz: float = cos(angles.z)
        out: Matrix3 = Matrix3()
        out.m = [
            [cy * cz, cy * sz, -sy],
            [sy*sx*cz - cx*sz, sy*sx*sz + cx*cz, cy * sx],
            [sy*cx*cz + sx*sz, sy*cx*sz - sx*cz, cy * cx],
        ]
        return out

    @staticmethod
    def from_axis_angle(axis: Vector3, angle: float) -> Matrix3:
        '''Creates a 3x3 rotation matrix that rotates around an axis.
        This is an equivalent to `Quaternion.from_rotation(axis, angle).to_matrix()`.

        Arguments:
            axis (Vector3): The axis of rotation.
            angle (float): The angle of rotation, in radians.
        
        Returns:
            out (Matrix3): The matrix equivalent to the axis-angle
        '''
        axis = axis.normalized()
        c: float = cos(angle)
        s: float = sin(angle)
        cx: float = (1.0 - c) * axis.x
        cy: float = (1.0 - c) * axis.y
        cz: float = (1.0 - c) * axis.z
        out: Matrix3 = Matrix3()
        out.m = [
            axis.x*cx + c, axis.x*cy - axis.z*s, axis.x*cz + axis.y*s,
            axis.y*cx + axis.z*s, axis.y*cy + c, axis.y*cz - axis.x*s,
            axis.z*cx - axis.y*s, axis.z*cy + axis.x*s, axis.z*cz + c
        ]
        return out

    @staticmethod
    def look_at(position: Vector3, target: Vector3, up: Vector3 = Z_AXIS) -> Matrix3:
        '''Creates a 3x3 rotation matrix that can be used to orient an object towards a target.
        Might give unexpected results if target and position are aligned.

        Arguments:
            position (Vector3): The position of the looking ("eye") object.
            target (Vector3): The position to look at.
            up (Vector3): The up direction. Default: Z_AXIS.
        
        Returns:
            out (Matrix3): The rotation matrix that looks at the target.
        '''
        direction: Vector3 = (target - position).normalized()
        right: Vector3 = (up.cross(direction)).normalized()
        camera_up: Vector3 = direction.cross(right).normalized()
        out: Matrix3 = Matrix3()
        out.m = [
            [-right.x, -right.y, -right.z],
            [direction.x, direction.y, direction.z],
            [camera_up.x, camera_up.y, camera_up.z]
        ]
        return out

    def __str__(self) -> str:
        '''Gets a stringified 3x3 matrix.
        
        Returns:
            out (str): The formatted matrix ((m00, m01, m02), (m10, m11, m12), (m20, m21, m22)).
        '''
        return f'({self.m[0]}, {self.m[1]}, {self.m[2]})'

    def __eq__(self, other: object) -> bool:
        '''Compares two 3x3 matrices for equality.
        
        Returns:
            out (bool): True if both matrices are equal, False otherwise.
        '''
        if not isinstance(other, Matrix3):
            return NotImplemented
        return self.m == other.m

    @overload
    def __mul__(self, other: Matrix3) -> Matrix3: ...
    @overload
    def __mul__(self, other: Vector3) -> Vector3:
        '''Multiplies a 3x3 matrix by a Vector3.

        Arguments:
            other (Vector3): A vector to multiply by.
        
        Returns:
            out (Vector3): The result vector.
        '''
        ...
    def __mul__(self, other: Matrix3 | Vector3) -> Matrix3 | Vector3:
        '''Multiplies two 3x3 matrices.

        Arguments:
            other (Matrix3): Another matrix.
        
        Returns:
            out (Matrix3): The result matrix.
        '''
        if isinstance(other, Matrix3):
            out: Matrix3 = Matrix3()
            out.m = [
                [sum(self.m[i][k] * other.m[k][j] for k in range(3))
                for j in range(3)] for i in range(3)
            ]
            return out
        if isinstance(other, Vector3):
            return Vector3(
                self.m[0][0]*other.x + self.m[0][1]*other.y + self.m[0][2]*other.z,
                self.m[1][0]*other.x + self.m[1][1]*other.y + self.m[1][2]*other.z,
                self.m[2][0]*other.x + self.m[2][1]*other.y + self.m[2][2]*other.z
            )
        return NotImplemented




class Matrix4:
    '''A class that represents a 4x4 matrix.

    Attributes:
        m (list[list[float]]): The 4x4 matrix values.
    '''
    def __init__(self) -> None:
        self.m = None

    @property
    def m(self) -> list[list[float]]:
        '''The 4x4 matrix values.'''
        return self._m
    @m.setter
    def m(self, m_modified: list[list[float]] | None) -> None:
        if (isinstance(m_modified, list)
            and len(m_modified) == 4
            and all(isinstance(row, list) and len(row) == 4 for row in m_modified)):
            self._m: list[list[float]] = m_modified
        else:
            self._m: list[list[float]] = [[0 for _ in range(4)] for _ in range(4)]

    def row(self, index: int) -> list[float]:
        '''Gets a row of the matrix.

        Arguments:
            index (int): The row index (0-3).
        
        Returns:
            out (list[float]): The row values.
        '''
        return self.m[index]

    def column(self, index: int) -> list[float]:
        '''Gets a column of the matrix.

        Arguments:
            index (int): The column index (0-3).
        
        Returns:
            out (list[float]): The column values.
        '''
        return [self.m[i][index] for i in range(4)]

    def set_identity(self) -> None:
        '''Sets the matrix to the identity matrix (1.0s in the diagonal, everything else 0.0s).'''
        self.m = [[1 if i == j else 0 for j in range(4)] for i in range(4)]

    def transposed(self) -> Matrix4:
        '''Gets the transpose of the matrix (rows and columns swapped).

        Returns:
            out (Matrix4): The transposed matrix.
        '''
        out: Matrix4 = Matrix4()
        out.m = [[self.m[j][i] for j in range(4)] for i in range(4)]
        return out

    def to_3x3(self) -> Matrix3:
        '''Gets the 3x3 the 3x3 part of this matrix, removing the last column and row.

        Returns:
            out (Matrix3): The result 3x3 matrix.
        '''
        out: Matrix3 = Matrix3()
        out.m = [[self.m[i][j] for j in range(3)] for i in range(3)]
        return out

    def __str__(self) -> str:
        '''Gets a stringified 4x4 matrix.
        
        Returns:
            out (str): The formatted matrix
                       ((m00, m01, m02, m03), (m10, m11, m12, m13),
                       (m20, m21, m22, m23), (m30, m31, m32, m33)).
        '''
        return f'({self.m[0]}, {self.m[1]}, {self.m[2]}, {self.m[3]})'

    def __eq__(self, other: object) -> bool:
        '''Compares two 4x4 matrices for equality.
        
        Returns:
            out (bool): True if both matrices are equal, False otherwise.
        '''
        if not isinstance(other, Matrix4):
            return NotImplemented
        return self.m == other.m
