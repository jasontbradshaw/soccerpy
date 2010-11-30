import message_parser
import sp_exceptions
import game_object

class WorldModel:
    """
    Holds and updates the model of the world as known from current and past
    data.
    """

    class PlayModes:
        """
        Contains all valid play modes in the soccer game.  Used to match and set
        them in the WorldModel.  Can't be instantiated, and acts as a static
        class.
        """

        BEFORE_KICK_OFF = "before_kick_off"
        PLAY_ON = "play_on"
        TIME_OVER = "time_over"
        KICK_OFF_L = "kick_off_l"
        KICK_OFF_R = "kick_off_r"
        KICK_IN_L = "kick_in_l"
        KICK_IN_R = "kick_in_r"
        FREE_KICK_L = "free_kick_l"
        FREE_KICK_R = "free_kick_r"
        CORNER_KICK_L = "corner_kick_l"
        CORNER_KICK_R = "corner_kick_r"
        GOAL_KICK_L = "goal_kick_l"
        GOAL_KICK_R = "goal_kick_r"
        GOAL_L = "goal_l"
        GOAL_R = "goal_r"
        DROP_BALL = "drop_ball"
        OFFSIDE_L = "offside_l"
        OFFSIDE_R = "offside_r"

        def __init__(self):
            raise NotImplementedError("Don't instantiate a PlayModes class,"
                    " access it statically through WorldModel instead.")

    def __init__(self):
        # these variables store all objects for any particular game step
        self.ball = None
        self.goals = []
        self.flags = []
        self.players = []
        self.lines = []

        # handle player information, like uniform number and side
        self.side = None
        self.uniform_number = None

        # stores the most recent message heard
        self.last_message = None

        # the mode the game is currently in (default to not playing yet)
        self.play_mode = WorldModel.PlayModes.BEFORE_KICK_OFF

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

