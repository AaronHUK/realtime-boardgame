from enum import Enum, unique

@unique
class ResType(Enum):
    CARBON = 1
    SILICON = 2
    URANIUM = 3
    BUILDS = 4


SHORT_RES = {ResType.BUILDS: 'B', ResType.CARBON: 'C', ResType.SILICON: 'Si', ResType.URANIUM: 'U'}
