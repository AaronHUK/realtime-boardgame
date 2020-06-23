from controller.phases import Phase
from controller.events import StartTurn
from model.board_state import BoardState
from model.purchaser import Purchaser
from datetime import datetime, timedelta
import time


class Controller:
    def __init__(self, net_players, rnd_units):
        self.phase = Phase.INIT
        self.net_players = net_players
        self.state = BoardState([ply.name for ply in net_players])
        self.purchaser = Purchaser(self.state)
        self.run_game()

    def run_game(self):
        round = 1
        while len(self.state.players) > 1:
            self.start_turn(round)
            self.declare()
            self.action()
            self.resolve()
            round += 1
        if len(self.state.players) == 1:
            self.msg_players("{} is the winner!".format(self.state.players[0].name))
        else:
            self.msg_players("Draw - everyone loses!")

    def event_loop(self, initial_time=20, bonus_time=8):
        anchor_time = datetime.now() + timedelta(seconds=initial_time)
        pauser = datetime.now() - timedelta(seconds=10)
        while anchor_time > datetime.now():
            if pauser + timedelta(milliseconds=100) > datetime.now():
                time.sleep(0.1)
            pauser = datetime.now()
            for player in self.net_players:
                event = player.non_blocking_get()
                if event:
                    if event.validate_and_msg(self.state, self.msg_players, self.purchaser):
                        self.apply_event(event)
                        anchor_time = max(anchor_time, datetime.now() + timedelta(seconds=bonus_time))
                    else:
                        player.message(player, "Failed: {}".format(event.last_error))
        return

    def start_turn(self, round_no):
        self.phase = Phase.START_TURN
        self.msg_players("\nRound {} begins!".format(round_no))
        self.apply_event(StartTurn())

    def declare(self):
        self.phase = Phase.DECLARE
        self.msg_players("\nDeclare attacking phase!")
        self.event_loop(initial_time=10)

    def action(self):
        self.phase = Phase.ACTION
        self.msg_players("\nAction phase!")
        self.event_loop()

    def resolve(self):
        self.phase = Phase.RESOLVE
        if self.state.attacks_pending:
            self.msg_players("\nResolve attack phase!")
            self.event_loop(bonus_time=10)
        else:
            self.msg_players("\nSkipping resolve attack phase (no-one declared)")

    def msg_players(self, message):
        for net_player in self.net_players:
            net_player.message(message)

    def apply_event(self, event):
        event.apply(self.state)
        for net_player in self.net_players:
            net_player.apply(event)
