import threading

import message_parser
import comm
import worldmodel

class Agent:
    def __init__(self, host, port, teamname, version=11):
        """
        Gives us a connection to the server as one player on a team.
        """

        # the pipe through which all of our communication takes place
        self.sock = comm.Socket(host, port)
        
        # our model of the world
        self.world = worldmodel.WorldModel()
        
        # connect this agent to the server before we start the message loops
        self._server_init(teamname, version)
        
        # set up our threaded message receiving system 
        self.running = True # tell thread that we're currently running
        self.msg_thread = threading.Thread(target=self._message_loop,
                                           name="msg_thread")
        self.msg_thread.daemon = True # dies when parent thread dies

        # start processing received messages
        self.msg_thread.start()

    def _message_loop(self):
        """
        Handles messages received from the server.
        """

        while self.running:
            msg_list = message_parser.parse(self.sock.recv())
            
            # handle all received message types
            for msg in msg_list:
                if msg[0] == "see":
                    self._handle_see(msg)
                elif msg[0] == "hear":
                    self._handle_hear(msg)
                elif msg[0] == "sense_body":
                    self._handle_sense_body(msg)
                elif msg[0] == "player_param":
                    self._handle_player_param(msg)
                elif msg[0] == "player_type":
                    self._handle_player_type(msg)
                elif msg[0] == "server_param":
                    self._handle_server_param(msg)

                # raise exception on unknown type
                else:
                    raise ValueError("Unknown message type '%s'" % msg[0])

    def disconnect(self):
        # kill the message loop
        self.running = False

        # tell the server that we're quitting
        self.sock.send("(bye)")

        # join our message loop thread, just to be tidy (but only wait briefly)
        self.msg_thread.join(3)

    def _server_init(self, teamname, version):
        """
        Handle the initial response from the server.  This isn't called by the
        loop like the other handler messages are, since we need this message
        specifically to proceed any further.
        """
        
        # send the init message and get the first response
        init_msg = "(init %s (version %d))"
        self.sock.send(init_msg % (teamname, version))
        init_response = message_parser.parse(self.sock.recv())[0]
         
        # make sure we successfully connected to the server
        if init_response[0] == "error":
            raise IOError("Server returned an error: '%s'" % init_response[1])
        # if we connected, set pertinent variables
        elif init_response[0] == "init":
            self.team = init_response[1]
            self.uniform_number = init_response[2]
            self.world.set_play_mode(init_response[3])
        # otherwise, give up
        else:
            raise IOError("Server returned unknown response type '%'" %
                    init_response[0])

    def _handle_hear(self, msg):
        pass

    def _handle_server_param(self, msg):
        pass

    def _handle_see(self, msg):
        print "see:", msg

    def _handle_sense_body(self, msg):
        pass

    def _handle_player_type(self, msg):
        pass

    def _handle_player_param(self, msg):
        pass

if __name__ == "__main__":
    a = Agent("localhost", 6000, "team_agenttest")
    while 1:
        pass
