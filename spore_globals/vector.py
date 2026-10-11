#!/usr/bin/env python3

'''Provides Spore floating point vectors.'''

from __future__ import annotations




from math import acos, sqrt, pi
from typing import overload, TYPE_CHECKING
if TYPE_CHECKING:
    from .point import Point




class Vector2:
    '''A class that represents Spore vector of two floating point values (X, Y).
    Similar to Point, but used for different purposes(properties, math, etc.).

    Attributes:
        x (float): The first (X) value.
        y (float): The second (Y) value.
    '''
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, point: Point) -> None: ...
    @overload
    def __init__(self, x: float, y: float) -> None: ...
    def __init__(self,
                 x_point: float | Point | None = None,
                 y: float | None = None) -> None:
        from .point import Point # pylint: disable=import-outside-toplevel
        if isinstance(x_point, Point):
            self.x = x_point.x
            self.y = x_point.y
        else:
            self.x = x_point
            self.y = y

    @property
    def x(self) -> float:
        '''The first (X) value.'''
        return self._x
    @x.setter
    def x(self, x_modified: float | None) -> None:
        self._x: float = x_modified if x_modified is not None else 0

    @property
    def y(self) -> float:
        '''The second (Y) value.'''
        return self._y
    @y.setter
    def y(self, y_modified: float | None) -> None:
        self._y: float = y_modified if y_modified is not None else 0

    def length(self) -> float:
        '''Calculates the length of the vector, calculated as the square root of the sum of its
        components squared.

        Returns:
            out (float): The length of the vector.
        '''
        return sqrt(self.x*self.x + self.y*self.y)

    def normalized(self) -> Vector2:
        '''Calculates the normalized vector. Being normalized means it has a length of 1.0.

        Returns:
            out (Vector2): The normalized vector.
        '''
        return self / self.length()

    def dot(self, other: Vector2) -> float:
        '''Calculates the dot product between this vector and the other one.
        The dot product is calculated as `a.x * b.x + a.y * b.y + a.z * b.z`.

        Arguments:
            other (Vector2): Another vector.
        
        Returns:
            out (float): The calculated dot product.
        '''
        return self.x*other.x + self.y*other.y

    def lerp(self, other: Vector2, mix: float) -> Vector2:
        '''Calculates the linear interpolation between this vector and the other one.
        
        Arguments:
            other (Vector2): Another vector.
            mix (float): The interpolation factor, in the range [0.0, 1.0].

        Returns:
            out (Vector2): The result vector.
        '''
        return Vector2(
            self.x + (other.x-self.x)*mix,
            self.y + (other.y-self.y)*mix
        )

    def __str__(self) -> str:
        '''Gets a stringified Vector2.
        
        Returns:
            out (str): The formatted vector (x, y).'''
        return f'({self.x}, {self.y})'

    def __eq__(self, other: object) -> bool:
        '''Compares two Vector2s for equality.
        
        Returns:
            out (bool): True if both vectors are equal, False otherwise.
        '''
        if not isinstance(other, Vector2):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __neg__(self) -> Vector2:
        '''Inverts both floats of the Vector2.

        Returns:
            out (Vector2): The result vector with inverted values.
        '''
        return Vector2(-self.x, -self.y)

    @overload
    def __add__(self, other: Vector2) -> Vector2: ...
    @overload
    def __add__(self, other: float) -> Vector2:
        '''Adds a floating point value to both values of a Vector2.

        Arguments:
            other (float): The floating point value.
        
        Returns:
            out (Vector2): The result vector.
        '''
        ...
    def __add__(self, other: Vector2 | float) -> Vector2:
        '''Adds values of two Vector2s.

        Arguments:
            other (Vector2): Another vector.
        
        Returns:
            out (Vector2): The result vector.
        '''
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
        if isinstance(other, (float, int)):
            return Vector2(self.x + other, self.y + other)
        return NotImplemented

    @overload
    def __sub__(self, other: Vector2) -> Vector2: ...
    @overload
    def __sub__(self, other: float) -> Vector2:
        '''Subtracts a floating point value from both values of a Vector2.

        Arguments:
            other (float): The floating point value.
        
        Returns:
            out (Vector2): The result vector.
        '''
        ...
    def __sub__(self, other: Vector2 | float) -> Vector2:
        '''Subtracts values of two Vector2s.

        Arguments:
            other (Vector2): Another vector.
        
        Returns:
            out (Vector2): The result vector.
        '''
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x, self.y - other.y)
        if isinstance(other, (float, int)):
            return Vector2(self.x - other, self.y - other)
        return NotImplemented

    @overload
    def __mul__(self, other: Vector2) -> Vector2: ...
    @overload
    def __mul__(self, other: float) -> Vector2:
        '''Multiplies both values of a Vector2 by a floating point value.

        Arguments:
            other (float): The floating point value.
        
        Returns:
            out (Vector2): The result vector.
        '''
        ...
    def __mul__(self, other: Vector2 | float) -> Vector2:
        '''Multiplies values of two Vector2s.

        Arguments:
            other (Vector2): Another vector.
        
        Returns:
            out (Vector2): The result vector.
        '''
        if isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)
        if isinstance(other, (float, int)):
            return Vector2(self.x * other, self.y * other)
        return NotImplemented

    @overload
    def __truediv__(self, other: Vector2) -> Vector2: ...
    @overload
    def __truediv__(self, other: float) -> Vector2:
        '''Divides both values of a Vector2 by a floating point value.

        Arguments:
            other (float): The floating point value.
        
        Returns:
            out (Vector2): The result vector.
        '''
        ...
    def __truediv__(self, other: Vector2 | float) -> Vector2:
        '''Divides values of two Vector2s.

        Arguments:
            other (Vector2): Another vector.
        
        Returns:
            out (Vector2): The result vector.
        '''
        if isinstance(other, Vector2):
            return Vector2(self.x / other.x, self.y / other.y)
        if isinstance(other, (float, int)):
            return Vector2(self.x / other, self.y / other)
        return NotImplemented

    @overload
    def __iadd__(self, other: Vector2) -> Vector2: ...
    @overload
    def __iadd__(self, other: float) -> Vector2:
        '''Adds a floating point value to both values of the Vector2.

        Arguments:
            other (float): The floating point value.
        '''
        ...
    def __iadd__(self, other: Vector2 | float) -> Vector2:
        '''Adds values of one Vector2 to another.

        Arguments:
            other (Vector2): Another vector.
        '''
        if isinstance(other, Vector2):
            self.x += other.x
            self.y += other.y
            return self
        if isinstance(other, (float, int)):
            self.x += other
            self.y += other
            return self
        return NotImplemented

    @overload
    def __isub__(self, other: Vector2) -> Vector2: ...
    @overload
    def __isub__(self, other: float) -> Vector2:
        '''Subtracts a floating point value from both values of the Vector2.

        Arguments:
            other (float): The floating point value.
        '''
        ...
    def __isub__(self, other: Vector2 | float) -> Vector2:
        '''Subtracts values of one Vector2 from another.

        Arguments:
            other (Vector2): Another vector.
        '''
        if isinstance(other, Vector2):
            self.x -= other.x
            self.y -= other.y
            return self
        if isinstance(other, (float, int)):
            self.x -= other
            self.y -= other
            return self
        return NotImplemented

    @overload
    def __imul__(self, other: Vector2) -> Vector2: ...
    @overload
    def __imul__(self, other: float) -> Vector2:
        '''Multiplies both values of the Vector2 by a floating point value.

        Arguments:
            other (float): The floating point value.
        '''
        ...
    def __imul__(self, other: Vector2 | float) -> Vector2:
        '''Multiplies values of one Vector2 by another.

        Arguments:
            other (Vector2): Another vector.
        '''
        if isinstance(other, Vector2):
            self.x *= other.x
            self.y *= other.y
            return self
        if isinstance(other, (float, int)):
            self.x *= other
            self.y *= other
            return self
        return NotImplemented

    @overload
    def __itruediv__(self, other: Vector2) -> Vector2: ...
    @overload
    def __itruediv__(self, other: float) -> Vector2:
        '''Divides both values of the Vector2 by a floating point value.

        Arguments:
            other (float): The floating point value.
        '''
        ...
    def __itruediv__(self, other: Vector2 | float) -> Vector2:
        '''Divides values of one Vector2 by another.
        
        Arguments:
            other (Vector2): Another vector.
        '''
        if isinstance(other, Vector2):
            self.x /= other.x
            self.y /= other.y
            return self
        if isinstance(other, (float, int)):
            self.x /= other
            self.y /= other
            return self
        return NotImplemented

    __radd__ = __add__

    __rmul__ = __mul__

    def __rsub__(self, other: float) -> Vector2:
        '''Subtracts both values of the Vector2 from a floating point value.
        
        Arguments:
            other (float): The floating point value.
        '''
        if not isinstance(other, (float, int)):
            return NotImplemented
        return Vector2(other - self.x, other - self.y)

    def __rtruediv__(self, other: float) -> Vector2:
        '''Divides a floating point value by both values of the Vector2.

        Arguments:
            other (float): The floating point value.
        '''
        if isinstance(other, (float, int)):
            return Vector2(other / self.x, other / self.y)
        return NotImplemented

    ZERO: Vector2

