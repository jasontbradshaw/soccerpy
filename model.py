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

        # used to store some number of recent messages heard by the agent.  the
        # queue's first item is the newest, and the last is the oldest.
        # messages are named tuples, where 'time' is time received, 'sender' is
        # direction or name of sender, and 'message' is the contents of the
        # received message.
        self.max_msg_queue_length = 25
        self.msg_queue = []

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

