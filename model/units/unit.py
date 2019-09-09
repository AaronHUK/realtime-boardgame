from model.resources import ResType, SHORT_RES


class Unit:
    cost = [(ResType.BUILDS, 1)]
    sacrifices = []
    attack = 0
    defence = 0
    sort = 0

    def __init__(self, player, death_callback, prompt=False, **kwargs):
        self.attack = self.attack
        self.defence = self.defence
        self.player = player
        self.death_callback = death_callback
        self.just_built = not prompt

    def start_of_turn(self):
        self.just_built = False

    def activate(self, target=None):
        pass

    def on_death(self):
        self.death_callback(self, self.player)

    @classmethod
    def cost_str(cls):
        res_s = []
        sac_s = []
        for res, amount in cls.cost:
            res_s.append("{}{}".format(amount, SHORT_RES[res]))
        for unit, amount in cls.sacrifices:
            amt_s = "" if amount == 1 else "{}x".format(amount)
            sac_s.append("{}{}".format(amt_s, unit.__name__))
        output = ", ".join(res_s)
        if sac_s:
            output += ", Sac:"
            output += ", ".join(sac_s)
        return output
