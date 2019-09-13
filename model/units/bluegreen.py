from model.units.unit import Unit
from model.units.greens import EnrichedUranium
from model.resources import ResType


class EMP(Unit):
    """Activate and sacrifice to nullify all attack for this turn."""
    cost = [(ResType.BUILDS, 1), (ResType.SILICON, 4), (ResType.URANIUM, 2)]
    sacrifices = [(EnrichedUranium, 2)]
    core = False
    sort = 1060

    def activate(self, target=None):
        self.defence += 61000
        super(EMP, self).activate(target)

    def start_of_turn(self):
        if self.defence > 0:
            self.on_death()
        super(EMP, self).start_of_turn()


class FissionReactor(Unit):
    """Activate and spend 2U to gain 2Si and 2 builds"""
    cost = [(ResType.BUILDS, 1), (ResType.SILICON, 6)]
    sacrifices = [(EnrichedUranium, 1)]
    core = False
    sort = 1030

    def activate(self, target=None):
        self.player.remove_resource(ResType.URANIUM, 2)
        self.player.add_resource(ResType.SILICON, 2)
        self.player.add_resource(ResType.BUILDS, 2)
        super(FissionReactor, self).activate(target)
