#!/usr/bin/env python3

'''Provides Spore locale keys (similar to resource keys, but with a pair of u32 fields).'''

from __future__ import annotations




from fixedint import UInt32




class LocaleKey:
    '''A class that represents Spore locale key.

    Attributes:
        instance_id (UInt32): The instance ID that is used to identify the line in the table.
        table_id (UInt32): The table (.locale file) ID.
    '''
    def __init__(self,
                 instance_id: UInt32 | int | None = None,
                 table_id: UInt32 | int | None = None) -> None:
        self.instance_id = instance_id
        self.table_id = table_id

    @property
    def instance_id(self) -> UInt32:
        '''The instance ID that is used to identify the line in the table.'''
        return self._instance_id
    @instance_id.setter
    def instance_id(self, instance_id_modified: UInt32 | int | None) -> None:
        self._instance_id = UInt32(instance_id_modified if instance_id_modified is not None else 0)

    @property
    def table_id(self) -> UInt32:
        '''The table (.locale file) ID.'''
        return self._table_id
    @table_id.setter
    def table_id(self, table_id_modified: UInt32 | int | None) -> None:
        self._table_id = UInt32(table_id_modified if table_id_modified is not None else 0)

    def __str__(self) -> str:
        '''Gets a stringified locale key.
        
        Returns:
            out (str): The formatted locale key (table!instance).
        '''
        return f'0x{self.table_id:08x}!0x{self.instance_id:08x}'

    def __eq__(self, other: object) -> bool:
        '''Compares two locale keys for equality.
        
        Returns:
            out (bool): True if both locale keys are equal, False otherwise.
        '''
        if not isinstance(other, LocaleKey):
            return NotImplemented
        return self.instance_id == other.instance_id and self.table_id == other.table_id

    def __hash__(self) -> int:
        '''Gets the hash of the locale key.
        
        Returns:
            out (int): The hash of the key.
        '''
        return hash((self.instance_id, self.table_id))

    def __lt__(self, other: object) -> bool:
        '''Compares two locale keys for the first to be less than another.
        Starts to check with instance_id, then switches to table_id. 
        
        Returns:
            out (bool): True if the first locale key is less, False otherwise.
        '''
        if not isinstance(other, LocaleKey):
            return NotImplemented
        return (self.table_id < other.table_id if self.instance_id == other.instance_id
                else self.instance_id < other.instance_id)

    def __gt__(self, other: object) -> bool:
        '''Compares two locale keys for the first to be greater than another.
        Starts to check with instance_id, then switches to table_id. 
        
        Returns:
            out (bool): True if the first locale key is greater, False otherwise.
        '''
        if not isinstance(other, LocaleKey):
            return NotImplemented
        return other < self

    def with_instance(self, instance_id: UInt32 | int | None) -> LocaleKey:
        '''Creates a new locale key with the replaced instance ID.

        Arguments:
            instance_id (UInt32 | None): The instance ID to use.
        
        Returns:
            out (LocaleKey): The locale key with the new instance ID.
        '''
        return LocaleKey(instance_id, self.table_id)

    def with_table(self, table_id: UInt32 | int | None) -> LocaleKey:
        '''Creates a new locale key with the replaced table ID.
        
        Arguments:
            table_id (UInt32 | None): The table ID to use.
        
        Returns:
            out (ResourceKey): The locale key with the new table ID.
        '''
        return LocaleKey(self.instance_id, table_id)
