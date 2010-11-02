import queue
import threading

import message_parser
import comm

class Agent:
    def __init__(self, host, port, teamname, version=11):
        """
        Gives us a connection to the server as one player on a team.
        """

        # the pipe through which all of our communication takes place
        self.sock = comm.Socket(host, port)
        
        # for messages that have no send frequency limit (say, etc.)
        self.outgoing_unlim = queue.Queue()

        # for messages that are frequency limited (kick, dash, etc.)
        self.outgoing = queue.Queue()
        
        # initialize the agent and get the first response
        init_msg = "(init %s (version %d))"
        self.sock.send(init_msg % (teamname, version))
        init_reponse = message_parser.parse(self.sock.recv())
        

    def _handle_init(self, msg):
        pass

    def _handle_hear(self, msg):
        pass

    def _handle_server_param(self, msg):
        pass

    def _handle_see(self, msg):
        pass

    def _handle_sense_body(self, msg):
        pass

    def _handle_player_type(self, msg):
        pass

    def _handle_player_param(self, msg):
        pass

