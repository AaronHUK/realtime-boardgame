from model.units.unit import Unit
from model.resources import ResType


class Shapeshifter(Unit):
    """10 Def. Activate to switch to 10 Atk (and vice versa)."""
    cost = [(ResType.BUILDS, 3), (ResType.CARBON, 3), (ResType.SILICON, 2)]
    prompt = True
    defence = 10
    core = False
    sort = 1040

    def __init__(self, player, death_callback, **kwargs):
        self.form = "Def"
        super(Shapeshifter, self).__init__(player, death_callback, **kwargs)

    def activate(self, target=None):
        self.form = "Atk" if self.form == "Def" else "Def"
        self.attack = 10 if self.form == "Atk" else 0
        self.defence = 0 if self.form == "Atk" else 10
        super(Shapeshifter, self).activate(target)


class Constructor(Unit):
    """1 Def, generates 1 build"""
    defence = 1
    sort = 1010
    cost = [(ResType.BUILDS, 1), (ResType.CARBON, 2), (ResType.SILICON, 2)]
    prompt = True  # No effect; just to remove the unpleasant +s at the start of the game
    core = False

    def start_of_turn(self):
        self.player.add_resource(ResType.BUILDS, 1)
        super(Constructor, self).start_of_turn()
