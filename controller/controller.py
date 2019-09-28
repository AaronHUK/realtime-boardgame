from model.board_state import BoardState
from model.player import Player
from model.purchaser import Purchaser
from model.exceptions import RequestException
import model.units.api as units_api
import display.text_api as display


class Controller:
    def __init__(self):
        player_names = display.ask_players()
        self.board = BoardState(player_names)
        self.players = self.board.units.keys()
        self.purchaser = Purchaser(self.board)
        self.round = 1
        while len(self.board.players) > 1:
            display.announce_round(self.round, self.board)
            self.play_round()
            self.round += 1
        winner = self.board.players[0].name
        losers = player_names
        losers.remove(winner)
        print("{} defeated {}!".format(winner, ', '.join(losers)))

    def play_round(self):
        round_players = set((player for player in self.board.units if not player.attacking))
        call_time = set()
        now_attacking = set((player for player in self.board.units if player.attacking))
        attacks = {}
        while len(round_players) != len(call_time):
            for player in round_players:
                if player in call_time:
                    continue
                display.announce_turn(player, self.board)
                action = display.get_player_action(player, self.purchaser)
                if action[0] == 'call_time':
                    call_time.add(player)
                elif action[0] == 'declare_attack':
                    player.attacking = True
                    round_players.remove(player)
                    call_time = set()
                else:
                    if getattr(self, action[0])(player, action[1]):
                        call_time.add(player)
                    else:
                        call_time = set()
        # Attacking time!
        for player in now_attacking:
            attacks[player] = display.choose_target(player, self.board)
        self.board.next_round(attacks)

    def build_unit(self, player, unit_type):
        try:
            self.purchaser.request(player, unit_type)
        except RequestException as e:
            display.reject(str(e) + ". {}'s turn is over.".format(player.name))
            return True

    def activate_unit(self, player, unit):
        self.board.get_unit(unit, player).activate()


if __name__ == "__main__":
    controller = Controller()
