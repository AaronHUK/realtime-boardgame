from model.resources import ResType

INIT = {ResType.BUILDS: 2,
        ResType.CARBON: 0,
        ResType.SILICON: 0,
        ResType.URANIUM: 0}
MAX = {ResType.BUILDS: 5,
       ResType.CARBON: 12,
       ResType.SILICON: 8,
       ResType.URANIUM: 5}
GROWTH = {ResType.BUILDS: [1],
          ResType.CARBON: [4, 3, 2],
          ResType.SILICON: [3, 2, 1],
          ResType.URANIUM: [2, 1]}
