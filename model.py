import message_parser
import sp_exceptions
import game_object

class WorldModel:
    """
    Holds and updates the model of the world as known from current and past
    data.
    """

    def __init__(self):
        # these variables store all objects for any particular game step
        self.ball = None
        self.goals = []
        self.flags = []
        self.players = []
        self.lines = []

class BodyModel:
    """
    Represents the agent's view of its own body.
    """

    def __init__(self):
        self.view_mode = (None, None)
        self.stamina = (None, None)
        self.speed = (None, None)
        self.head_angle = None

        # counts of actions taken so far
        self.kick_count = None
        self.dash_count = None
        self.turn_count = None
        self.say_count = None
        self.turn_neck_count = None
        self.catch_count = None
        self.move_count = None
        self.change_view_count = None

