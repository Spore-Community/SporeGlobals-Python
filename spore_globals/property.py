#!/usr/bin/env python3

'''Serializes and deserializes Spore properties.'''

from __future__ import annotations




import struct
from enum import IntFlag
from functools import singledispatch
from typing import BinaryIO, get_args, get_origin
from fixedint import FixedInt, UInt8, UInt16, UInt32, Int8, Int16, Int32
from . import bbox
from . import color
from . import locale_key
from . import resource_key
from . import string
from . import text
from . import transform
from . import vector




# for * imports
BoundingBox = bbox.BoundingBox
ColorRGB = color.ColorRGB
ColorRGBA = color.ColorRGBA
LocaleKey = locale_key.LocaleKey
ResourceKey = resource_key.ResourceKey
String8 = string.String8
String16 = string.String16
Char8 = string.Char8
Char16 = string.Char16
Text = text.Text
Transform = transform.Transform
Vector2 = vector.Vector2
Vector3 = vector.Vector3
Vector4 = vector.Vector4

_PropertyBase = (bool
                 | Char8 | Char16
                 | String8 | String16
                 | Int8 | Int16 | Int32
                 | UInt8 | UInt16 | UInt32
                 | float
                 | ResourceKey
                 | Vector2 | Vector3 | Vector4
                 | ColorRGB | ColorRGBA)

Property = _PropertyBase | list[Text] | list[Transform] | list[BoundingBox] | list[_PropertyBase]

PropertyList = dict[UInt32, Property]

class _PropertyID(UInt16):
    '''A class that represesnts property IDs
    (`EA::Variant::eTypeId`/`SP::tExtraVariantTypes` in Feb2008 & `App::PropertyType` in ModAPI).
    '''

class _PropertySize(UInt32):
    '''A class that represesnts constant property size for serializing lists (arrays).
    All taken from SporeModder FX.
    '''

_PropertyType = tuple[_PropertyID, _PropertySize, bool, int] # id, size, be, padding if not in array

_TYPE_IDS_LENGTHS: dict[type, _PropertyType] = {
    # 0x0 = unidentified
    bool: (_PropertyID(0x1), _PropertySize(1), True, 0),
    Char8: (_PropertyID(0x2), _PropertySize(1), True, 0),
    Char16: (_PropertyID(0x3), _PropertySize(2), True, 0),
    #Char32: (_PropertyID(0x4), _PropertySize(4), True, 0),
    Int8: (_PropertyID(0x5), _PropertySize(1), True, 0),
    UInt8: (_PropertyID(0x6), _PropertySize(1), True, 0),
    Int16: (_PropertyID(0x7), _PropertySize(2), True, 0),
    UInt16: (_PropertyID(0x8), _PropertySize(2), True, 0),
    Int32: (_PropertyID(0x9), _PropertySize(4), True, 0),
    UInt32: (_PropertyID(0xa), _PropertySize(4), True, 0),
    #Int64: (_PropertyID(0xb), _PropertySize(8), True, 0),
    #UInt64: (_PropertyID(0xc), _PropertySize(8), True, 0),
    float: (_PropertyID(0xd), _PropertySize(4), True, 0),
    # 0xe = double
    # 0xf = pointer
    # 0x10 = void (???)
    # 0x11 = Object
    String8: (_PropertyID(0x12), _PropertySize(0x10), False, 0),
    String16: (_PropertyID(0x13), _PropertySize(0x10), False, 0),
    #String32: (_PropertyID(0x14), _PropertySize(0x10), False, 0),

    ResourceKey: (_PropertyID(0x20), _PropertySize(4+4+4), False, 4), # instance + type + group
    # 0x21 = flagset
    Text: (_PropertyID(0x22), _PropertySize(4+4+0x100), False, 0), # locale(i + t) + placeholder

    Vector2: (_PropertyID(0x30), _PropertySize(4+4), False, 8), # x + y
    Vector3: (_PropertyID(0x31), _PropertySize(4+4+4), False, 4), # x + y + z
    ColorRGB: (_PropertyID(0x32), _PropertySize(4+4+4), False, 4), # r + g + b
    Vector4: (_PropertyID(0x33), _PropertySize(4+4+4+4), False, 0), # x + y + z + w
    ColorRGBA: (_PropertyID(0x34), _PropertySize(4+4+4+4), False, 0), # r + g + b + a
    # 0x35 = Matrix2
    # 0x36 = Matrix3
    # 0x37 = Matrix4
    Transform: (_PropertyID(0x38), _PropertySize(2+2 + (4+4+4)+4+(4*3*3)), False, 0), #f+c+(o)+s+(r)
    BoundingBox: (_PropertyID(0x39), _PropertySize((4+4+4)+(4+4+4)), False, 0), # lower + upper
}

