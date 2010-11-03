import threading
import time

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
        self.parsing = True # tell thread that we're currently running
        self.msg_thread = threading.Thread(target=self.__message_loop,
                                           name="message_loop")
        self.msg_thread.daemon = True # dies when parent thread dies

        # start processing received messages. this will catch the initial server
        # response and all subsequent communication.
        self.msg_thread.start()

        # create our thinking thread.  this will perform the actions necessary
        # to play a game of robo-soccer.
        self.thinking = False
        self.think_thread = threading.Thread(target=self.__think_loop,
                                             name="think_loop")
        self.think_thread.daemon = True

        # send the init message and allow the world model to handle further
        # responses.
        init_msg = "(init %s (version %d))"
        self.sock.send(init_msg % (teamname, version))

    def disconnect(self):
        """
        Tell the loop threads to stop and signal the server that we're
        disconnecting.

        Since the message loop thread can conceiveably block indefinitely while
        waiting for the server to respond, we only allow it (and the think loop
        for good measure) a short time to finish before simply giving up.
        """

        # tell the message loop to terminate
        self.parsing = False
        self.thinking = False

        # tell the server that we're quitting
        self.sock.send("(bye)")

        # tell our threads to join, but only wait breifly for them to do so
        self.msg_thread.join(1)
        self.think_thread.join(1)

    def play(self):
        """
        Kicks off the thread that does the agent's thinking, allowing it to play
        during the game.  Every time this is called, it sets up a new thread of
        control to allow the agent to play asynchronosly.  Throws an exception
        if called while the agent is already playing.
        """

        # throw exception if called while thread is already running
        if self.thinking:
            raise sp_exceptions.AgentAlreadyPlayingError(
                "Agent is already playing.")

        self.thinking = True
        self.think_thread.start()

    def __message_loop(self):
        """
        Handles messages received from the server.

        This SHOULD NOT be called externally, since it's used as a threaded loop
        internally by this object.  Calling it externally is a BAD THING!
        """

        # loop until we're told to stop
        while self.parsing:
            # receive message data from the server and pass it along to the
            # world model as-is.  the world model parses it and stores it within
            # itself for perusal at our leisure.
            raw_msg = self.sock.recv()
            self.world.handle_message(raw_msg)

    def __think_loop(self):
        """
        Performs world model analysis and sends appropriate commands to the
        server to allow the agent to participate in the current game.

        Like the message loop, this SHOULD NOT be called externally.  Use the
        play method to start play, and the disconnect method to end it.
        """

        while self.thinking:
            # performs the actual thinking our agent will do
            self.think()

            # this is necessary to allow our socket some time to recv messages,
            # as well as allowing us to send them.  this occurs since we use
            # threads, which in python share the same physical process.  if we
            # eat up all the time trying to send messages, we never recv any.
            time.sleep(0.0001)

    def think(self):
        """
        Performs a single step of thinking for our agent.  Gets called on every
        iteration of our think loop.
        """

        self.move(1000, 1000)

    def move(self, x, y):
        """
        Teleport the player to some location on the field.  Only works before
        play begins, ie. pre-game, before starting again at half-time, and
        post-goal.  If an invalid location is specified, player is teleported to
        a random location on their side of the field.
        """

        msg = "(move %.10f %.10f)" % (x, y)
        self.sock.send(msg)

    def turn(self, relative_degrees):
        """
        Turns the player's body some number of degrees relative to its current
        angle.
        """

        # disallow unreasonable turning
        assert -180 <= relative_degrees <= 180

        msg = "(turn %.10f)" % relative_degrees
        self.sock.send(msg)

    def dash(self, power):
        """
        Accelerate the player in the direction its body currently faces.
        """

        msg = "(dash %.10f)" % power
        self.sock.send(msg)

    def kick(self, power, relative_direction):
        """
        Accelerates the ball with the given power in the given direction,
        relative to the current direction of the player's body.
        """

        msg = "(kick %.10f %.10f)"
        self.sock.send(msg)

    def catch(self, relative_direction):
        """
        Attempts to catch the ball and put it in the goalie's hand.  The ball
        remains there until the goalie kicks it away.
        """

        msg = "(catch %.10f)" % relative_direction
        self.sock.send(msg)

    def turn_neck(self, relative_direction):
        """
        Rotates the player's neck relative to its previous direction.  Neck
        angle is relative to body angle.
        """

        msg = "(turn_neck %.10f)" % relative_direction
        self.sock.send(msg)

if __name__ == "__main__":
    import time
    a = Agent("localhost", 6000, "team_agenttest")
    a.play()

    try:
        while 1:
            time.sleep(0.05)
    except KeyboardInterrupt:
        print "Disconnecting agent..."
        a.disconnect()
        print "Agent disconnected."

