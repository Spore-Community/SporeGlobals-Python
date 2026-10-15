#!/usr/bin/env python3

'''Provides Spore color properties.'''

from __future__ import annotations




from typing import overload
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
                Color._set_byteshift(UInt8(a if a is not None else UInt8.maxval), 3)
                | Color._set_byteshift(UInt8(value_r), 2)
                | Color._set_byteshift(UInt8(g), 1)
                | Color._set_byteshift(UInt8(b), 0)
            )

    @staticmethod
    def _get_byteshift(value: UInt32, shift: int) -> UInt8:
        '''Gets a color channel value by a byteshift.
        
        Arguments:
            value (UInt32): The initial ARGB color value.
            shift (int): The amount of bytes to shift.
        
        Returns:
            out (UInt8): The result color channel value.
        '''
        return UInt8(value >> shift*8)

    @staticmethod
    def _set_byteshift(value: UInt8, shift: int) -> UInt32:
        '''Sets a color channel value by a byteshift.
        
        Arguments:
            value (UInt32): The initial color channel value.
            shift (int): The amount of bytes to shift.
        
        Returns:
            out (UInt8): The result ARGB color value.
        '''
        return UInt32(int(value) << shift*8)

    @property
    def a(self) -> UInt8:
        '''The alpha value.'''
        return UInt8(Color._get_byteshift(self.value, 3))
    @a.setter
    def a(self, a_modified: UInt8 | int | None) -> None:
        if not isinstance(a_modified, UInt8):
            a_modified = UInt8(a_modified if a_modified is not None else 0)
        self.value = UInt32((self.value & 0x00ffffff) | Color._set_byteshift(a_modified, 3))

    @property
    def r(self) -> UInt8:
        '''The red color value.'''
        return UInt8(Color._get_byteshift(self.value, 2))
    @r.setter
    def r(self, r_modified: UInt8 | int | None) -> None:
        if not isinstance(r_modified, UInt8):
            r_modified = UInt8(r_modified if r_modified is not None else 0)
        self.value = UInt32((self.value & 0xff00ffff) | Color._set_byteshift(r_modified, 2))

    @property
    def g(self) -> UInt8:
        '''The green color value.'''
        return UInt8(Color._get_byteshift(self.value, 1))
    @g.setter
    def g(self, g_modified: UInt8 | int | None) -> None:
        if not isinstance(g_modified, UInt8):
            g_modified = UInt8(g_modified if g_modified is not None else 0)
        self.value = UInt32((self.value & 0xffff00ff) | Color._set_byteshift(g_modified, 1))

    @property
    def b(self) -> UInt8:
        '''The blue color value.'''
        return UInt8(Color._get_byteshift(self.value, 0))
    @b.setter
    def b(self, b_modified: UInt8 | int | None) -> None:
        if not isinstance(b_modified, UInt8):
            b_modified = UInt8(b_modified if b_modified is not None else 0)
        self.value = UInt32((self.value & 0xffffff00) | b_modified)

    @property
    def value(self) -> UInt32:
        '''The ARGB color value.'''
        return self._value
    @value.setter
    def value(self, value_modified: UInt32 | int | None) -> None:
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




def _float_to_byte(value: float) -> UInt8:
    '''Converts a 0.0-1.0 floating point value to a 0-255 byte with clamping.
    
    Arguments:
        value (float): The value to convert.
    
    Returns:
        out (UInt8): The resulting byte.
    '''
    return UInt8(round(max(0, min(value, 1.0)) * UInt8.maxval))




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
            self.r = r_color.r / UInt8.maxval
            self.g = r_color.g / UInt8.maxval
            self.b = r_color.b / UInt8.maxval
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
        return Color(_float_to_byte(self.r),
                     _float_to_byte(self.g),
                     _float_to_byte(self.b),
                     UInt8.maxval)

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
            self.a = r_color.a / UInt8.maxval
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
        '''Converts to the 8-bit ARGB color.'''
        return Color(_float_to_byte(self.r),
                     _float_to_byte(self.g),
                     _float_to_byte(self.b),
                     _float_to_byte(self.a))

    def __str__(self) -> str:
        '''Gets a stringified RGBA color.
        
        Returns:
            out (str): The formatted RGBA color (r, g, b, a).'''
        return f'({self.r}, {self.g}, {self.b}, {self.a})'

# TODO: ColorHSV and related functions
