#!/usr/bin/env python3

'''Provides various Spore-related classes & functions of general use.'''

from __future__ import annotations

__author__ = '0KepOnline' # https://github.com/0KepOnline
__license__ = 'MIT' # see: "LICENSE"
__maintainer__ = '0KepOnline'
__email__ = 'i.am@scenariopla.net'




from datetime import datetime, timezone
from typing import Callable




# timestamps & everything related should stay here
class Timestamp(int):
    UNIX_Y1_DELTA: int = -62135683200
    UNIX_INSTANCE_ID_DELTA: int = 1104534000 # year 2005, US/Pacific

    @staticmethod
    def _get_timestamp() -> int:
        '''Gets the current UTC timestamp.

        Returns:
            out (int): The current Unix UTC timestamp.
        '''
        return int(datetime.now(timezone.utc).timestamp())

    def __new__(cls, value: int = _get_timestamp()):
        return super().__new__(cls, value)


    def year1(self) -> int:
        '''Gets the current UTC timestamp since the year 1.

        Returns:
            out (int): The current amount of seconds since the year 1.
        '''
        return self - Timestamp.UNIX_Y1_DELTA

    def instance_id(self) -> int:
        '''Gets the current Spore instance ID (timestamp since the year 2005 in US/Pacific).

        Returns:
            out (int): The current Spore instance ID.
        '''
        return self - Timestamp.UNIX_INSTANCE_ID_DELTA


# resource keys
class ResourceKey:
    '''A class that represents Spore resource key.

    Attributes:
        instance_id (int): The instance ID that is used to identify the object
            (file/some kind of inode). Generates a new from the current timestamp if not specified.
        type_id (int): The type (extension) ID.
        group_id (int): The group (folder) ID.
    '''
    def __init__(self,
                 instance_id: int | None | type = Timestamp,
                 type_id: int | None = 0,
                 group_id: int | None = 0) -> None:
        if instance_id is Timestamp:
            self.instance_id = Timestamp().instance_id()
        else:
            self.instance_id = instance_id if not isinstance(instance_id, type) else None
        self.type_id = type_id
        self.group_id = group_id

    # for basic syntax compatibility with ModAPI
    OVERFLOW: Callable[[int], int] = lambda value: value & 0xffffffff

    @property
    def instance_id(self) -> int:
        '''The instance ID that is used to identify the object (file/some kind of inode).'''
        return self._instance_id
    @instance_id.setter
    def instance_id(self, instance_id_modified: int | None) -> None:
        if instance_id_modified is None:
            instance_id_modified = 0
        self._instance_id = ResourceKey.OVERFLOW(instance_id_modified)

    @property
    def type_id(self) -> int:
        '''The type (extension) ID.'''
        return self._type_id
    @type_id.setter
    def type_id(self, type_id_modified: int | None) -> None:
        if type_id_modified is None:
            type_id_modified = 0
        self._type_id = ResourceKey.OVERFLOW(type_id_modified)

    @property
    def group_id(self) -> int:
        '''The group (folder) ID.'''
        return self._group_id
    @group_id.setter
    def group_id(self, group_id_modified: int | None) -> None:
        if group_id_modified is None:
            group_id_modified = 0
        self._group_id = ResourceKey.OVERFLOW(group_id_modified)

    def __str__(self) -> str:
        '''Gets a stringified resource key.
        
        Returns:
            out (str): The formatted resource key (group!instance.type).'''
        return (
            (f'0x{self.group_id:08x}!' if self.group_id != 0 else '')
            + (f'0x{self.instance_id:08x}')
            + (f'.0x{self.type_id:08x}' if self.type_id != 0 else '')
        )

    def __eq__(self, other: object) -> bool:
        '''Compares two resource keys for equality.
        
        Returns:
            out (bool): True if both resource keys are equal, False otherwise.
        '''
        if not isinstance(other, ResourceKey):
            return NotImplemented
        return (
            self.instance_id == other.instance_id
            and self.type_id == other.type_id
            and self.group_id == other.group_id
        )

    def __lt__(self, other: object) -> bool:
        '''Compares two resource keys for the first to be less than another.
        Starts to check with instance_id, then switches to type_id, and group_id in the order. 
        
        Returns:
            out (bool): True if the first resource key is less, False otherwise.'''
        if not isinstance(other, ResourceKey):
            return NotImplemented
        if self.instance_id == other.instance_id:
            if self.type_id == other.type_id:
                return self.group_id < other.group_id
            else:
                return self.type_id < other.type_id
        else:
            return self.instance_id < other.instance_id

    def __gt__(self, other: object) -> bool:
        '''Compares two resource keys for the first to be greater than another.
        Starts to check with instance_id, then switches to type_id, and group_id in the order. 
        
        Returns:
            out (bool): True if the first resource key is greater, False otherwise.'''
        if not isinstance(other, ResourceKey):
            return NotImplemented
        return other < self

    def with_instance(self, instance_id: int | None) -> ResourceKey:
        '''Creates a new resource key with the replaced instance ID.

        Arguments:
            instance_id (int | None): The instance ID to use.
        
        Returns:
            out (ResourceKey): The resource key with the new instance ID.
        '''
        return ResourceKey(instance_id, self.type_id, self.group_id)

    def with_type(self, type_id: int | None) -> ResourceKey:
        '''Creates a new resource key with the replaced type ID.
        
        Arguments:
            type_id (int | None): The type ID to use.
        
        Returns:
            out (ResourceKey): The resource key with the new type ID.
        '''
        return ResourceKey(self.instance_id, type_id, self.group_id)

    def with_group(self, group_id: int | None) -> ResourceKey:
        '''Creates a new resource key with the replaced group ID.
        
        Arguments:
            group_id (int | None): The group ID to use.
        
        Returns:
            out (ResourceKey): The resource key with the new group ID.
        '''
        return ResourceKey(self.instance_id, self.type_id, group_id)


# TODO: MathUtils.h structs, Transform, basic prop-related things, etc etc