Vector2.ZERO = Vector2()




class Vector3:
    '''A class that represents Spore vector of three floating point values (X, Y, Z).

    Attributes:
        x (float): The first (X) value.
        y (float): The second (Y) value.
        z (float): The third (Z) value.
    '''
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, x: float, y: float, z: float) -> None: ...
    def __init__(self,
                 x: float | None = None,
                 y: float | None = None,
                 z: float | None = None) -> None:
        self.x = x
        self.y = y
        self.z = z

    @property
    def x(self) -> float:
        '''The first (X) value.'''
        return self._x
    @x.setter
    def x(self, x_modified: float | None) -> None:
        self._x: float = x_modified if x_modified is not None else 0

    @property
    def y(self) -> float:
        '''The second (Y) value.'''
        return self._y
    @y.setter
    def y(self, y_modified: float | None) -> None:
        self._y: float = y_modified if y_modified is not None else 0

    @property
    def z(self) -> float:
        '''The third (Z) value.'''
        return self._z
    @z.setter
    def z(self, z_modified: float | None) -> None:
        self._z: float = z_modified if z_modified is not None else 0

    def length(self) -> float:
        '''Calculates the length of the vector, calculated as the square root of the sum of its
        components squared.

        Returns:
            out (float): The length of the vector.
        '''
        return sqrt(self.x*self.x + self.y*self.y + self.z*self.z)

    def squared_length(self) -> float:
        '''Calculates the squared length of the vector. Similar to length(), but without applying
        the square root.

        Returns:
            out (float): The squared length of the vector.
        '''
        return self.x*self.x + self.y*self.y + self.z*self.z

    def normalized(self) -> Vector3:
        '''Calculates the normalized vector. Being normalized means it has a length of 1.0.

        Returns:
            out (Vector3): The normalized vector.
        '''
        return self / self.length()

    def dot(self, other: Vector3) -> float:
        '''Calculates the dot product between this vector and the other one.
        The dot product is calculated as `a.x * b.x + a.y * b.y + a.z * b.z`.

        Arguments:
            other (Vector3): Another vector.
        
        Returns:
            out (float): The calculated dot product.
        '''
        return self.x*other.x + self.y*other.y + self.z*other.z

    def cross(self, other: Vector3) -> Vector3:
        '''Calculates the cross product between this vector and the other one.
        This will return a vector that is perpendicular to both vectors.

        Arguments:
            other (Vector3): Another vector.

        Returns:
            out (Vector3): The calculated perpendicular vector (cross product).
        '''
        return Vector3(
            self.y*other.z - self.z*other.y,
            self.z*other.x - self.x*other.z,
            self.x*other.y - self.y*other.x
        )

    def angle_to(self, other: Vector3) -> float:
        '''Calculates the angle between this vector and the other one in radians,
        in the range [0, PI].

        Arguments:
            other (Vector3): Another vector.

        Returns:
            out (float): The calculated angle in radians.
        '''
        return acos(self.dot(other) / (other.length()*self.length()))

    @staticmethod
    def oriented_angle(v1: Vector3, v2: Vector3, orientation_axis: Vector3) -> float:
        '''Calculates the oriented angle between two vectors in radians, in the range [0, 2pi).
        An additional vector must be passed to determine which is the orientation (i.e. whether a
		positive angle moves from `v1` to `v2` or the other way around), following
        the "right hand rule".

        Arguments:
            v1 (Vector3): The first vector.
            v2 (Vector3): The second vector.
            orientation_axis (Vector3): The axis used to determine the orientation.
        
        Returns:
            out (float): The calculated oriented angle in radians.
        '''
        v1, v2 = v1.normalized(), v2.normalized()
        if v1 == v2:
            return 0
        angle: float = acos(max(-1.0, min(v1.dot(v2), 1.0)))
        if orientation_axis.dot(v1.cross(v2)) < 0:
            angle = 2*pi - angle
        return angle

    def lerp(self, other: Vector3, mix: float) -> Vector3:
        '''Calculates the linear interpolation between this vector and the other one.
        
        Arguments:
            other (Vector3): Another vector.
            mix (float): The interpolation factor, in the range [0.0, 1.0].

        Returns:
            out (Vector3): The result vector.
        '''
        return Vector3(
            self.x + (other.x-self.x)*mix,
            self.y + (other.y-self.y)*mix,
            self.z + (other.z-self.z)*mix
        )

    def __str__(self) -> str:
        '''Gets a stringified Vector3.
        
        Returns:
            out (str): The formatted vector (x, y, z).'''
        return f'({self.x}, {self.y}, {self.z})'

    def __eq__(self, other: object) -> bool:
        '''Compares two Vector3s for equality.
        
        Returns:
            out (bool): True if both vectors are equal, False otherwise.
        '''
        if not isinstance(other, Vector3):
            return NotImplemented
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __neg__(self) -> Vector3:
        '''Inverts all floats of the Vector3.

        Returns:
            out (Vector3): The result vector with inverted values.
        '''
        return Vector3(-self.x, -self.y, -self.z)

    @overload
    def __add__(self, other: Vector3) -> Vector3: ...
    @overload
    def __add__(self, other: float) -> Vector3:
        '''Adds a floating point value to all values of a Vector3.

        Arguments:
            other (float): The floating point value.
        
        Returns:
            out (Vector3): The result vector.
        '''
        ...
    def __add__(self, other: Vector3 | float) -> Vector3:
        '''Adds values of two Vector3s.

        Arguments:
            other (Vector3): Another vector.
        
        Returns:
            out (Vector3): The result vector.
        '''
        if isinstance(other, Vector3):
            return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
        if isinstance(other, (float, int)):
            return Vector3(self.x + other, self.y + other, self.z + other)
        return NotImplemented

    @overload
    def __sub__(self, other: Vector3) -> Vector3: ...
    @overload
    def __sub__(self, other: float) -> Vector3:
        '''Subtracts a floating point value from all values of a Vector3.

        Arguments:
            other (float): The floating point value.
        
        Returns:
            out (Vector3): The result vector.
        '''
        ...
    def __sub__(self, other: Vector3 | float) -> Vector3:
        '''Subtracts values of two Vector3s.

        Arguments:
            other (Vector3): Another vector.
        
        Returns:
            out (Vector3): The result vector.
        '''
        if isinstance(other, Vector3):
            return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
        if isinstance(other, (float, int)):
            return Vector3(self.x - other, self.y - other, self.z - other)
        return NotImplemented

    @overload
    def __mul__(self, other: Vector3) -> Vector3: ...
    @overload
    def __mul__(self, other: float) -> Vector3:
        '''Multiplies all values of a Vector3 by a floating point value.

        Arguments:
            other (float): The floating point value.
        
        Returns:
            out (Vector3): The result vector.
        '''
        ...
    def __mul__(self, other: Vector3 | float) -> Vector3:
        '''Multiplies values of two Vector3s.

        Arguments:
            other (Vector3): Another vector.
        
        Returns:
            out (Vector3): The result vector.
        '''
        if isinstance(other, Vector3):
            return Vector3(self.x * other.x, self.y * other.y, self.z * other.z)
        if isinstance(other, (float, int)):
            return Vector3(self.x * other, self.y * other, self.z * other)
        return NotImplemented

    @overload
    def __truediv__(self, other: Vector3) -> Vector3: ...
    @overload
    def __truediv__(self, other: float) -> Vector3:
        '''Divides all values of a Vector3 by a floating point value.

        Arguments:
            other (float): The floating point value.
        
        Returns:
            out (Vector3): The result vector.
        '''
        ...
    def __truediv__(self, other: Vector3 | float) -> Vector3:
        '''Divides values of two Vector3s.

        Arguments:
            other (Vector3): Another vector.
        
        Returns:
            out (Vector3): The result vector.
        '''
        if isinstance(other, Vector3):
            return Vector3(self.x / other.x, self.y / other.y, self.z / other.z)
        if isinstance(other, (float, int)):
            return Vector3(self.x / other, self.y / other, self.z / other)
        return NotImplemented

    @overload
    def __iadd__(self, other: Vector3) -> Vector3: ...
    @overload
    def __iadd__(self, other: float) -> Vector3:
        '''Adds a floating point value to all values of the Vector3.

        Arguments:
            other (float): The floating point value.
        '''
        ...
    def __iadd__(self, other: Vector3 | float) -> Vector3:
        '''Adds values of one Vector3 to another.

        Arguments:
            other (Vector3): Another vector.
        '''
        if isinstance(other, Vector3):
            self.x += other.x
            self.y += other.y
            self.z += other.z
            return self
        if isinstance(other, (float, int)):
            self.x += other
            self.y += other
            self.z += other
            return self
        return NotImplemented

    @overload
    def __isub__(self, other: Vector3) -> Vector3: ...
    @overload
    def __isub__(self, other: float) -> Vector3:
        '''Subtracts a floating point value from all values of the Vector3.

        Arguments:
            other (float): The floating point value.
        '''
        ...
    def __isub__(self, other: Vector3 | float) -> Vector3:
        '''Subtracts values of one Vector3 from another.

        Arguments:
            other (Vector3): Another vector.
        '''
        if isinstance(other, Vector3):
            self.x -= other.x
            self.y -= other.y
            self.z -= other.z
            return self
        if isinstance(other, (float, int)):
            self.x -= other
            self.y -= other
            self.z -= other
            return self
        return NotImplemented

    @overload
    def __imul__(self, other: Vector3) -> Vector3: ...
    @overload
    def __imul__(self, other: float) -> Vector3:
        '''Multiplies all values of the Vector3 by a floating point value.

        Arguments:
            other (float): The floating point value.
        '''
        ...
    def __imul__(self, other: Vector3 | float) -> Vector3:
        '''Multiplies values of one Vector3 by another.

        Arguments:
            other (Vector3): Another vector.
        '''
        if isinstance(other, Vector3):
            self.x *= other.x
            self.y *= other.y
            self.z *= other.z
            return self
        if isinstance(other, (float, int)):
            self.x *= other
            self.y *= other
            self.z *= other
            return self
        return NotImplemented

    @overload
    def __itruediv__(self, other: Vector3) -> Vector3: ...
    @overload
    def __itruediv__(self, other: float) -> Vector3:
        '''Divides all values of the Vector3 by a floating point value.

        Arguments:
            other (float): The floating point value.
        '''
        ...
    def __itruediv__(self, other: Vector3 | float) -> Vector3:
        '''Divides values of one Vector3 by another.

        Arguments:
            other (Vector3): Another vector.
        '''
        if isinstance(other, Vector3):
            self.x /= other.x
            self.y /= other.y
            self.z /= other.z
            return self
        if isinstance(other, (float, int)):
            self.x /= other
            self.y /= other
            self.z /= other
            return self
        return NotImplemented

    __radd__ = __add__

    __rmul__ = __mul__

    def __rsub__(self, other: float) -> Vector3:
        '''Subtracts all values of the Vector3 from a floating point value.
        
        Arguments:
            other (float): The floating point value.
        '''
        if not isinstance(other, (float, int)):
            return NotImplemented
        return Vector3(other - self.x, other - self.y, other - self.z)

    def __rtruediv__(self, other: float) -> Vector3:
        '''Divides a floating point value by all values of the Vector3.

        Arguments:
            other (float): The floating point value.
        '''
        if isinstance(other, (float, int)):
            return Vector3(other / self.x, other / self.y, other / self.z)
        return NotImplemented

    ZERO: Vector3

