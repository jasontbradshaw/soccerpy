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
        self.view_width = None
        self.view_quality = None
        self.stamina = None
        self.effort = None
        self.speed_amount = None
        self.speed_direction = None
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

        # create a new server parameter object for holding all server params
        self.server_parameters = ServerParameters()

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

        return (self.ball is not None and
                self.ball.distance is not None and
                self.ball.distance <= self.server_settings.kickable_margin)

    def get_ball_speed_max(self):
        """
        Returns the maximum speed the ball can be kicked at.
        """

        return self.server_settings.ball_speed_max

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
        Returns the agent's current stamina amount.
        """

        return self.stamina[0]

    def get_recovery(self):
        """
        Returns something.
        """

        # TODO: need body model inside world model

    def get_stamina_max(self):
        """
        Returns the maximum amount of stamina a player can have.
        """

        return self.server_settings.stamina_max

    def turn_body_to_object(self, obj):
        """
        Turns the player's body to face a particular object.
        """

        self.ah.turn(obj.direction)

class ServerParameters:
    """
    A storage container for all the settings of the soccer server.
    """

    def __init__(self):
        """
        Initialize default parameters for a server.
        """

        self.audio_cut_dist = 50
        self.auto_mode = 0
        self.back_passes = 1
        self.ball_accel_max = 2.7000000000000002
        self.ball_decay = 0.93999999999999995
        self.ball_rand = 0.050000000000000003
        self.ball_size = 0.085000000000000006
        self.ball_speed_max = 2.7000000000000002
        self.ball_stuck_area = 3
        self.ball_weight = 0.20000000000000001
        self.catch_ban_cycle = 5
        self.catch_probability = 1
        self.catchable_area_l = 2
        self.catchable_area_w = 1
        self.ckick_margin = 1
        self.clang_advice_win = 1
        self.clang_define_win = 1
        self.clang_del_win = 1
        self.clang_info_win = 1
        self.clang_mess_delay = 50
        self.clang_mess_per_cycle = 1
        self.clang_meta_win = 1
        self.clang_rule_win = 1
        self.clang_win_size = 300
        self.coach = 0
        self.coach_port = 6001
        self.coach_w_referee = 0
        self.connect_wait = 300
        self.control_radius = 2
        self.dash_power_rate =0.0060000000000000001
        self.drop_ball_time = 200
        self.effort_dec = 0.0050000000000000001
        self.effort_dec_thr = 0.29999999999999999
        self.effort_inc = 0.01
        self.effort_inc_thr = 0.59999999999999998
        self.effort_init = 1
        self.effort_min = 0.59999999999999998
        self.forbid_kick_off_offside = 1
        self.free_kick_faults = 1
        self.freeform_send_period = 20
        self.freeform_wait_period = 600
        self.fullstate_l = 0
        self.fullstate_r = 0
        self.game_log_compression = 0
        self.game_log_dated = 1
        self.game_log_dir = './'
        self.game_log_fixed = 0
        self.game_log_fixed_name = 'rcssserver'
        self.game_log_version = 3
        self.game_logging = 1
        self.game_over_wait = 100
        self.goal_width = 14.02
        self.goalie_max_moves = 2
        self.half_time = 300
        self.hear_decay = 1
        self.hear_inc = 1
        self.hear_max = 1
        self.inertia_moment = 5
        self.keepaway = 0
        self.keepaway_length = 20
        self.keepaway_log_dated = 1
        self.keepaway_log_dir = './'
        self.keepaway_log_fixed = 0
        self.keepaway_log_fixed_name = 'rcssserver'
        self.keepaway_logging = 1
        self.keepaway_start = -1
        self.keepaway_width = 20
        self.kick_off_wait = 100
        self.kick_power_rate = 0.027
        self.kick_rand = 0
        self.kick_rand_factor_l = 1
        self.kick_rand_factor_r = 1
        self.kickable_margin = 0.69999999999999996
        self.landmark_file = '~/.rcssserver-landmark.xml'
        self.log_date_format = '%Y%m%d%H%M-'
        self.log_times = 0
        self.max_goal_kicks = 3
        self.maxmoment = 180
        self.maxneckang = 90
        self.maxneckmoment = 180
        self.maxpower = 100
        self.minmoment = -180
        self.minneckang = -90
        self.minneckmoment = -180
        self.minpower = -100
        self.nr_extra_halfs = 2
        self.nr_normal_halfs = 2
        self.offside_active_area_size = 2.5
        self.offside_kick_margin = 9.1500000000000004
        self.olcoach_port = 6002
        self.old_coach_hear = 0
        self.pen_allow_mult_kicks = 1
        self.pen_before_setup_wait = 30
        self.pen_coach_moves_players = 1
        self.pen_dist_x = 42.5
        self.pen_max_extra_kicks = 10
        self.pen_max_goalie_dist_x = 14
        self.pen_nr_kicks = 5
        self.pen_random_winner = 0
        self.pen_ready_wait = 50
        self.pen_setup_wait = 100
        self.pen_taken_wait = 200
        self.penalty_shoot_outs = 1
        self.player_accel_max = 1
        self.player_decay = 0.40000000000000002
        self.player_rand = 0.10000000000000001
        self.player_size = 0.29999999999999999
        self.player_speed_max = 1.2
        self.player_weight = 60
        self.point_to_ban = 5
        self.point_to_duration = 20
        self.port = 6000
        self.prand_factor_l = 1
        self.prand_factor_r = 1
        self.profile = 0
        self.proper_goal_kicks = 0
        self.quantize_step = 0.10000000000000001
        self.quantize_step_l = 0.01
        self.record_messages = 0
        self.recover_dec = 0.002
        self.recover_dec_thr = 0.29999999999999999
        self.recover_init = 1
        self.recover_min = 0.5
        self.recv_step = 10
        self.say_coach_cnt_max = 128
        self.say_coach_msg_size = 128
        self.say_msg_size = 10
        self.send_comms = 0
        self.send_step = 150
        self.send_vi_step = 100
        self.sense_body_step = 100
        self.simulator_step = 100
        self.slow_down_factor = 1
        self.slowness_on_top_for_left_team = 1
        self.slowness_on_top_for_right_team = 1
        self.stamina_inc_max = 45
        self.stamina_max = 4000
        self.start_goal_l = 0
        self.start_goal_r = 0
        self.stopped_ball_vel = 0.01
        self.synch_micro_sleep = 1
        self.synch_mode = 0
        self.synch_offset = 60
        self.tackle_back_dist = 0.5
        self.tackle_cycles = 10
        self.tackle_dist = 2
        self.tackle_exponent = 6
        self.tackle_power_rate = 0.027
        self.tackle_width = 1
        self.team_actuator_noise = 0
        self.text_log_compression = 0
        self.text_log_dated = 1
        self.text_log_dir = './'
        self.text_log_fixed = 0
        self.text_log_fixed_name = 'rcssserver'
        self.text_logging = 1
        self.use_offside = 1
        self.verbose = 0
        self.visible_angle = 90
        self.visible_distance = 3
        self.wind_ang = 0
        self.wind_dir = 0
        self.wind_force = 0
        self.wind_none = 0
        self.wind_rand = 0
        self.wind_random = 0