_IDS_TYPES: dict[int, type] = {int(k[0]): t for t, k in _TYPE_IDS_LENGTHS.items()}

class PropertyFlags(IntFlag):
    '''An enum with property flags. There are more (`EA::Variant::eFlags`), but those are unused.'''
    NORMAL = 0
    _TYPE_CONSTRUCT = 1
    _INVARIANT = 2
    _DESTRUCT = 4
    _CONSTRUCT = 8
    _C_ARRAY = 16
    _RAW_POINTER = 32
    _POINTER_PTR = 64

    ARRAY = _C_ARRAY | _RAW_POINTER




@singledispatch
def write(writable: Property, io: BinaryIO, big_endian: bool = False) -> None:
    '''Writes Spore property object (UInt8/16/32, Int8/16/32, float, bool, ColorRGB(A), String8/16,
    Char8/16, ResourceKey, Vector2/3/4, list[Text, Transform, BoundingBox + everything from above]).

    Arguments:
        writable (object): The writable property object.
        io (BinaryIO): The stream to write into.
        big_endian (bool): Should use big endian instead of litte. Default: False.
    
    Raises:
        TypeError: If the object can't be serialized as a Spore property.
    '''
    raise TypeError(f'{type(writable).__name__} is not a serializable Spore property.')

def _encode(writable: String8 | String16, big_endian: bool = False) -> bytes:
    '''Encodes a string with a possible endianness change.

    Arguments:
        writable (object): The writable property object.
        big_endian (bool): Should use big endian instead of litte. Default: False.
    
    Returns:
        out (bytes): The encoded strin.
    '''
    #TODO: maybe in a better way
    encoding: str = writable.encoding.replace('-le', '-be') if big_endian else writable.encoding
    return writable.encode(encoding)

def _validate_type(writable_type: type) -> _PropertyType:
    '''Checks if the type can be serialized. Should not be used with PropertyList & list.

    Arguments:
        writable_type (type): The type to serialize.
    
    Returns:
        out (_PropertyID, _PropertySize, bool, int): The desired property ID & size for this type.

    Raises:
        TypeError: If the type can't be serialized.
    '''
    try:
        property_type: _PropertyType = _TYPE_IDS_LENGTHS[writable_type]
    except KeyError:
        raise TypeError(f'{writable_type.__name__} is not a serializable Spore property.') from None
    return property_type


def _validate_array(writable: list) -> tuple[bool, _PropertyType | None]:
    '''Checks if the list can be serialized (contains only objects of one kind and is not empty).

    Arguments:
        writable (list): The list to serialize as an array.
    
    Returns:
        out (bool, (_PropertyID, _PropertySize, bool, int) | None): True and property ID & size if
                                                                    the list is not empty, False
                                                                    otherwise.

    Raises:
        TypeError: If the list contains non-serializable object types, or objects
                   of different kinds.
    '''
    if len({type(item) for item in writable}) > 1:
        typenames: str = ', '.join(sorted({type(item).__name__ for item in writable}))
        raise TypeError(f'List must have only one kind of objects, got: {typenames}.')
    if not writable:
        return (False, None)
    array_type: type = type(writable[0])
    property_type: _PropertyType = _validate_type(array_type)
    return (True, property_type)

