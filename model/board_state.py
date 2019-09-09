from model import resources
from model import player
from model.units.api import Constructor
from model.exceptions import RequestException, ModelException


class BoardState(object):
    def __init__(self, player_names):
        self.players = [player.Player(name) for name in player_names]
        self.units = {player_: [Constructor(player_, self._remove_unit), Constructor(player_, self._remove_unit)]
                      for player_ in self.players}
        self.pending_attack = set()
        self.pending_defeat = set()

    def add_unit(self, type_, player_, **modifiers):
        if player_.attacking:
            raise ModelException("An attacking player cannot build units")
        for unit_type, amount in type_.sacrifices:
            for _ in range(amount):
                found_unit = False
                for unit in self.units[player_]:
                    if not found_unit and isinstance(unit, unit_type):
                        found_unit = True
                        unit.on_death()
                if not found_unit:
                    raise ModelException("{} requires a {} to build ({} has {})".format(type_.__name__,
                                         unit_type.__name__, player_.name, self.units[player_]))
        new_unit = type_(player_, self._remove_unit, **modifiers)
        self.units[player_].append(new_unit)
        return new_unit  # for debugging / testing

    def next_round(self, attacks):
        for attacker in self.pending_attack:
            self.attack_player(attacker, attacks[attacker])
            attacker.attacking = False
        self.pending_attack = set()
        for defeated in self.pending_defeat:
            self.defeat_player(defeated)
        self.pending_defeat = set()
        for player_ in self.players:
            if player_.attacking:
                self.pending_attack.add(player_)
            for unit in self.units[player_]:
                unit.start_of_turn()

    def clear_all(self):
        for player_, units in self.units.items():
            for unit in units[:]:
                unit.on_death()

    def kill(self, player_, type_):
        self.get_unit(type_, player_).on_death()

    def get_unit(self, type_, player_):
        for unit in self.units[player_]:
            if isinstance(unit, type_):
                return unit
        raise RequestException("Player {} has no {}s\nunits: {}".format(
                        player_.name, type_.__name__, self.units[player_]))

    def total_attack(self, player_):
        return sum((unit.attack for unit in self.units[player_]))

    def total_defence(self, player_):
        return sum((unit.defence for unit in self.units[player_]))

    def attack_player(self, attacker, defender):
        if attacker not in self.pending_attack:
            raise ModelException("Players can only attack if they declared last turn that they were attacking")
        if self.total_attack(attacker) > self.total_defence(defender):
            self.transfer_resources(defender, attacker)
            self.pending_defeat.add(defender)

    @staticmethod
    def transfer_resources(giver, receiver):
        for res in resources.ResType:
            receiver.add_resource(res, giver.resources[res])
            giver.remove_resource(res, giver.resources[res])

    def defeat_player(self, vanquished):
        for unit in self.units[vanquished]:
            unit.on_death()
        del self.units[vanquished]
        self.players.remove(vanquished)

    def _remove_unit(self, unit, player_):
        self.units[player_].remove(unit)