from controller.phases import Phase
from model.exceptions import RequestException


class Event:
    phase = Phase.INIT

    def __init__(self):
        self.last_error = ""

    def validate_and_msg(self, board_state, cur_phase, msg_func, purchaser):
        if cur_phase != self.phase:
            self.last_error = "Invalid phase (requires {}, current {})".format(self.phase, cur_phase)
            return False
        return True

    def apply(self, board_state):
        pass


class BuyUnitEvent(Event):
    phase = Phase.ACTION

    def __init__(self, player, unit_type):
        super().__init__()
        self.player = player
        self.unit_type = unit_type
        self.purchaser = None

    def validate_and_msg(self, board_state, cur_phase, msg_func, purchaser):
        if not super().validate_and_msg(board_state, cur_phase):
            return False
        if self.player.attacking:
            self.last_error = "You cannot buy units after declaring attack!"
            return False
        try:
            purchaser.check_resources(self.player, self.unit_type)
        except RequestException as e:
            self.last_error = "Unable to buy {}: {}".format(self.unit_type.__name__, e.msg)
            return False
        self.purchaser = purchaser
        return True

    def apply(self, board_state):
        self.purchaser.request(self.player, self.unit_type)


class StartTurn(Event):
    phase = Phase.START_TURN

    def validate_and_msg(self, board_state, cur_phase, msg_func, purchaser):
        # The server generates this event... so this function will should never get called
        if not super().validate_and_msg(board_state, cur_phase):
            return False
        return True

    def apply(self, board_state):
        board_state.start_turn()


class DeclareAttack(Event):
    phase = Phase.DECLARE

    def __init__(self, player):
        super().__init__()
        self.player = player

    def validate_and_msg(self, board_state, cur_phase, msg_func, purchaser):
        if not super().validate_and_msg(board_state, cur_phase):
            return False
        if self.player.attacking:
            self.last_error = "You are already attacking!"
            return False
        msg_func("{} has declared his intention to attack!")
        return True

    def apply(self, board_state):
        self.player.attacking = True
