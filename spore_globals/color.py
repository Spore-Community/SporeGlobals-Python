#!/usr/bin/env python3

'''Provides Spore color properties.'''

from __future__ import annotations




from typing import Callable, overload
from fixedint import UInt8, UInt32




class Color:
    '''A class that represents Spore ARGB 8-bit colors.

    Attributes:
        r (UInt8): The red color value.
        g (UInt8): The green color value.
        b (UInt8): The blue color value.
        a (UInt8): The alpha value.
        value (UInt32): The ARGB color value.
    '''
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, value: UInt32 | int) -> None: ...
    @overload
    def __init__(self, r: UInt8 | int, g: UInt8 | int, b: UInt8 | int, a: UInt8 | int) -> None: ...
    def __init__(self,
                 value_r: UInt32 | UInt8 | int = 0,
                 g: UInt8 | int | None = None,
                 b: UInt8 | int | None = None,
                 a: UInt8 | int | None = None) -> None:
        if g is None:
            self.value = value_r
        else:
            self._value: UInt32 = UInt32(
                Color.BYTESHIFT_SET(a, 3)
                | Color.BYTESHIFT_SET(value_r, 2)
                | Color.BYTESHIFT_SET(g, 1)
                | Color.BYTESHIFT_SET(b, 0)
            )

    BYTESHIFT_GET: Callable[[int, int], int] = lambda value, shift: (value >> shift*8) & 0xff
    BYTESHIFT_SET: Callable[[int, int], int] = lambda value, shift: (value & 0xff) << shift*8

    @property
    def a(self) -> UInt8:
        '''The alpha value.'''
        return UInt8(Color.BYTESHIFT_GET(self.value, 3))
    @a.setter
    def a(self, a_modified: UInt8 | None) -> None:
        if a_modified is None:
            a_modified = 0
        self.value = UInt32((self.value & 0x00ffffff) | Color.BYTESHIFT_SET(a_modified, 3))

    @property
    def r(self) -> UInt8:
        '''The red color value.'''
        return UInt8(Color.BYTESHIFT_GET(self.value, 2))
    @r.setter
    def r(self, r_modified: UInt8 | None) -> None:
        if r_modified is None:
            r_modified = 0
        self.value = UInt32((self.value & 0xff00ffff) | Color.BYTESHIFT_SET(r_modified, 2))

    @property
    def g(self) -> UInt8:
        '''The green color value.'''
        return UInt8(Color.BYTESHIFT_GET(self.value, 1))
    @g.setter
    def g(self, g_modified: UInt8 | None) -> None:
        if g_modified is None:
            g_modified = 0
        self.value = UInt32((self.value & 0xffff00ff) | Color.BYTESHIFT_SET(g_modified, 1))

    @property
    def b(self) -> UInt8:
        '''The blue color value.'''
        return UInt8(Color.BYTESHIFT_GET(self.value, 0))
    @b.setter
    def b(self, b_modified: UInt8 | None) -> None:
        if b_modified is None:
            b_modified = 0
        self.value = UInt32((self.value & 0xffffff00) | Color.BYTESHIFT_SET(b_modified, 0))

    @property
    def value(self) -> UInt32:
        '''The ARGB color value.'''
        return self._value
    @value.setter
    def value(self, value_modified: UInt32 | None) -> None:
        self._value = UInt32(value_modified if value_modified is not None else 0)

    def __eq__(self, other: object) -> bool:
        '''Compares two colors for equality.
        
        Returns:
            out (bool): True if both colors are equal, False otherwise.
        '''
        if not isinstance(other, Color):
            return NotImplemented
        return self.value == other.value

    def __str__(self) -> str:
        '''Gets a stringified color.
        
        Returns:
            out (str): The formatted color (r, g, b, a: hexadecimal value).'''
        return f'({self.r}, {self.g}, {self.b}, {self.a}: 0x{self.value:08x})'

    def __add__(self, other: Color) -> Color:
        '''Adds values of two colors.
        
        Returns:
            out (Color): The result color.
        '''
        if not isinstance(other, Color):
            return NotImplemented
        return Color(self.value + other.value)

    def __sub__(self, other: Color) -> Color:
        '''Subtracts values of two colors.
        
        Returns:
            out (Color): The result color.
        '''
        if not isinstance(other, Color):
            return NotImplemented
        return Color(self.value - other.value)

    def __iadd__(self, other: Color) -> Color:
        '''Adds the value of one color to another.'''
        if not isinstance(other, Color):
            return NotImplemented
        self.value += other.value
        return self

    def __isub__(self, other: Color) -> Color:
        '''Subtracts the value of one color from another.'''
        if not isinstance(other, Color):
            return NotImplemented
        self.value -= other.value
        return self

    RED: Color
    BLUE: Color
    GREEN: Color
    WHITE: Color
    BLACK: Color

