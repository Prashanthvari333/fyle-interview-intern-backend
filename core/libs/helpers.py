import random
import string
from datetime import datetime

TIMESTAMP_WITH_TIMEZONE_FORMAT = '%Y-%m-%dT%H:%M:%S.%f%z'


class GeneralObject:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def __getitem__(self, key):
        return self.__dict__[key]


def get_utc_now():
    return datetime.utcnow()