Vector3.ZERO = Vector3()

X_AXIS: Vector3 = Vector3(1, 0, 0)
Y_AXIS: Vector3 = Vector3(0, 1, 0)
Z_AXIS: Vector3 = Vector3(0, 0, 1)




class Vector4:
    '''A class that represents Spore vector of four floating point values (X, Y, Z, W).

    Attributes:
        x (float): The first (X) value.
        y (float): The second (Y) value.
        z (float): The third (Z) value.
        w (float): The fourth (W) value.
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
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    @property
    def x(self) -> float:
        '''The first (X) value.'''
        return self._x
    @x.setter
    def x(self, x_modified: float | None) -> None:
        self._x: float = x_modified if x_modified is not None else 0

    @property
    def y(self) -> float:
        '''The second (Y) value.'''
        return self._y
    @y.setter
    def y(self, y_modified: float | None) -> None:
        self._y: float = y_modified if y_modified is not None else 0

    @property
    def z(self) -> float:
        '''The third (Z) value.'''
        return self._z
    @z.setter
    def z(self, z_modified: float | None) -> None:
        self._z: float = z_modified if z_modified is not None else 0

    @property
    def w(self) -> float:
        '''The fourth (W) value.'''
        return self._w
    @w.setter
    def w(self, w_modified: float | None) -> None:
        self._w: float = w_modified if w_modified is not None else 0

    def length(self) -> float:
        '''Calculates the length of the vector, calculated as the square root of the sum of its
        components squared.

        Returns:
            out (float): The length of the vector.
        '''
        return sqrt(self.x*self.x + self.y*self.y + self.z*self.z + self.w*self.w)

    def normalized(self) -> Vector4:
        '''Calculates the normalized vector. Being normalized means it has a length of 1.0.

        Returns:
            out (Vector4): The normalized vector.
        '''
        return self / self.length()

    def dot(self, other: Vector4) -> float:
        '''Calculates the dot product between this vector and the other one.
        The dot product is calculated as `a.x * b.x + a.y * b.y + a.z * b.z`.

        Arguments:
            other (Vector4): Another vector.
        
        Returns:
            out (float): The calculated dot product.
        '''
        return self.x*other.x + self.y*other.y + self.z*other.z + self.w*other.w

    def lerp(self, other: Vector4, mix: float) -> Vector4:
        '''Calculates the linear interpolation between this vector and the other one.
        
        Arguments:
            other (Vector4): Another vector.
            mix (float): The interpolation factor, in the range [0.0, 1.0].

        Returns:
            out (Vector4): The result vector.
        '''
        return Vector4(
            self.x + (other.x-self.x)*mix,
            self.y + (other.y-self.y)*mix,
            self.z + (other.z-self.z)*mix,
            self.w + (other.w-self.w)*mix
        )

    def __str__(self) -> str:
        '''Gets a stringified Vector4.
        
        Returns:
            out (str): The formatted vector (x, y, z, w).'''
        return f'({self.x}, {self.y}, {self.z}, {self.w})'

    def __eq__(self, other: object) -> bool:
        '''Compares two Vector4s for equality.
        
        Returns:
            out (bool): True if both vectors are equal, False otherwise.
        '''
        if not isinstance(other, Vector4):
            return NotImplemented
        return self.x == other.x and self.y == other.y and self.z == other.z and self.w == other.w

    def __neg__(self) -> Vector4:
        '''Inverts all floats of the Vector4.

        Returns:
            out (Vector4): The result vector with inverted values.
        '''
        return Vector4(-self.x, -self.y, -self.z, -self.w)

    @overload
    def __add__(self, other: Vector4) -> Vector4: ...
    @overload
    def __add__(self, other: float) -> Vector4:
        '''Adds a floating point value to all values of a Vector4.

        Arguments:
            other (float): The floating point value.
        
        Returns:
            out (Vector4): The result vector.
        '''
        ...
    def __add__(self, other: Vector4 | float) -> Vector4:
        '''Adds values of two Vector4s.

        Arguments:
            other (Vector4): Another vector.
        
        Returns:
            out (Vector4): The result vector.
        '''
        if isinstance(other, Vector4):
            return Vector4(self.x + other.x, self.y + other.y, self.z + other.z, self.w + other.w)
        if isinstance(other, (float, int)):
            return Vector4(self.x + other, self.y + other, self.z + other, self.w + other)
        return NotImplemented

    @overload
    def __sub__(self, other: Vector4) -> Vector4: ...
    @overload
    def __sub__(self, other: float) -> Vector4:
        '''Subtracts a floating point value from all values of a Vector4.

        Arguments:
            other (float): The floating point value.
        
        Returns:
            out (Vector4): The result vector.
        '''
        ...
    def __sub__(self, other: Vector4 | float) -> Vector4:
        '''Subtracts values of two Vector4s.

        Arguments:
            other (Vector4): Another vector.
        
        Returns:
            out (Vector4): The result vector.
        '''
        if isinstance(other, Vector4):
            return Vector4(self.x - other.x, self.y - other.y, self.z - other.z, self.w - other.w)
        if isinstance(other, (float, int)):
            return Vector4(self.x - other, self.y - other, self.z - other, self.w - other)
        return NotImplemented

    @overload
    def __mul__(self, other: Vector4) -> Vector4: ...
    @overload
    def __mul__(self, other: float) -> Vector4:
        '''Multiplies all values of a Vector4 by a floating point value.

        Arguments:
            other (float): The floating point value.
        
        Returns:
            out (Vector4): The result vector.
        '''
        ...
    def __mul__(self, other: Vector4 | float) -> Vector4:
        '''Multiplies values of two Vector4s.

        Arguments:
            other (Vector4): Another vector.
        
        Returns:
            out (Vector4): The result vector.
        '''
        if isinstance(other, Vector4):
            return Vector4(self.x * other.x, self.y * other.y, self.z * other.z, self.w * other.w)
        if isinstance(other, (float, int)):
            return Vector4(self.x * other, self.y * other, self.z * other, self.w * other)
        return NotImplemented

    @overload
    def __truediv__(self, other: Vector4) -> Vector4: ...
    @overload
    def __truediv__(self, other: float) -> Vector4:
        '''Divides all values of a Vector4 by a floating point value.

        Arguments:
            other (float): The floating point value.
        
        Returns:
            out (Vector4): The result vector.
        '''
        ...
    def __truediv__(self, other: Vector4 | float) -> Vector4:
        '''Divides values of two Vector4s.

        Arguments:
            other (Vector4): Another vector.
        
        Returns:
            out (Vector4): The result vector.
        '''
        if isinstance(other, Vector4):
            return Vector4(self.x / other.x, self.y / other.y, self.z / other.z, self.w / other.w)
        if isinstance(other, (float, int)):
            return Vector4(self.x / other, self.y / other, self.z / other, self.w / other)
        return NotImplemented

    @overload
    def __iadd__(self, other: Vector4) -> Vector4: ...
    @overload
    def __iadd__(self, other: float) -> Vector4:
        '''Adds a floating point value to all values of the Vector4.

        Arguments:
            other (float): The floating point value.
        '''
        ...
    def __iadd__(self, other: Vector4 | float) -> Vector4:
        '''Adds values of one Vector4 to another.

        Arguments:
            other (Vector4): Another vector.
        '''
        if isinstance(other, Vector4):
            self.x += other.x
            self.y += other.y
            self.z += other.z
            self.w += other.w
            return self
        if isinstance(other, (float, int)):
            self.x += other
            self.y += other
            self.z += other
            self.w += other
            return self
        return NotImplemented

    @overload
    def __isub__(self, other: Vector4) -> Vector4: ...
    @overload
    def __isub__(self, other: float) -> Vector4:
        '''Subtracts a floating point value from all values of the Vector4.

        Arguments:
            other (float): The floating point value.
        '''
        ...
    def __isub__(self, other: Vector4 | float) -> Vector4:
        '''Subtracts values of one Vector4 from another.

        Arguments:
            other (Vector4): Another vector.
        '''
        if isinstance(other, Vector4):
            self.x -= other.x
            self.y -= other.y
            self.z -= other.z
            self.w -= other.w
            return self
        if isinstance(other, (float, int)):
            self.x -= other
            self.y -= other
            self.z -= other
            self.w -= other
            return self
        return NotImplemented

    @overload
    def __imul__(self, other: Vector4) -> Vector4: ...
    @overload
    def __imul__(self, other: float) -> Vector4:
        '''Multiplies all values of the Vector4 by a floating point value.

        Arguments:
            other (float): The floating point value.
        '''
        ...
    def __imul__(self, other: Vector4 | float) -> Vector4:
        '''Multiplies values of one Vector4 by another.

        Arguments:
            other (Vector4): Another vector.
        '''
        if isinstance(other, Vector4):
            self.x *= other.x
            self.y *= other.y
            self.z *= other.z
            self.w *= other.w
            return self
        if isinstance(other, (float, int)):
            self.x *= other
            self.y *= other
            self.z *= other
            self.w *= other
            return self
        return NotImplemented

    @overload
    def __itruediv__(self, other: Vector4) -> Vector4: ...
    @overload
    def __itruediv__(self, other: float) -> Vector4:
        '''Divides all values of the Vector4 by a floating point value.

        Arguments:
            other (float): The floating point value.
        '''
        ...
    def __itruediv__(self, other: Vector4 | float) -> Vector4:
        '''Divides values of one Vector4 by another.

        Arguments:
            other (Vector4): Another vector.
        '''
        if isinstance(other, Vector4):
            self.x /= other.x
            self.y /= other.y
            self.z /= other.z
            self.w /= other.w
            return self
        if isinstance(other, (float, int)):
            self.x /= other
            self.y /= other
            self.z /= other
            self.w /= other
            return self
        return NotImplemented

    __radd__ = __add__

    __rmul__ = __mul__

    def __rsub__(self, other: float) -> Vector4:
        '''Subtracts all values of the Vector4 from a floating point value.
        
        Arguments:
            other (float): The floating point value.
        '''
        if not isinstance(other, (float, int)):
            return NotImplemented
        return Vector4(other - self.x, other - self.y, other - self.z, other - self.w)

    def __rtruediv__(self, other: float) -> Vector4:
        '''Divides a floating point value by all values of the Vector4.

        Arguments:
            other (float): The floating point value.
        '''
        if isinstance(other, (float, int)):
            return Vector4(other / self.x, other / self.y, other / self.z, other / self.w)
        return NotImplemented

    ZERO: Vector4

Vector4.ZERO = Vector4()
