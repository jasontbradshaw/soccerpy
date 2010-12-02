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

        # body state
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


    def is_before_kick_off(self):
        """
        Tells us whether the game is in a pre-kickoff state.
        """

        return self.play_mode == WorldModel.PlayModes.BEFORE_KICK_OFF

    def is_kick_off_us(self):
        """
        Tells us whether it's our turn to kick off.
        """

        ko_left = WorldModel.PlayModes.KICK_OFF_L
        ko_right = WorldModel.PlayModes.KICK_OFF_R

        # return whether we're on the side that's kicking off
        return (self.side == WorldModel.SIDE_L and self.play_mode == ko_left or
                self.side == WorldModel.SIDE_R and self.play_mode == ko_right)

    def is_dead_ball_them(self):
        """
        Returns whether the ball is in the other team's posession and it's a
        free kick, corner kick, or kick in.
        """

        # shorthand for verbose constants
        kil = WorldModel.PlayModes.KICK_IN_L
        kir = WorldModel.PlayModes.KICK_IN_R
        fkl = WorldModel.PlayModes.FREE_KICK_L
        fkr = WorldModel.PlayModes.FREE_KICK_R
        ckl = WorldModel.PlayModes.CORNER_KICK_L
        ckr = WorldModel.PlayModes.CORNER_KICK_R

        # shorthand for whether left team or right team is free to act
        pm = self.play_mode
        free_left = (pm == kil or pm == fkl or pm == ckl)
        free_right = (pm == kir or pm == fkr or pm == ckr)

        # return whether the opposing side is in a dead ball situation
        if self.side == WorldModel.SIDE_L:
            return free_right
        else:
            return free_left

    def is_ball_kickable(self):
        """
        Tells us whether the ball is in reach of the current player.
        """

        # TODO: parse server settings

    def get_ball_speed_max(self):
        """
        Returns the maximum speed the ball can be kicked at.
        """

        # TODO: parse server settings

    def kick_to(self, position, speed):
        """
        Kick the ball to some position with some speed.
        """

        # TODO: predict angle and model speed at end

    def intercept(self, should_intercept):
        """
        TODO: what does this do?
        """

        # TODO: model ball movement and trajectory

    def turn_neck_to_object(self, obj):
        """
        Turns the player's neck to a given object.
        """

        self.ah.turn_neck(obj.direction)

    def get_strategic_position(self):
        """
        Returns a good position for the player to be in relative to its starting
        position and other variables.
        """

    def get_distance_to(self, point):
        """
        Returns the linear distance to some point on the field from the current
        point.
        """

        # TODO: need player coordinates to do this

    def turn_body_to_point(self, point):
        """
        Turns the agent's body to face a given point on the field.
        """

        # TODO: need player coordinates to do this

    def teleport_to_pos(self, point):
        """
        Teleports the player to a given (x, y) point using the 'move' command.
        """

        self.ah.move(point[0], point[1])

    def align_neck_with_body(self):
        """
        Turns the player's neck to be in line with its body, making the angle
        between the two 0 degrees.
        """

        # TODO: need body model inside world model

    def get_fastest_teammate_to_point(self, point):
        """
        Returns the uniform number of the fastest teammate to some point.
        """

    def get_stamina(self):
        """
        Returns the agent's current stamina.
        """

        # TODO: need body model inside world model

    def get_recovery(self):
        """
        Returns something...
        """

        # TODO: need body model inside world model

    def get_stamina_max(self):
        """
        Returns the maximum amount of stamina a player can have.
        """

        # TODO: parse server settings

    def turn_body_to_object(self, obj):
        """
        Turns the player's body to face a particular object.
        """

        self.ah.turn(obj.direction)

