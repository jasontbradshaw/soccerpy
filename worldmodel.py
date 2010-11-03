
class WorldModel:
    """
    Holds and updates the model of the world as known from current and past
    data.
    """

    def __init__(self):
        self.play_mode = None

    def set_play_mode(self, mode):
        self.play_mode = mode

