#!/usr/bin/env python3

'''Provides C-like fixed strings of a certain size.'''

from __future__ import annotations




from collections import UserString
from typing import ClassVar, overload
from fixedint import UInt8, UInt16, UInt32




def _validate_char(instance: _IStringFixed) -> None:
    '''Validates a character type of some fixed size.

    Raises:
        ValueError: If the length isn't 1.
    '''
    length: int = len(instance.encode(instance.encoding))
    if length != instance.width // 8:
        raise ValueError(f'{type(instance).__name__} needs exactly 1 char, got {length}.')

class _IStringFixed(UserString):
    '''A private interface that is used for strings of a fixed character size.'''
    encoding: ClassVar[str]
    '''The encoding used for this string.'''
    width: ClassVar[int] = 8
    '''The width in bits.'''

    _locked: bool = False
    _terminate: bool = True

    def __init_subclass__(cls) -> None:
        if _IStringFixed._locked:
            raise TypeError('This interface can\'t be used outside of the module.')

    def __init__(self,
                 value: str
                        | bytes
                        | bytearray
                        | UInt8
                        | UInt16
                        | int
                        | list[UInt8]
                        | list[UInt16]
                        | list[int] = '') -> None:
        if isinstance(value, int):
            value = chr(value)
        elif isinstance(value, list):
            value = ''.join(map(chr, value))
        elif isinstance(value, bytes | bytearray):
            value = bytes(value).decode(self.encoding, 'replace')
        value = str(value).encode(self.encoding, 'replace').decode(self.encoding)
        if self._terminate:
            value = value.split('\0', 1)[0]
        super().__init__(value)




class String8(_IStringFixed):
    '''A class that represents a typical C-like "string".
    
    Attributes:
        width (int) = 8: The width in bits.
    '''
    encoding = 'latin-1'
    width = 8

    @overload
    def __getitem__(self, index: int) -> Char8: ...
    @overload
    def __getitem__(self, index: slice) -> String8: ...
    def __getitem__(self, index: int | slice) -> Char8 | String8:
        out: str = self.data[index]
        return Char8(out) if isinstance(index, int) else String8(out)

String = String8




class String16(_IStringFixed):
    '''A class that represents a typical C-like "string16".
    
    Attributes:
        width (int) = 16: The width in bits.'''
    encoding = 'utf-16-le'
    width = 16

    @overload
    def __getitem__(self, index: int) -> Char16: ...
    @overload
    def __getitem__(self, index: slice) -> String16: ...
    def __getitem__(self, index: int | slice) -> Char16 | String16:
        out: str = self.data[index]
        return Char16(out) if isinstance(index, int) else String16(out)

WString = String16




class String32(_IStringFixed):
    '''A class that represents a typical C-like "string32" (not present in EASTL though).
    
    Attributes:
        width (int) = 32: The width in bits.'''
    encoding = 'utf-32-le'
    width = 32

    @overload
    def __getitem__(self, index: int) -> Char32: ...
    @overload
    def __getitem__(self, index: slice) -> String32: ...
    def __getitem__(self, index: int | slice) -> Char32 | String32:
        out: str = self.data[index]
        return Char32(out) if isinstance(index, int) else String32(out)




class Char8(String8):
    '''A class that represents a typical C-like 1-byte character.
    
    Attributes:
        width (int) = 8: The width in bits.
    '''
    _terminate = False
    def __init__(self, value: String8 | str | bytes | bytearray | UInt8 | int = '\0') -> None:
        super().__init__(value)
        _validate_char(self)

    def __int__(self) -> int:
        '''Converts the character to its 8-bit numeric code.

        Returns:
            out (int): The code of the character (0-255).
        '''
        return ord(self.data)

Char = Char8




class Char16(String16):
    '''A class that represents a typical C-like 2-byte wide character.
    
    Attributes:
        width (int) = 16: The width in bits.
    '''
    _terminate = False
    def __init__(self, value: String16 | str | bytes | bytearray | UInt16 | int = '\0') -> None:
        super().__init__(value)
        _validate_char(self)

    def __int__(self) -> int:
        '''Converts the character to its 16-bit numeric code.

        Returns:
            out (int): The code of the wide character (0-65535).
        '''
        return ord(self.data)

WChar = Char16




class Char32(String32):
    '''A class that represents a typical C-like 4-byte unicode character.
    
    Attributes:
        width (int) = 32: The width in bits.
    '''
    _terminate = False
    def __init__(self, value: String32 | str | bytes | bytearray | UInt32 | int = '\0') -> None:
        super().__init__(value)
        _validate_char(self)

    def __int__(self) -> int:
        '''Converts the character to its 32-bit numeric code.

        Returns:
            out (int): The code of the unicode character (0-1114111).
        '''
        return ord(self.data)




_IStringFixed._locked = True # pylint: disable=protected-access
