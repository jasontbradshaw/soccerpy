import message_parser
import sp_exceptions
import game_object

class WorldModel:
    """
    Holds and updates the model of the world as known from current and past
    data.
    """

    # constants for team sides
    SIDE_L = "l"
    SIDE_R = "r"

    class PlayModes:
        """
        Acts as a static class containing variables for all valid play modes.
        The string values correspond to what the referee calls the game modes.
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
        DROP_BALL = "drop_ball"
        OFFSIDE_L = "offside_l"
        OFFSIDE_R = "offside_r"

        def __init__(self):
            raise NotImplementedError("Don't instantiate a PlayModes class,"
                    " access it statically through WorldModel instead.")

    class RefereeMessages:
        """
        Static class containing possible non-mode messages sent by a referee.
        """

        # these are referee messages, not play modes
        FOUL_L = "foul_l"
        FOUL_R = "foul_r"
        GOALIE_CATCH_BALL_L = "goalie_catch_ball_l"
        GOALIE_CATCH_BALL_R = "goalie_catch_ball_r"
        TIME_UP_WITHOUT_A_TEAM = "time_up_without_a_team"
        TIME_UP = "time_up"
        HALF_TIME = "half_time"
        TIME_EXTENDED = "time_extended"

        # these are special, as they are always followed by '_' and an int of
        # the number of goals scored by that side so far.  these won't match
        # anything specifically, but goals WILL start with these.
        GOAL_L = "goal_l_"
        GOAL_R = "goal_r_"

        def __init__(self):
            raise NotImplementedError("Don't instantiate a RefereeMessages class,"
                    " access it statically through WorldModel instead.")

    def __init__(self, action_handler):
        """
        Create the world model with default values and an ActionHandler class it
        can use to complete requested actions.
        """

        # we use the action handler to complete complex commands
        self.ah = action_handler

        # these variables store all objects for any particular game step
        self.ball = None
        self.goals = []
        self.flags = []
        self.players = []
        self.lines = []

        # scores for each side
        self.score_l = 0
        self.score_r = 0

        # the name of the agent's team
        self.teamname = None

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
        self.neck_angle = None

        # counts of actions taken so far
        self.kick_count = None
        self.dash_count = None
        self.turn_count = None
        self.say_count = None
        self.turn_neck_count = None
        self.catch_count = None
        self.move_count = None
        self.change_view_count = None

