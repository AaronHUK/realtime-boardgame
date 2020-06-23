import PySimpleGUI as sg
from model.exceptions import ExitException

sg.theme('DarkAmber')	# Add a touch of color

CURRENT_LOG = ""
COMBAT_LOG = sg.Text("", size=(80, 30))
_layout = [[COMBAT_LOG]]
_window = sg.Window("Combat Log", _layout)
_window.Finalize()


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
    global CURRENT_LOG
    CURRENT_LOG = "Round {} begins!".format(round_no)
    COMBAT_LOG.update(CURRENT_LOG)


def announce_declare_attack():
    global CURRENT_LOG
    CURRENT_LOG += "\n\nDeclare attack phase:"


def announce_actions():
    global CURRENT_LOG
    CURRENT_LOG += "\n\nBuy phase:"


def announce_attack():
    global CURRENT_LOG
    CURRENT_LOG += "\n\nAttack phase:"


def announce_turn(player, board):
    global CURRENT_LOG
    CURRENT_LOG += "\n{}'s turn:".format(player.name)


def get_declare_attack(player, board):
    pass


def get_player_action(player, purchaser):
    pass


def choose_target(player, board):
    pass
