from model import magics
from model.resources import ResType, SHORT_RES
from model.exceptions import RequestException
import model.units.api as uapi
from model.units.unit import Unit
from model.units.factories import res_growth
from util.utils import min_max


def ask_players():
    player_number = 1
    names = []
    while player_number < 6:
        new_name = input("Enter player {}'s name (leave blank if finished): ".format(player_number))
        if new_name == '':
            break
        names.append(new_name)
        player_number += 1
    assert len(names) >= 2
    return names


def announce_round(round_no, board):
    _flush_stdout()
    print("Round {}!".format(round_no))


def _flush_stdout():
    print("\n" * 2)


def _display_players(player, board):
    names = [plyr.name if plyr != player else "**{}**".format(plyr.name) for plyr in board.units]
    print(" | ".join(["{:15s}".format(plyr) for plyr in names]))


def _display_resources(board):
    res_strs = [[], [], [], []]
    for player, units in board.units.items():
        for index, (res, fact) in enumerate(((ResType.BUILDS, (uapi.Constructor,
                                                               uapi.FortifiedConstructor,
                                                               uapi.UniversalConstructor)),
                                             (ResType.CARBON, uapi.TarPit),
                                             (ResType.SILICON, uapi.Mine),
                                             (ResType.URANIUM, uapi.Centrifuge))):
            fact_count = sum([1 if not isinstance(unit, uapi.UniversalConstructor) else 2
                              for unit in units if isinstance(unit, fact)])
            res_growth(res)
            res_strs[index].append("{:2s}: {} /{} (+{})".format(
                SHORT_RES[res], player.resources[res], magics.MAX[res], res_growth(res) * fact_count))
    for player_strs in res_strs:
        print(" | ".join(["{:15s}".format(p_s) for p_s in player_strs]))


def _display_atkdef(board):
    fight_strs = [[], []]
    for player in board.units:
        atk_str = "Atk: {}".format(board.total_attack(player))
        if player.attacking:
            atk_str = "**" + atk_str + "**"
        fight_strs[0].append(atk_str)
        fight_strs[1].append("Def: {}".format(board.total_defence(player)))
    for player_strs in fight_strs:
        print(" | ".join(["{:15s}".format(p_s) for p_s in player_strs]))


def _display_units(board):
    unit_strs = []
    for index, (player, units) in enumerate(board.units.items()):
        _strs = []
        for unit in sorted(units, key=lambda x: x.sort):
            u_str = type(unit).__name__
            if unit.just_built:
                u_str = "+{}+".format(u_str)
            _strs.append(u_str)
        unit_strs.append(_strs)
    print(_columnise(unit_strs))


def _columnise(player_lists, width=15, separator=" | "):
    player_lists = _pad_lists(player_lists)
    lines = _transpose(player_lists)
    output = []
    for items in lines:
        output.append(separator.join((("{:" + str(width) + "s}").format(item) for item in items)))
    return "\n".join(output)


def _pad_lists(lists):
    max_len = max((len(mylist) for mylist in lists))

    def pad_me(my_list):
        if len(my_list) < max_len:
            return my_list + [''] * (max_len - len(my_list))
        return my_list

    return [pad_me(my_list) for my_list in lists]


def _transpose(lists):
    cols = len(lists)
    rows = len(lists[0])
    output = []
    for r_index in range(rows):
        new_row = []
        for c_index in range(cols):
            new_row.append(lists[c_index][r_index])
        output.append(new_row)
    return output


def announce_turn(player, board):
    _flush_stdout()
    print("{}'s turn!".format(player.name))
    _display_players(player, board)
    _display_resources(board)
    _display_atkdef(board)
    _display_units(board)


def get_player_action(player, purchaser):
    while True:
        actions = "1. Build unit\n2. Activate unit\n3. Declare attack\n4. End turn\nEnter input: "
        action = int(input(actions))
        if action == 1:
            unit = get_unit_name(player, purchaser)
            if unit is None:
                continue
            return "build_unit", unit
        if action == 2:
            unit = get_player_unit(player, purchaser.board)
            if unit is None:
                continue
            return "activate_unit", unit
        if action == 3:
            return "declare_attack", None
        if action == 4:
            return "end_turn",
        else:
            print("Unrecognised input!")


def get_unit_name(player, purchaser):
    unit_names = [name for name in dir(uapi) if not name.startswith("_")]
    units = [getattr(uapi, c_name) for c_name in unit_names]
    units.sort(key=lambda a: a.sort)
    prompt = "0: Cancel\n"
    for index, unit in enumerate(units):
        u_s = "{}: {} '{}' (cost: {})".format(index + 1, unit.__name__, unit.__doc__, unit.cost_str())
        try:
            purchaser.check_resources(player, unit)
        except RequestException:
            u_s = "[" + u_s + " *can't afford*]"
        prompt += u_s + "\n"
    units.insert(0, None)
    return units[min_max(int(input(prompt + "Which unit: ")), len(units) - 1)]


def get_player_unit(player, board):
    units = set((type(unit) for unit in board.units[player]
                 if type(unit).activate != Unit.activate and not unit.just_built))
    units = sorted(list(units), key=lambda a: a.sort)
    prompt = "0: Cancel\n"
    for index, unit in enumerate(units):
        prompt += "{}: {} ({})\n".format(index + 1, unit.__name__, unit.activate.__doc__)
    units.insert(0, None)
    return units[min_max(int(input(prompt + "Which unit: ")), len(units) - 1)]


def choose_target(player, board):
    _flush_stdout()
    print("{} is attacking!".format(player.name))
    _display_players(player, board)
    _display_resources(board)
    _display_atkdef(board)
    defenders = [plyr for plyr in board.units if plyr != player]
    d_str = ""
    for index, defender in enumerate(defenders):
        d_str += "{}. {}\n".format(index, defender.name)
    d_str += "Choose target: "
    return defenders[min_max(int(input(d_str)), len(defenders) - 1)]


def reject(message):
    print("Illegal action: {}".format(message))
