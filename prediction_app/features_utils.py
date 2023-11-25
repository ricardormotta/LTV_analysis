from pydantic import BaseModel
from enum import Enum


# Enum for categorical values
class ProductEnum(str, Enum):
    product_a = 'product_a'
    product_c = 'product_c'
    product_b = 'product_b'
    pass

class ChannelEnum(str, Enum):
    channel_a = 'channel_a'
    channel_b = 'channel_b' 
    pass

class AgeEnum(str, Enum):
    between_18_24 = '18-24'
    between_25_29 = '25-29'
    between_30_34 = '30-34'
    between_35_39 = '35-39'
    between_40_44 = '40-44'
    between_45_49 = '45-49'
    between_50_54 = '50-54'
    more_55 = '55+'
    pass

class OperatingSystemEnum(str, Enum):
    iOS= "iOS" 
    Android= "Android"
    pass


class NumericalFeatures(BaseModel):
    pass

    @classmethod
    def from_dict(cls, input_dict):
        return cls(**input_dict)


class BooleanFeatures(BaseModel):
    pass

    @classmethod
    def from_dict(cls, input_dict):
        return cls(**input_dict)
