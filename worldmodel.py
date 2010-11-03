import message_parser
import sp_exceptions

class WorldModel:
    """
    Holds and updates the model of the world as known from current and past
    data.
    
    All '_handle_*' functions deal with their appropriate message types
    as received from a server.  This allows adding a message handler to be as
    simple as adding a new '_handle_*' function to this object.
    """

    def __init__(self):
        self.play_mode = None

    def handle_message(self, msg):
        """
        Takes a raw message direct from the server, parses it, and stores its
        data within this object.
        """
        
        # get all the expressions contained in the given message
        parsed = message_parser.parse(msg)
        
        for msg in parsed:
            
            # this is the name of the function that should be used to handle
            # this message type.  we pull it from this object dynamically to
            # avoid having a huge if/elif/.../else statement.
            msg_func = "_handle_%s" % msg[0]

            if hasattr(self, msg_func):
                # call the appropriate function with this message
                getattr(self, msg_func).__call__(msg)

            # throw an exception if we don't know about the given message type
            else:
                m = "Can't handle message type '%s', function '%s' not found."
                raise sp_exceptions.MessageTypeError(m % (msg[0], msg_func))

    def _handle_see(self, msg):
        """
        Parses visual information in a message and turns it into useful data.
        """

        print "see:", msg[1:]

    def _handle_hear(self, msg):
        """
        Parses audible information and turns it into useful information.
        """

        print "hear:", msg[1:]

    def _handle_sense_body(self, msg):
        """
        Deals with the agent's body model information.
        """

        print "sense_body:", msg[1:]

    def _handle_player_param(self, msg):
        """
        Deals with player parameter information.
        """

        print "player_param:", msg[1:]

    def _handle_player_type(self, msg):
        """
        Handles player type information.
        """

        print "player_type:", msg[1:]

    def _handle_server_param(self, msg):
        """
        Stores server parameter information.
        """

        print "server_param:", msg[1:]

    def _handle_init(self, msg):
        """
        Deals with initialization messages sent by the server.
        """

        print "init:", msg[1:]
    
    def _handle_error(self, msg):
        """
        Deals with error messages by raising them as exceptions.
        """

        raise ServerError("Server returned an error: '%s'" % msg[1])

