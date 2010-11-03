
class SoccerServerError(Exception):
    """
    Represents an error message returned by the soccer server.
    """

class SoccerServerWarning(Exception):
    """
    Represents a warning message returned by the soccer server.
    """

class MessageTypeError(Exception):
    """
    An exception for an unknown message type received from the soccer server.
    """

class AgentAlreadyPlayingError(Exception):
    """
    Raised when a user calls an agent's play method after it has already started
    playing.
    """