# ints
@write.register
def _(writable: FixedInt, io: BinaryIO, big_endian: bool = False) -> None:
    io.write(writable.to_bytes(writable.width//8, 'little' if not big_endian else 'big'))
# bool
@write.register
def _(writable: bool, io: BinaryIO, big_endian: bool = False) -> None:
    io.write(b'\x01' if writable else b'\0')
# float
@write.register
def _(writable: float, io: BinaryIO, big_endian: bool = False) -> None:
    io.write(struct.pack('<f' if not big_endian else '>f', writable))
    #TODO: double??? for some reason smfx supports those in proplists
# char
@write.register
def _(writable: Char8 | Char16, io: BinaryIO, big_endian: bool = False) -> None:
    io.write(_encode(writable, big_endian))
# string
@write.register
def _(writable: String8 | String16, io: BinaryIO, big_endian: bool = False) -> None:
    str_bytes: bytes = _encode(writable, big_endian)
    write(UInt32(len(str_bytes) // (writable.width//8)), io, True)
    io.write(str_bytes)
# locale key
@write.register
def _(writable: LocaleKey, io: BinaryIO, big_endian: bool = False) -> None:
    write(writable.instance_id, io, big_endian)
    write(writable.table_id, io, big_endian)
# resource key
@write.register
def _(writable: ResourceKey, io: BinaryIO, big_endian: bool = False) -> None:
    write(writable.instance_id, io, big_endian)
    write(writable.type_id, io, big_endian)
    write(writable.group_id, io, big_endian)
# text
@write.register
def _(writable: Text, io: BinaryIO, big_endian: bool = False) -> None:
    write(writable.locale, io, big_endian)
    io.write(writable.placeholder.data)
# color
@write.register
def _(writable: ColorRGB | ColorRGBA, io: BinaryIO, big_endian: bool = False) -> None:
    write(writable.r, io, big_endian)
    write(writable.g, io, big_endian)
    write(writable.b, io, big_endian)
    if isinstance(writable, ColorRGBA):
        write(writable.a, io, big_endian)
# vector
@write.register
def _(writable: Vector2 | Vector3 | Vector4, io: BinaryIO, big_endian: bool = False) -> None:
    write(writable.x, io, big_endian)
    write(writable.y, io, big_endian)
    if isinstance(writable, Vector3 | Vector4):
        write(writable.z, io, big_endian)
        if isinstance(writable, Vector4):
            write(writable.w, io, big_endian)
# bbox
@write.register
def _(writable: BoundingBox, io: BinaryIO, big_endian: bool = False) -> None:
    write(writable.lower, io, big_endian)
    write(writable.upper, io, big_endian)
# transform
@write.register
def _(writable: Transform, io: BinaryIO, big_endian: bool = False) -> None:
    # pylint: disable=protected-access
    write(writable._flags, io, big_endian)
    write(writable._transform_count, io, big_endian)
    write(writable.offset, io, big_endian)
    write(writable.scale, io, big_endian)
    for row in writable.rotation.m:
        for value in row:
            write(float(value), io, big_endian)
# arrays
def _write_list(writable: list,
                io: BinaryIO,
                big_endian: bool = False,
                property_type: _PropertyType | None = None) -> None:
    if property_type is None:
        result: tuple[bool, _PropertyType | None] = _validate_array(writable)
        if not result[0]:
            return
        property_type = result[1]
    property_size: UInt32 = property_type[1]
    write(UInt32(len(writable)), io, True)
    write(property_size, io, True)
    for item in writable:
        write(item, io, big_endian)
@write.register
def _(writable: list, io: BinaryIO, big_endian: bool = False) -> None:
    _write_list(writable, io, big_endian)

def serialize(property_list: PropertyList, io: BinaryIO) -> None:
    '''Serializes a property list (.prop) of Spore into a binary IO.

    Arguments:
        property_list (PropertyList): The property list (dict[UInt32, Property]) to serialize.
        io (BinaryIO): The stream to write into.
    '''
    if not property_list:
        return
    write(UInt32(len(property_list)), io, True)
    for property_id, value in sorted(property_list.items()):
        flags: PropertyFlags = PropertyFlags.NORMAL
        property_type: _PropertyType
        is_list: bool = isinstance(value, list)
        if is_list:
            result: tuple[bool, _PropertyType | None] = _validate_array(value)
            if not result[0]:
                continue
            property_type = result[1]
            flags = PropertyFlags.ARRAY
        else:
            property_type = _validate_type(type(value))
        write(UInt32(property_id), io, True)
        write(property_type[0], io, True)
        write(UInt16(flags), io, True)
        if is_list:
            _write_list(value, io, property_type[2], property_type)
        else:
            write(value, io, property_type[2])
            io.write(bytes(property_type[3]))




@singledispatch
def _read(property_type: type, io: BinaryIO, big_endian: bool = False) -> Property:
    raise TypeError(f'{property_type.__name__} is not a deserializable Spore property.')

def read(property_type: type, io: BinaryIO, big_endian: bool = False) -> Property:
    '''Reads Spore property object (UInt8/16/32, Int8/16/32, float, bool, ColorRGB(A), String8/16,
    Char8/16, ResourceKey, Vector2/3/4, list[Text, Transform, BoundingBox + everything from above]).
 
    Arguments:
        property_type (type): The type of the property to read.
        io (BinaryIO): The stream to read from.
        big_endian (bool): Should use big endian instead of litte. Default: False.
 
    Returns:
        out (object): The property object of the desired type.
 
    Raises:
        TypeError: If the type can't be deserialized as a Spore property, or if property_type is set
                   to list with no explicit type specifying.
        EOFError: If the stream ended unexpectedly.
    '''
    return _read.dispatch(get_origin(property_type) or property_type)(property_type, io, big_endian)

def _read_exact(io: BinaryIO, size: int) -> bytes:
    '''Reads exactly n bytes.
 
    Arguments:
        io (BinaryIO): The stream to read from.
        size (int): The amount of bytes to read.
 
    Returns:
        out (bytes): The bytes read.
 
    Raises:
        EOFError: If the stream ended before.
    '''
    data: bytes = io.read(size)
    if len(data) != size:
        raise EOFError(f'Expected {size} bytes, got {len(data)}.')
    return data

def _decode(property_type: type[String8 | String16],
            data: bytes,
            big_endian: bool = False) -> String8 | String16:
    '''Decodes a string with a possible endianness change.
 
    Arguments:
        property_type (type): The string type (String8 | String16).
        data (bytes): The bytes to decode.
        big_endian (bool): Should use big endian instead of litte. Default: False.
 
    Returns:
        out (object): The decoded string.
    '''
    encoding: str = property_type().encoding
    if big_endian:
        #TODO: maybe in a better way
        encoding = encoding.replace('-le', '-be')
    return property_type(data.decode(encoding))

# ints
@_read.register(FixedInt)
def _(property_type: type[FixedInt], io: BinaryIO, big_endian: bool = False) -> FixedInt:
    return property_type(int.from_bytes(_read_exact(io, property_type.width//8),
                                        'little' if not big_endian else 'big'))
# bool
@_read.register(bool)
def _(property_type: type[bool], io: BinaryIO, big_endian: bool = False) -> bool:
    return _read_exact(io, 1) != b'\0'
# float
@_read.register(float)
def _(property_type: type[float], io: BinaryIO, big_endian: bool = False) -> float:
    return struct.unpack('<f' if not big_endian else '>f', _read_exact(io, 4))[0]
    #TODO: double??? for some reason smfx supports those in proplists
# char
@_read.register(Char8 | Char16)
def _(property_type: type[Char8 | Char16],
      io: BinaryIO,
      big_endian: bool = False) -> Char8 | Char16:
    return _decode(property_type, _read_exact(io, property_type.width//8), big_endian)
# string
@_read.register(String8 | String16)
def _(property_type: type[String8 | String16],
      io: BinaryIO,
      big_endian: bool = False) -> String8 | String16:
    length: UInt32 = read(UInt32, io, True)
    return _decode(property_type,
                   _read_exact(io, property_type.width//8 * int(length)),
                   big_endian)
# locale key
@_read.register(LocaleKey)
def _(property_type: type[LocaleKey], io: BinaryIO, big_endian: bool = False) -> LocaleKey:
    instance_id: UInt32 = read(UInt32, io, big_endian)
    table_id: UInt32 = read(UInt32, io, big_endian)
    return LocaleKey(instance_id, table_id)
# resource key
@_read.register(ResourceKey)
def _(property_type: type[ResourceKey], io: BinaryIO, big_endian: bool = False) -> ResourceKey:
    instance_id: UInt32 = read(UInt32, io, big_endian)
    type_id: UInt32 = read(UInt32, io, big_endian)
    group_id: UInt32 = read(UInt32, io, big_endian)
    return ResourceKey(instance_id, type_id, group_id)
# text
@_read.register(Text)
def _(property_type: type[Text], io: BinaryIO, big_endian: bool = False) -> Text:
    out: Text = Text(read(LocaleKey, io, big_endian))
    out.placeholder.data[:] = _read_exact(io, 0x100)
    return out
# color
@_read.register(ColorRGB | ColorRGBA)
def _(property_type: type[ColorRGB | ColorRGBA],
      io: BinaryIO,
      big_endian: bool = False) -> ColorRGB | ColorRGBA:
    r: float = read(float, io, big_endian)
    g: float = read(float, io, big_endian)
    b: float = read(float, io, big_endian)
    if issubclass(property_type, ColorRGBA):
        a: float = read(float, io, big_endian)
        return property_type(r, g, b, a)
    return property_type(r, g, b)
# vector
@_read.register(Vector2 | Vector3 | Vector4)
def _(property_type: type[Vector2 | Vector3 | Vector4],
      io: BinaryIO,
      big_endian: bool = False) -> Vector2 | Vector3 | Vector4:
    x: float = read(float, io, big_endian)
    y: float = read(float, io, big_endian)
    if not issubclass(property_type, Vector3 | Vector4):
        return property_type(x, y)
    z: float = read(float, io, big_endian)
    if not issubclass(property_type, Vector4):
        return property_type(x, y, z)
    w: float = read(float, io, big_endian)
    return property_type(x, y, z, w)
# bbox
@_read.register(BoundingBox)
def _(property_type: type[BoundingBox], io: BinaryIO, big_endian: bool = False) -> BoundingBox:
    lower: Vector3 = read(Vector3, io, big_endian)
    upper: Vector3 = read(Vector3, io, big_endian)
    return BoundingBox(lower, upper)
# transform
@_read.register(Transform)
def _(property_type: type[Transform], io: BinaryIO, big_endian: bool = False) -> Transform:
    # pylint: disable=protected-access
    out: Transform = Transform()
    flags: UInt16 = read(UInt16, io, big_endian)
    transform_count: UInt16 = read(UInt16, io, big_endian)
    out.offset = read(Vector3, io, big_endian)
    out.scale = read(float, io, big_endian)
    out.rotation.m = [[read(float, io, big_endian) for _ in range(3)] for _ in range(3)]

    out._flags = flags
    out._transform_count = transform_count
    return out
# arrays
@_read.register(list)
def _(property_type: type[list], io: BinaryIO, big_endian: bool = False) -> list:
    types: tuple = get_args(property_type)
    if len(types) != 1:
        raise TypeError('List item type must be given, e.g. list[UInt32].')
    array_property_type: type = types[0]
    _validate_type(array_property_type)
    count: UInt32 = read(UInt32, io, True)
    _property_size: UInt32 = read(UInt32, io, True) #TODO: compare with the dict?
    return [read(array_property_type, io, big_endian) for _ in range(int(count))]

def deserialize(io: BinaryIO) -> PropertyList:
    '''Deserializes a property list (.prop) of Spore from a binary IO.

    Arguments:
        io (BinaryIO): The stream to read from.

    Returns:
        out (PropertyList): The deserialized property list (dict[UInt32, Property]).

    Raises:
        TypeError: If an unknown property type ID is found (may happen to other Spark games even if
                   the .prop file is valid).
        EOFError: If the stream ended unexpectedly.
    '''
    property_list: PropertyList = {}
    first_byte: bytes = io.read(1)
    if not first_byte:
        #may happen to empty streams, those proplists aren't invalid in theory. just empty.
        return property_list
    property_count: UInt32 = UInt32(int.from_bytes(first_byte + _read_exact(io, 3), 'big'))
    for _ in range(property_count):
        property_id: UInt32 = read(UInt32, io, True)
        type_id: UInt16 = read(UInt16, io, True)
        flags: PropertyFlags = PropertyFlags(read(UInt16, io, True))
        try:
            value_type: type = _IDS_TYPES[type_id]
        except KeyError:
            raise TypeError(f'Unknown or unsupported property type ID: 0x{type_id:x}.') from None
        property_type: _PropertyType = _TYPE_IDS_LENGTHS[value_type]
        if (flags & PropertyFlags.ARRAY) == PropertyFlags.ARRAY: #smfx checks for ==, not (&) ==
            property_list[property_id] = read(list[value_type], io, property_type[2])
        else:
            property_list[property_id] = read(value_type, io, property_type[2])
            _read_exact(io, property_type[3])
    return property_list
