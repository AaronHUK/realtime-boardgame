from model.units.unit import Unit
from model.resources import ResType
from model.exceptions import RequestException


class Zergling(Unit):
    """+3/+0"""
    cost = [(ResType.BUILDS, 1), (ResType.CARBON, 3)]
    attack = 3
    sort = 70


class StemCell(Unit):
    """Sacrifice: Gain 2 builds"""
    cost = [(ResType.BUILDS, 1), (ResType.CARBON, 2)]
    sort = 62

    def activate(self, target=None):
        """Gain 2 builds"""
        self.player.add_resource(ResType.BUILDS, 2)
        super(StemCell, self).activate(target)
        self.on_death()


class Queen(Unit):
    """upgrades Zergling: +0/+5"""
    cost = [(ResType.BUILDS, 2), (ResType.CARBON, 5)]
    sacrifices = [(Zergling, 1)]
    attack = 3
    defence = 5
    sort = 80


class Hydralisk(Unit):
    """upgrades Zergling: +6/+0"""
    cost = [(ResType.BUILDS, 2), (ResType.CARBON, 5)]
    sacrifices = [(Zergling, 1)]
    attack = 9
    sort = 90


class Ultralisk(Unit):
    """upgrades Hydralisk: +16/+0"""
    cost = [(ResType.BUILDS, 3), (ResType.CARBON, 12)]
    sacrifices = [(Hydralisk, 1)]
    attack = 25
    sort = 100
