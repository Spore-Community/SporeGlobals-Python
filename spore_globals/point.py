#!/usr/bin/env python3

'''Provides Spore 2D points with coordinates.'''

from __future__ import annotations




from typing import overload, TYPE_CHECKING
if TYPE_CHECKING:
    from .vector import Vector2




class Point:
    '''A class that represents Spore 2D point with two floating point coordinates (X, Y).

    Attributes:
        x (float): The abscissa (X) value.
        y (float): The ordinate (Y) value.
    '''
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, vector: Vector2) -> None: ...
    @overload
    def __init__(self, x: float, y: float) -> None: ...
    def __init__(self,
                 x_vector: float | Vector2 | None = None,
                 y: float | None = None) -> None:
        from .vector import Vector2 # pylint: disable=import-outside-toplevel
        if isinstance(x_vector, Vector2):
            self.x = x_vector.x
            self.y = x_vector.y
        else:
            self.x = x_vector
            self.y = y

    @property
    def x(self) -> float:
        '''The abscissa (X) value.'''
        return self._x
    @x.setter
    def x(self, x_modified: float | None) -> None:
        self._x: float = x_modified if x_modified is not None else 0

    @property
    def y(self) -> float:
        '''The ordinate (Y) value.'''
        return self._y
    @y.setter
    def y(self, y_modified: float | None) -> None:
        self._y: float = y_modified if y_modified is not None else 0

    def __str__(self) -> str:
        '''Gets a stringified 2D point.
        
        Returns:
            out (str): The formatted point (x, y).'''
        return f'({self.x}, {self.y})'

    def __eq__(self, other: object) -> bool:
        '''Compares two 2D points for equality.
        
        Returns:
            out (bool): True if both points are equal, False otherwise.
        '''
        if not isinstance(other, Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __neg__(self) -> Point:
        '''Inverts both coordinates of the Point.

        Returns:
            out (Point): The result point with inverted coordinates.
        '''
        return Point(-self.x, -self.y)

    @overload
    def __add__(self, other: Point) -> Point: ...
    @overload
    def __add__(self, other: float) -> Point:
        '''Adds a floating point value to both coordinates of a Point.

        Arguments:
            other (float): The floating point value.
        
        Returns:
            out (Point): The result point.
        '''
        ...
    def __add__(self, other: Point | float) -> Point:
        '''Adds coordinates of two points.

        Arguments:
            other (Point): Another point.
        
        Returns:
            out (Point): The result point.
        '''
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        if isinstance(other, (float, int)):
            return Point(self.x + other, self.y + other)
        return NotImplemented

    @overload
    def __sub__(self, other: Point) -> Point: ...
    @overload
    def __sub__(self, other: float) -> Point:
        '''Subtracts a floating point value from both coordinates of a Point.

        Arguments:
            other (float): The floating point value.
        
        Returns:
            out (Point): The result point.
        '''
        ...
    def __sub__(self, other: Point | float) -> Point:
        '''Subtracts coordinates of two points.

        Arguments:
            other (Point): Another point.
        
        Returns:
            out (Point): The result point.
        '''
        if isinstance(other, Point):
            return Point(self.x - other.x, self.y - other.y)
        if isinstance(other, (float, int)):
            return Point(self.x - other, self.y - other)
        return NotImplemented

    @overload
    def __mul__(self, other: Point) -> Point: ...
    @overload
    def __mul__(self, other: float) -> Point:
        '''Multiplies both coordinates of a Point by a floating point value.

        Arguments:
            other (float): The floating point value.
        
        Returns:
            out (Point): The result point.
        '''
        ...
    def __mul__(self, other: Point | float) -> Point:
        '''Multiplies coordinates of two points.

        Arguments:
            other (Point): Another point.
        
        Returns:
            out (Point): The result point.
        '''
        if isinstance(other, Point):
            return Point(self.x * other.x, self.y * other.y)
        if isinstance(other, (float, int)):
            return Point(self.x * other, self.y * other)
        return NotImplemented

    @overload
    def __truediv__(self, other: Point) -> Point: ...
    @overload
    def __truediv__(self, other: float) -> Point:
        '''Divides both coordinates of a Point by a floating point value.

        Arguments:
            other (float): The floating point value.
        
        Returns:
            out (Point): The result point.
        '''
        ...
    def __truediv__(self, other: Point | float) -> Point:
        '''Divides coordinates of two points.

        Arguments:
            other (Point): Another point.
        
        Returns:
            out (Point): The result point.
        '''
        if isinstance(other, Point):
            return Point(self.x / other.x, self.y / other.y)
        if isinstance(other, (float, int)):
            return Point(self.x / other, self.y / other)
        return NotImplemented

    @overload
    def __iadd__(self, other: Point) -> Point: ...
    @overload
    def __iadd__(self, other: float) -> Point:
        '''Adds a floating point value to both coordinates of the Point.

        Arguments:
            other (float): The floating point value.
        '''
        ...
    def __iadd__(self, other: Point | float) -> Point:
        '''Adds coordinates of one point to another.

        Arguments:
            other (Point): Another point.
        '''
        if isinstance(other, Point):
            self.x += other.x
            self.y += other.y
            return self
        if isinstance(other, (float, int)):
            self.x += other
            self.y += other
            return self
        return NotImplemented

    @overload
    def __isub__(self, other: Point) -> Point: ...
    @overload
    def __isub__(self, other: float) -> Point:
        '''Subtracts a floating point value from both coordinates of the Point.

        Arguments:
            other (float): The floating point value.
        '''
        ...
    def __isub__(self, other: Point | float) -> Point:
        '''Subtracts coordinates of one point from another.

        Arguments:
            other (Point): Another point.
        '''
        if isinstance(other, Point):
            self.x -= other.x
            self.y -= other.y
            return self
        if isinstance(other, (float, int)):
            self.x -= other
            self.y -= other
            return self
        return NotImplemented

    @overload
    def __imul__(self, other: Point) -> Point: ...
    @overload
    def __imul__(self, other: float) -> Point:
        '''Multiplies both coordinates of the Point by a floating point value.

        Arguments:
            other (float): The floating point value.
        '''
        ...
    def __imul__(self, other: Point | float) -> Point:
        '''Multiplies coordinates of one point by another.

        Arguments:
            other (Point): Another point.
        '''
        if isinstance(other, Point):
            self.x *= other.x
            self.y *= other.y
            return self
        if isinstance(other, (float, int)):
            self.x *= other
            self.y *= other
            return self
        return NotImplemented

    @overload
    def __itruediv__(self, other: Point) -> Point: ...
    @overload
    def __itruediv__(self, other: float) -> Point:
        '''Divides both coordinates of the Point by a floating point value.

        Arguments:
            other (float): The floating point value.
        '''
        ...
    def __itruediv__(self, other: Point | float) -> Point:
        '''Divides coordinates of one point by another.
        
        Arguments:
            other (Point): Another point.
        '''
        if isinstance(other, Point):
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

    def __rsub__(self, other: float) -> Point:
        '''Subtracts both coordinates of the Point from a floating point value.
        
        Arguments:
            other (float): The floating point value.
        '''
        if not isinstance(other, (float, int)):
            return NotImplemented
        return Point(other - self.x, other - self.y)

    def __rtruediv__(self, other: float) -> Point:
        '''Divides a floating point value by both coordinates of the Point.

        Arguments:
            other (float): The floating point value.
        '''
        if isinstance(other, (float, int)):
            return Point(other / self.x, other / self.y)
        return NotImplemented
    