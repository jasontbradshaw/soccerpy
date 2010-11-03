import threading

import comm
import worldmodel
import sp_exceptions

class Agent:
    def __init__(self, host, port, teamname, version=11):
        """
        Gives us a connection to the server as one player on a team.  This
        immediately connects the agent to the server and starts receiving and
        parsing the information it sends.
        """

        # the pipe through which all of our communication takes place
        self.sock = comm.Socket(host, port)

        # our model of the world
        self.world = worldmodel.WorldModel()

        # set up our threaded message receiving system 
        self.running = True # tell thread that we're currently running
        self.msg_thread = threading.Thread(target=self.__message_loop,
                                           name="msg_loop")
        self.msg_thread.daemon = True # dies when parent thread dies

        # start processing received messages
        self.msg_thread.start()

        # send the init message and allow the world model to handle further
        # responses.
        init_msg = "(init %s (version %d))"
        self.sock.send(init_msg % (teamname, version))

    def disconnect(self):
        # tell the message loop to terminate
        self.running = False

        # tell the server that we're quitting
        self.sock.send("(bye)")

        # join our message loop thread, just to be tidy (but only wait briefly)
        self.msg_thread.join(1)

    def __message_loop(self):
        """
        Handles messages received from the server.
        This SHOULD NOT be called externally, since it's used as a threaded loop
        internally by this object.  Calling it externally is a BAD THING!
        """

        # loop until we're told to stop
        while self.running:
            # receive message data from the server and pass it along to the
            # world model as-is.  the world model parses it and stores it within
            # itself for perusal at our leisure.
            raw_msg = self.sock.recv()
            self.world.handle_message(raw_msg)

if __name__ == "__main__":
    a = Agent("localhost", 6000, "team_agenttest")
    while 1:
        pass