Color.RED = Color(255, 0, 0, 255)
Color.BLUE = Color(0, 0, 255, 255)
Color.GREEN = Color(0, 255, 0, 255)
Color.WHITE = Color(255, 255, 255, 255)
Color.BLACK = Color(0, 0, 0, 255)




class ColorRGB:
    '''A class that represents Spore RGB float colors.

    Attributes:
        r (float): The red color value (0.0-1.0).
        g (float): The green color value (0.0-1.0).
        b (float): The blue color value (0.0-1.0).
    '''
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, color: Color) -> None: ...
    @overload
    def __init__(self,
                 r: float | None,
                 g: float | None,
                 b: float | None) -> None: ...
    def __init__(self,
                 r_color: float | Color | None = None,
                 g: float | None = None,
                 b: float | None = None) -> None:
        if isinstance(r_color, Color):
            self.r = r_color.r / 0xff
            self.g = r_color.g / 0xff
            self.b = r_color.b / 0xff
        else:
            self.r = r_color
            self.g = g
            self.b = b

    @property
    def r(self) -> float:
        '''The red color value (0.0-1.0).'''
        return self._r
    @r.setter
    def r(self, r_modified: float | None) -> None:
        self._r: float = float(r_modified) if r_modified is not None else 0

    @property
    def g(self) -> float:
        '''The green color value (0.0-1.0).'''
        return self._g
    @g.setter
    def g(self, g_modified: float | None) -> None:
        self._g: float = float(g_modified) if g_modified is not None else 0

    @property
    def b(self) -> float:
        '''The blue color value (0.0-1.0).'''
        return self._b
    @b.setter
    def b(self, b_modified: float | None) -> None:
        self._b: float = float(b_modified) if b_modified is not None else 0

    def to_int_color(self) -> Color:
        '''Converts to the 8-bit ARGB color.'''
        return Color(round(self.r * 0xff), round(self.g * 0xff), round(self.b * 0xff), 0xff)

    def __str__(self) -> str:
        '''Gets a stringified RGB color.
        
        Returns:
            out (str): The formatted RGB color (r, g, b).'''
        return f'({self.r}, {self.g}, {self.b})'

    def __eq__(self, other: object) -> bool:
        '''Compares two float colors for equality. 
        
        Returns:
            out (bool): True if both colors are equal, False otherwise.
        '''
        if not isinstance(other, ColorRGB):
            return NotImplemented
        self_a: float = self.a if isinstance(self, ColorRGBA) else 1.0
        other_a: float = other.a if isinstance(other, ColorRGBA) else 1.0
        return (
            self.r == other.r
            and self.g == other.g
            and self.b == other.b
            and self_a == other_a
        )




class ColorRGBA(ColorRGB):
    '''A class that represents Spore RGBA float colors.

    Attributes:
        r (float): The red color value (0.0-1.0).
        g (float): The green color value (0.0-1.0).
        b (float): The blue color value (0.0-1.0).
        a (float): The alpha value (0.0-1.0).
    '''
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, color: Color) -> None: ...
    @overload
    def __init__(self, color: ColorRGB, a: float | None) -> None: ...
    @overload
    def __init__(self,
                 r: float | None,
                 g: float | None,
                 b: float | None,
                 a: float | None) -> None: ...
    def __init__(self,
                 r_color: float | Color | None = None,
                 g_a: float | None = None,
                 b: float | None = None,
                 a: float | None = None) -> None:
        if isinstance(r_color, Color):
            super().__init__(r_color)
            self.a = r_color.a / 0xff
        elif isinstance(r_color, ColorRGB):
            super().__init__(r_color.r, r_color.g, r_color.b)
            self.a = g_a
        else:
            super().__init__(r_color, g_a, b)
            self.a = a

    @property
    def a(self) -> float:
        '''The alpha value (0.0-1.0).'''
        return self._a
    @a.setter
    def a(self, a_modified: float | None) -> None:
        self._a: float = float(a_modified) if a_modified is not None else 0

    def to_int_color(self) -> Color:
        color: Color = super().to_int_color()
        color.a = round(self.a * 0xff)
        return color

    def __str__(self) -> str:
        '''Gets a stringified RGBA color.
        
        Returns:
            out (str): The formatted RGBA color (r, g, b, a).'''
        return f'({self.r}, {self.g}, {self.b}, {self.a})'

# TODO: ColorHSV and related functions
