from model.units import unit
from model import magics
from model.resources import ResType
from util.utils import min_max
from model.exceptions import ModelException


FACTS = {ResType.CARBON: {},
         ResType.SILICON: {},
         ResType.URANIUM: {}}


def res_growth(res):
    if res == ResType.BUILDS:
        return 1
    return magics.GROWTH[res][min_max(len(FACTS[res]) - 1, max_val=len(magics.GROWTH[res]) - 1)]


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


# OPTIONAL BELOW THIS POINT #
class Market(unit.Unit):
    sort = 65
    cost = [(ResType.BUILDS, 1)]
    core = False
    GENERATE = {ResType.CARBON: 3, ResType.SILICON: 2, ResType.URANIUM: 2}

    def activate(self, target=None):
        if not isinstance(target, ResType):
            raise ModelException("Market needs to be given a resource to generate (received a {})".format(
                                 type(target).__name__))
        self.player.add_resource(target, self.GENERATE[target])
        super(Market, self).activate()
