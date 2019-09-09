from model.units import unit
from model import magics
from model.resources import ResType
from util.utils import min_max


FACTS = {ResType.CARBON: {},
         ResType.SILICON: {},
         ResType.URANIUM: {}}


def res_growth(res):
    if res == ResType.BUILDS:
        return 1
    return magics.GROWTH[res][min_max(len(FACTS[res]) - 1, max_val=len(magics.GROWTH[res]) - 1)]


class Constructor(unit.Unit):
    """+0/+1, generates +1 build"""
    defence = 1
    sort = 10
    cost = [(ResType.BUILDS, 1), (ResType.CARBON, 1), (ResType.SILICON, 1), (ResType.URANIUM, 1)]

    def start_of_turn(self):
        self.player.add_resource(ResType.BUILDS, 1)
        super(Constructor, self).start_of_turn()


class _BasicFact(unit.Unit):
    cost = [(ResType.BUILDS, 2)]
    res = None

    def __init__(self, player, death_callback, **kwargs):
        if player not in FACTS[self.res]:
            FACTS[self.res][player] = 0
        FACTS[self.res][player] += 1
        super(_BasicFact, self).__init__(player, death_callback, **kwargs)

    def start_of_turn(self):
        self.player.add_resource(self.res, res_growth(self.res))
        super(_BasicFact, self).start_of_turn()

    def on_death(self):
        FACTS[self.res][self.player] -= 1
        if FACTS[self.res][self.player] == 0:
            del FACTS[self.res][self.player]
        super(_BasicFact, self).on_death()


class TarPit(_BasicFact):
    """+0/+0, generates Carbon"""
    res = ResType.CARBON
    sort = 40


class Mine(_BasicFact):
    """+0/+0, generates Silicon"""
    res = ResType.SILICON
    sort = 50


class Centrifuge(_BasicFact):
    """+0/+0, generates Uranium"""
    res = ResType.URANIUM
    sort = 60
