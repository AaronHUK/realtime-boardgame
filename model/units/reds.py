from model.units.unit import Unit
from model.resources import ResType
from model.exceptions import RequestException


class Zergling(Unit):
    """+3/+0"""
    cost = [(ResType.BUILDS, 1), (ResType.CARBON, 2)]
    attack = 3
    sort = 70


class StemCell(Unit):
    """Activate: Pay 2 C to gain a build"""
    cost = [(ResType.BUILDS, 1), (ResType.CARBON, 1)]
    sort = 62

    def activate(self, target=None):
        """Pay 2 C to gain a build"""
        self.player.remove_resource(ResType.CARBON, 1)
        self.player.add_resource(ResType.BUILDS, 1)
        super(StemCell, self).activate(target)


class Queen(Unit):
    """upgrades Zergling: +0/+5"""
    cost = [(ResType.BUILDS, 2), (ResType.CARBON, 3)]
    sacrifices = [(Zergling, 1)]
    attack = 3
    defence = 5
    sort = 80


class Hydralisk(Unit):
    """upgrades Zergling: +6/+0"""
    cost = [(ResType.BUILDS, 2), (ResType.CARBON, 3)]
    sacrifices = [(Zergling, 1)]
    attack = 9
    sort = 90


class Ultralisk(Unit):
    """upgrades Hydralisk: +16/+0"""
    cost = [(ResType.BUILDS, 3), (ResType.CARBON, 7)]
    sacrifices = [(Hydralisk, 1)]
    attack = 25
    sort = 100
