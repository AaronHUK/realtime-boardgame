from model.player import Player
from model.exceptions import RequestException


class Purchaser:
    def __init__(self, board):
        self.board = board

    def request(self, player, unit):
        self.check_resources(player, unit)
        for res, amount in unit.cost:
            player.remove_resource(res, amount)
        self.board.add_unit(unit, player)

    def check_resources(self, player, unit):
        for res, amount in unit.cost:
            if player.resources[res] < amount:
                raise RequestException("Not enough {} (needed {}, had {})".format(
                                       res.name, amount, player.resources[res]))
        current_units = self.board.units[player].copy()
        for unit_type, amount in unit.sacrifices:
            for _ in range(amount):
                found_unit = False
                for unit_i in current_units:
                    if not found_unit and isinstance(unit_i, unit_type):
                        found_unit = unit_i
                        break
                if not found_unit:
                    raise RequestException("{} requires a {} to build ({} has {})".format(unit.__name__,
                                           unit_type.__name__, player.name, self.board.units[player]))
                current_units.remove(unit_i)
