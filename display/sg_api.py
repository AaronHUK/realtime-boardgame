import PySimpleGUI as sg
from model.exceptions import ExitException

sg.theme('DarkAmber')	# Add a touch of color


def ask_players():
    layout = [[sg.Text('How many players?')],
              [sg.Button('1'), sg.Button('2'), sg.Button('3'), sg.Button('4')]]

    # Create the Window
    window = sg.Window('How many players?', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            raise ExitException("User closed ask_players window")
        if event:  # if user closes window or clicks cancel
            print("{} {}".format(event, type(event)))
            break
    window.close()

    layout = []
    for _ in range(int(event)):
        layout.append([sg.InputText()])
    layout.append([sg.Button("Done")])
    window = sg.Window('Enter names', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            raise ExitException("User closed ask_players window")
        if event:
            print("{} {}".format(values, type(values)))
            break
    window.close()

    return values.values()


def announce_round(round_no):
    pass


def announce_declare_attack():
    pass


def announce_actions():
    pass


def announce_attack():
    pass



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
        p_us = OrderedDict()
        for unit in sorted(units, key=lambda x: x.sort):
            u_str = type(unit).__name__
            if unit.just_built:
                u_str = "+{}+".format(u_str)
            if u_str not in p_us:
                p_us[u_str] = 0
            p_us[u_str] += 1
        unit_strs.append([unit if count == 1 else "{}x{}".format(count, unit) for unit, count in p_us.items()])
    print(_columnise(unit_strs))



def announce_turn(player, board):
    pass


def _display_board_state(player, board):
    _display_players(player, board)
    _display_resources(board)
    _display_atkdef(board)
    _display_units(board)


def get_declare_attack(player, board):
    while True:
        _display_board_state(player, board)
        actions = "1. Declare Attack\n2. Call time\nEnter input: "
        action = forced_int_input(actions)
        if action == 1:
            return "declare_attack"
        if action == 2:
            return "call_time"
        else:
            print("Unrecognised input!")


def get_player_action(player, purchaser):
    while True:
        _display_board_state(player, purchaser.board)
        actions = "1. Build unit\n2. Activate unit\n3. Call time\nEnter input: "
        action = forced_int_input(actions)
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
            return "call_time",
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
    return units[min_max(forced_int_input(prompt + "Which unit: "), len(units) - 1)]


def get_player_unit(player, board):
    units = set((type(unit) for unit in board.units[player]
                 if type(unit).activate != Unit.activate and not unit.just_built))
    units = sorted(list(units), key=lambda a: a.sort)
    prompt = "0: Cancel\n"
    for index, unit in enumerate(units):
        prompt += "{}: {} ({})\n".format(index + 1, unit.__name__, unit.activate.__doc__)
    units.insert(0, None)
    return units[min_max(forced_int_input(prompt + "Which unit: "), len(units) - 1)]


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
    return defenders[min_max(forced_int_input(d_str), len(defenders) - 1)]


def reject(message):
    print("Illegal action: {}".format(message))
