from model.units.unit import Unit
from model.units.api import Constructor
from model.resources import ResType
from model.exceptions import RequestException


class Deflector(Unit):
    """+0/+3"""
    cost = [(ResType.BUILDS, 1), (ResType.SILICON, 3)]
    defence = 3
    sort = 110


class PlasmaShields(Unit):
    """+0/+6"""
    cost = [(ResType.BUILDS, 1), (ResType.SILICON, 6)]
    defence = 6
    sort = 120


class UniversalConstructor(Unit):
    """upgrades Constructor: +0/-1, generates +1 build"""
    cost = [(ResType.BUILDS, 2), (ResType.SILICON, 4)]
    sacrifices = [(Constructor, 1)]
    defence = 0
    sort = 20

    def start_of_turn(self):
        self.player.add_resource(ResType.BUILDS, 2)
        super(UniversalConstructor, self).start_of_turn()


class FortifiedConstructor(Unit):
    '''upgrades Constructor: +0/+7'''
    cost = [(ResType.SILICON, 6)]
    sacrifices = [(Constructor, 1)]
    defence = 8
    sort = 30

    def start_of_turn(self):
        self.player.add_resource(ResType.BUILDS, 1)
        super(FortifiedConstructor, self).start_of_turn()


class TimedExplosive(Unit):
    """+2/+0 next turn ONLY"""
    cost = [(ResType.SILICON, 1)]
    sort = 125

    def start_of_turn(self):
        if self.attack > 0:
            self.on_death()
        if self.attack == 0:
            self.attack = 2


class VonNeumannBot(Unit):
    '''+1/+0, attack doubles every turn'''
    cost = [(ResType.BUILDS, 3), (ResType.SILICON, 11)]
    attack = 1
    sort = 130

    def start_of_turn(self):
        self.attack *= 2
        super(VonNeumannBot, self).start_of_turn()