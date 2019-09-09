from model.resources import ResType

INIT = {ResType.BUILDS: 2,
        ResType.CARBON: 0,
        ResType.SILICON: 0,
        ResType.URANIUM: 0}
MAX = {ResType.BUILDS: 5,
       ResType.CARBON: 20,
       ResType.SILICON: 16,
       ResType.URANIUM: 9}
GROWTH = {ResType.BUILDS: [1],
          ResType.CARBON: [6, 5, 4, 3],
          ResType.SILICON: [5, 4, 3, 3],
          ResType.URANIUM: [4, 3, 2, 1]}
