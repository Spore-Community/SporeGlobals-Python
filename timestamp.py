#!/usr/bin/env python3

'''Provides Spore-related timestamps.'''

__author__ = '0KepOnline' # https://github.com/0KepOnline
__license__ = 'MIT' # see: "LICENSE"
__maintainer__ = '0KepOnline'
__email__ = 'i.am@scenariopla.net'




from datetime import datetime, timezone




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

    def __new__(cls, value: int | None = None):
        '''Creates a new timestamp if the value is set to None, otherwise sets a given value.
        
        Arguments:
            value (int | None): The given value, or None. Default: None.
        '''
        return super().__new__(cls, value if value is not None else Timestamp._get_timestamp())


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
