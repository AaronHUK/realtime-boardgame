from model.units.unit import Unit
from model.resources import ResType
from collections import defaultdict


class GlowingInsect(Unit):
    """Has attack equal to half the number of Glowing Insects you control (rounded up)"""
    cost = [(ResType.BUILDS, 1), (ResType.CARBON, 3), (ResType.URANIUM, 1)]
    core = False
    INSECT_COUNT = defaultdict(int)
    sort = 1050

    def __init__(self, player, death_callback, **kwargs):
        self.INSECT_COUNT[player] += 1
        super(GlowingInsect, self).__init__(player, death_callback, **kwargs)

    @property
    def attack(self):
        return (1 + self.INSECT_COUNT[self.player]) // 2

    def on_death(self):
        self.INSECT_COUNT[self.player] -= 1
        super(GlowingInsect, self).on_death()


class NaturesBounty(Unit):
    """Generates 2C, 2Si, 1U. Sacrifice to gain 1 build, 2C"""
    cost = [(ResType.BUILDS, 1), (ResType.CARBON, 2), (ResType.URANIUM, 2)]
    core = False
    sort = 1020

    def start_of_turn(self):
        self.player.add_resource(ResType.CARBON, 2)
        self.player.add_resource(ResType.SILICON, 2)
        self.player.add_resource(ResType.URANIUM, 1)
        super(NaturesBounty, self).start_of_turn()

    def activate(self, target=None):
        self.player.add_resource(ResType.BUILDS, 1)
        self.player.add_resource(ResType.CARBON, 2)
        super(NaturesBounty, self).activate()
        self.on_death()
