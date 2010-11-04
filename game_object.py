
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

class FieldObject(GameObject):
    """
    Represents some object on the field, stationary or mobile.
    """

    def __init__(self, distance, direction, position):
        """
        Field objects have a position in addition to GameObject's members.
        """

        self.position = position

        GameObject.__init__(self, distance, direction)

class Line(GameObject):
    """
    Represents a line on the soccer field.
    """

    def __init__(self, distance, direction, line_id):
        self.line_id = line_id
        
        GameObject.__init__(self, distance, direction)

class MobileObject(FieldObject):
    """
    Represents objects that can move.
    """

    def __init__(self, distance, direction, position, dist_change, dir_change,
            speed):
        """
        Adds variables for velocity vector deltas.
        """

        self.dist_change = dist_change
        self.dir_change = dir_change
        self.speed = speed

        FieldObject.__init__(self, distance, direction, position)

class StationaryObject(FieldObject):
    """
    Represents a field object that has a fixed position throughout the game.
    """

    def __init__(self, distance, direction, position):

        FieldObject.__init__(self, distance, direction, position)

class Ball(MobileObject):
    """
    A special instance of a mobile object representing the soccer ball.
    """

    def __init__(self, distance, direction, position, dist_change, dir_change,
            speed):
        
        MobileObject.__init__(self, distance, direction, position, dist_change,
                dir_change, speed)

class Player(MobileObject):
    """
    Represents a friendly or enemy player in the game.
    """

    def __init__(self, distance, direction, position, dist_change, dir_change,
            speed, team, side, uniform_number, body_direction, face_direction,
            neck_direction):
        """
        Adds player-specific information to a mobile object.
        """

        self.team = team
        self.side = side
        self.uniform_number = uniform_number
        self.body_direction = body_direction
        self.face_direction = face_direction
        self.neck_direction = neck_direction

        MobileObject.__init__(self, distance, direction, position, dist_change,
                dir_change, speed)

class Marker(StationaryObject):
    """
    A marker on the field.  Used to indicate relative position to the player.
    """

    def __init__(self, distance, direction, position, marker_id):
        """
        Adds a marker id for this field object.  Every marker has a unique id.
        """

        self.marker_id = marker_id

        StationaryObject.__init__(self, distance, direction, position)

