#!/usr/bin/env python3

'''Provides Spore resource keys.'''

from __future__ import annotations




from fixedint import UInt32
from .timestamp import Timestamp




class ResourceKey:
    '''A class that represents Spore resource key.

    Attributes:
        instance_id (UInt32): The instance ID that is used to identify the object
                              (file/some kind of inode). Generates a new from the current timestamp
                              if not specified.
        type_id (UInt32): The type (extension) ID.
        group_id (UInt32): The group (folder) ID.
    '''
    def __init__(self,
                 instance_id: UInt32 | int | None = Timestamp,
                 type_id: UInt32 | int | None = None,
                 group_id: UInt32 | int | None = None) -> None:
        if instance_id is Timestamp:
            self.instance_id = Timestamp().instance_id()
        else:
            self.instance_id = instance_id if not isinstance(instance_id, type) else None
        self.type_id = type_id
        self.group_id = group_id

    @property
    def instance_id(self) -> UInt32:
        '''The instance ID that is used to identify the object (file/some kind of inode).'''
        return self._instance_id
    @instance_id.setter
    def instance_id(self, instance_id_modified: UInt32 | int | None) -> None:
        self._instance_id = UInt32(instance_id_modified if instance_id_modified is not None else 0)

    @property
    def type_id(self) -> UInt32:
        '''The type (extension) ID.'''
        return self._type_id
    @type_id.setter
    def type_id(self, type_id_modified: UInt32 | int | None) -> None:
        self._type_id = UInt32(type_id_modified if type_id_modified is not None else 0)

    @property
    def group_id(self) -> UInt32:
        '''The group (folder) ID.'''
        return self._group_id
    @group_id.setter
    def group_id(self, group_id_modified: UInt32 | int | None) -> None:
        self._group_id = UInt32(group_id_modified if group_id_modified is not None else 0)

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

    def with_instance(self, instance_id: UInt32 | int | None) -> ResourceKey:
        '''Creates a new resource key with the replaced instance ID.

        Arguments:
            instance_id (UInt32 | None): The instance ID to use.
        
        Returns:
            out (ResourceKey): The resource key with the new instance ID.
        '''
        return ResourceKey(instance_id, self.type_id, self.group_id)

    def with_type(self, type_id: UInt32 | int | None) -> ResourceKey:
        '''Creates a new resource key with the replaced type ID.
        
        Arguments:
            type_id (UInt32 | None): The type ID to use.
        
        Returns:
            out (ResourceKey): The resource key with the new type ID.
        '''
        return ResourceKey(self.instance_id, type_id, self.group_id)

    def with_group(self, group_id: UInt32 | int | None) -> ResourceKey:
        '''Creates a new resource key with the replaced group ID.
        
        Arguments:
            group_id (UInt32 | None): The group ID to use.
        
        Returns:
            out (ResourceKey): The resource key with the new group ID.
        '''
        return ResourceKey(self.instance_id, self.type_id, group_id)
