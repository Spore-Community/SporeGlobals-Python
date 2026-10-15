#!/usr/bin/env python3

'''Provides Spore localized strings (texts).'''

from __future__ import annotations




from typing import overload
from fixedint import UInt32
from .locale_key import LocaleKey
from .string import String16




class Text:
    '''A class that represents Spore localized text. Should never be used instead of a normal
    String32 if the locale key is unset and it's not used in a property that doesn't explicitly
    require this exact type.

    Attributes:
        locale (LocaleKey): The locale key to use.
        placeholder (String16Placeholder): The fixed 128-char long String16 that is used if
                                           the localization can't be applied.
    '''
    class String16Placeholder:
        '''A class that represents a fixed 128-char long String16.
        
        Attributes:
            data (bytearray): The 256-byte array that is used to store 2-byte wide characters.
            value (String16): The stringified contents of a bytearray.
        '''
        def __init__(self, value: String16 | str | None = None) -> None:
            self._data: bytearray = bytearray()
            self.value = value
            self._view: memoryview = memoryview(self._data)

        @property
        def data(self) -> bytearray:
            '''The 256-byte array that is used to store 2-byte wide characters.'''
            return self._data

        @property
        def value(self) -> String16:
            '''The stringified contents of a bytearray.'''
            return String16(self.data)
        @value.setter
        def value(self, value_modified: String16 | str | None) -> None:
            if value_modified is None:
                self._data[:] = bytes(256)
                return
            string: String16 = String16(value_modified)
            string_bytes: bytes = str(string).encode(string.encoding)
            if len(string_bytes) > 256:
                raise ValueError(f'String is too long: {len(string_bytes) // 2} char16s > 128.')
            self.data[:] = string_bytes.ljust(256, b'\0')

        def __str__(self) -> str:
            '''Gets the string, same as value.
            
            Returns:
                out (str): The stringified contents of a bytearray.
            '''
            return str(self.value)

    @overload
    def __init__(self,
                 locale: LocaleKey | None = None,
                 placeholder: Text.String16Placeholder | None = None) -> None: ...
    @overload
    def __init__(self,
                 instance_id: UInt32 | int | None = None,
                 table_id: UInt32 | int | None = None,
                 placeholder: Text.String16Placeholder | None = None) -> None: ...
    def __init__(self,
                 locale_instance_id: LocaleKey | UInt32 | int | None = None,
                 placeholder_table_id: Text.String16Placeholder
                                       | String16
                                       | str
                                       | UInt32
                                       | int
                                       | None = None,
                 placeholder: Text.String16Placeholder | String16 | str | None = None) -> None:
        if isinstance(locale_instance_id, LocaleKey):
            self.locale = locale_instance_id
            self.placeholder = placeholder_table_id
        elif isinstance(locale_instance_id, str | String16 | Text.String16Placeholder):
            self.locale = None
            self.placeholder = locale_instance_id
        elif (locale_instance_id is None
              and (placeholder_table_id is None
                   or isinstance(placeholder_table_id, (Text.String16Placeholder,
                                                        String16,
                                                        str)))):
            self.locale = None
            self.placeholder = (placeholder_table_id if placeholder_table_id is not None
                                else placeholder)
        else:
            self.locale = LocaleKey(locale_instance_id, placeholder_table_id)
            self.placeholder = placeholder

    @property
    def locale(self) -> LocaleKey:
        '''The locale key to use.'''
        return self._locale
    @locale.setter
    def locale(self, locale_modified: LocaleKey | None) -> None:
        self._locale = locale_modified if locale_modified is not None else LocaleKey()

    @property
    def placeholder(self) -> Text.String16Placeholder:
        '''The fixed 128-char long String16 that is used if the localization can't be applied.'''
        return self._placeholder
    @placeholder.setter
    def placeholder(self, placeholder_modified: (Text.String16Placeholder
                                                | String16
                                                | str
                                                | None)) -> None:
        self._placeholder = (placeholder_modified
                             if isinstance(placeholder_modified, Text.String16Placeholder)
                             else Text.String16Placeholder(placeholder_modified))

    def __str__(self):
        '''Gets a stringified localized text property.
        
        Returns:
            out (str): The formatted locale key and a placeholder text in quotation marks, replacing
                       the original ones with `\\"` everywhere in the string.
        '''
        placecolder_stringified: str = str(self.placeholder).replace('"', '\\"')
        return f'({self.locale}) "{placecolder_stringified}"'
