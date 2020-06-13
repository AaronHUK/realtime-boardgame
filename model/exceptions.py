class ModelException(Exception):
    # This exception should NEVER be caught. It indicates that internal state
    # is inconsistent, and the program should be shut down.
    pass


class RequestException(Exception):
    # This is a recoverable exception, it should always be caught and handled.
    pass


class ExitException(Exception):
    # Used to exit the game by a player (e.g. by closing the main window).
    pass
