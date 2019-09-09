class ModelException(Exception):
    # This exception should NEVER be caught. It indicates that internal state
    # is inconsistent, and the program should be shut down.
    pass


class RequestException(Exception):
    # This is a recoverable exception, it should always be caught and handled.
    pass
