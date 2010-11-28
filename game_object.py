
class GameObject:
    """
    Root class for all percievable objects in the world model.
    """

    def __init__(self, distance, direction):
        """
        All objects have a distance and direction to the player, at a minimum.
        """

        self.distance = distance
        self.direction = direction

class Line(GameObject):
    """
    Represents a line on the soccer field.
    """

    def __init__(self, distance, direction, line_id):
        self.line_id = line_id
        
        GameObject.__init__(self, distance, direction)

class Goal(GameObject):
    """
    Represents a goal object on the field.
    """

    def __init__(self, distance, direction, goal_id):
        self.goal_id = goal_id

        GameObject.__init__(self, distance, direction)

class Flag(GameObject):
    """
    A flag on the field.  Can be used by the agent to determine its position.
    """

    def __init__(self, distance, direction, flag_id):
        """
        Adds a flag id for this field object.  Every flag has a unique id.
        """

        self.flag_id = flag_id

        GameObject.__init__(self, distance, direction)

class MobileObject(GameObject):
    """
    Represents objects that can move.
    """

    def __init__(self, distance, direction, dist_change, dir_change, speed):
        """
        Adds variables for distance and direction deltas.
        """

        self.dist_change = dist_change
        self.dir_change = dir_change
        self.speed = speed

        GameObject.__init__(self, distance, direction)

class Ball(MobileObject):
    """
    A spcial instance of a mobile object representing the soccer ball.
    """

    def __init__(self, distance, direction, dist_change, dir_change, speed):
        
        MobileObject.__init__(self, distance, direction, dist_change,
                dir_change, speed)

class Player(MobileObject):
    """
    Represents a friendly or enemy player in the game.
    """

    def __init__(self, distance, direction, dist_change, dir_change, speed,
            position, team, side, uniform_number, body_direction,
            neck_direction):
        """
        Adds player-specific information to a mobile object.
        """

        self.team = team
        self.side = side
        self.position = position
        self.uniform_number = uniform_number
        self.body_direction = body_direction
        self.neck_direction = neck_direction

        MobileObject.__init__(self, distance, direction, dist_change,
                dir_change, speed)

