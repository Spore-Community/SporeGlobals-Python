#!/usr/bin/env python3

'''Provides FNV1-32 hashing algorithm which is used for hashing Spore names.'''




from typing import Final
from fixedint import UInt32
from .string import String8, String16, String32
from .text import Text




FNV1_OFFSET: Final[UInt32] = UInt32(0x811c9dc5)
FNV1_PRIME: Final[UInt32] = UInt32(0x1000193)
FNV1_MASK: Final[UInt32] = UInt32(UInt32.maxval)

def fnv1(data: str | String8 | String16 | String32 | Text.String16Placeholder | bytes | bytearray,
         lowercase: bool = True,
         offset: UInt32 | int = FNV1_OFFSET,
         prime: UInt32 | int = FNV1_PRIME,
         mask: UInt32 | int = FNV1_MASK) -> UInt32:
    '''Hashes the input with the FNV1-32 algorithm. Strings get encoded with UTF-16 first.
    
    Arguments:
        data (str | String8 | String16 | String32 | Text.String16Placeholder | bytes | bytearray):
            The input data to encode.
        lowercase (bool): Should the string be lowercased or not (doesn't affect bytes/bytearray).
                          Default: True.
        offset (UInt32 | int): The value offset. Default: 0x811c9dc5.
        prime (UInt32 | int): The prime value. Default: 0x1000193.
        mask (UInt32 | int): The mask to use. Default: 0xffffffff.
    
    Returns:
        out (UInt32): The hashed result.
    '''
    if isinstance(data, str | String8 | String16 | String32 | Text.String16Placeholder):
        data_str: str = str(data)
        # strings are hashed by two bytes per char instead of one
        data = memoryview((data_str.lower() if lowercase else data_str)
                          .encode('utf-16', 'surrogatepass')).cast('H')[1:] #bom marker
    out: int = int(offset)
    prime = int(prime)
    mask = int(mask)
    for byte in data:
        out = (out * prime) & mask ^ byte
    return UInt32(out)
