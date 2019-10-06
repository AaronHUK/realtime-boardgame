from model.units.unit import Unit
from model.resources import ResType


class EnrichedUranium(Unit):
    """No effect"""
    cost = [(ResType.BUILDS, 1), (ResType.URANIUM, 2)]
    sort = 64
    prompt = True


class Nuke(Unit):
    """Next turn: immense damage to a player when attacking"""
    cost = [(ResType.BUILDS, 1), (ResType.SILICON, 2)]
    sacrifices = [(EnrichedUranium, 3)]
    sort = 160

    def start_of_turn(self):
        if self.attack > 0:
            self.on_death()
        self.attack += 60000
        super(Nuke, self).start_of_turn()


class FusionCannon(Unit):
    """2 Atk, 3 Def"""
    cost = [(ResType.BUILDS, 1), (ResType.URANIUM, 2)]
    attack = 2
    defence = 3
    sort = 140


class Irradiate(Unit):
    """4 Def this turn ONLY"""
    cost = [(ResType.URANIUM, 1)]
    defence = 4
    sort = 150

    def start_of_turn(self):
        self.on_death()
