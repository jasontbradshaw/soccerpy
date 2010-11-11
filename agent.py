import threading
import time
import random

import sock
import model 
import sp_exceptions
import handler

class Agent:
    def __init__(self, host, port, teamname, version=11):
        """
        Gives us a connection to the server as one player on a team.  This
        immediately connects the agent to the server and starts receiving and
        parsing the information it sends.
        """

        # the pipe through which all of our communication takes place
        self.__sock = sock.Socket(host, port)

        # our models of the world and our body
        self.world = model.WorldModel()
        self.body = model.BodyModel()

        # handles all messages received from the server
        self.msg_handler = handler.MessageHandler(self.world, self.body)

        # handles the sending of actions to the server
        self.act_handler = handler.ActionHandler(self.__sock)

        # set up our threaded message receiving system 
        self.__parsing = True # tell thread that we're currently running
        self.__msg_thread = threading.Thread(target=self.__message_loop,
                                           name="message_loop")
        self.__msg_thread.daemon = True # dies when parent thread dies

        # start processing received messages. this will catch the initial server
        # response and all subsequent communication.
        self.__msg_thread.start()

        # create our thinking thread.  this will perform the actions necessary
        # to play a game of robo-soccer.
        self.__thinking = False
        self.__think_thread = threading.Thread(target=self.__think_loop,
                                             name="think_loop")
        self.__think_thread.daemon = True

        # send the init message and allow the message handler to handle further
        # responses.
        init_msg = "(init %s (version %d))"
        self.__sock.send(init_msg % (teamname, version))

    def play(self):
        """
        Kicks off the thread that does the agent's thinking, allowing it to play
        during the game.  Throws an exception if called while the agent is
        already playing.
        """

        # throw exception if called while thread is already running
        if self.__thinking:
            raise sp_exceptions.AgentAlreadyPlayingError(
                "Agent is already playing.")

        # run the method that sets up the agent's persistant variables
        self.setup_environment()

        # tell the thread that it should be running, then start it
        self.__thinking = True
        self.__think_thread.start()

    def disconnect(self):
        """
        Tell the loop threads to stop and signal the server that we're
        disconnecting, then join the loop threads and destroy all our inner
        methods.

        Since the message loop thread can conceiveably block indefinitely while
        waiting for the server to respond, we only allow it (and the think loop
        for good measure) a short time to finish before simply giving up.

        Once an agent has been disconnected, it is 'dead' and cannot be used
        again.  All of its methods get replaced by a method that raises an
        exception every time it is called.
        """

        # tell the message loop to terminate
        self.__parsing = False
        self.__thinking = False

        # tell the server that we're quitting
        self.__sock.send("(bye)")

        # tell our threads to join, but only wait breifly for them to do so
        self.__msg_thread.join(0.1)
        self.__think_thread.join(0.1)

        # used as a replacement for all this object's methods
        def destroyed_method():
            """
            Raises an error, no matter the arguments given.
            """
            
            m = ("Agent has been disconnected and no longer supports "
                    "any method calls.")
            raise NotImplementedError(m)

        # destroy this agent object's methods to prevent using them ever again
        for item in Agent.__dict__.keys(): # iterate over all created methods
            setattr(self, item, lambda *args: bork())

    def __message_loop(self):
        """
        Handles messages received from the server.

        This SHOULD NOT be called externally, since it's used as a threaded loop
        internally by this object.  Calling it externally is a BAD THING!
        """

        # loop until we're told to stop
        while self.__parsing:
            # receive message data from the server and pass it along to the
            # world model as-is.  the world model parses it and stores it within
            # itself for perusal at our leisure.
            raw_msg = self.__sock.recv()
            self.msg_handler.handle_message(raw_msg)

    def __think_loop(self):
        """
        Performs world model analysis and sends appropriate commands to the
        server to allow the agent to participate in the current game.

        Like the message loop, this SHOULD NOT be called externally.  Use the
        play method to start play, and the disconnect method to end it.
        """

        while self.__thinking:
            # performs the actions necessary for the agent to play soccer
            self.think()

            # this is necessary to allow our socket some time to recv messages,
            # as well as allowing us to send them.  this occurs since we use
            # threads, which in python share the same physical process.  if we
            # eat up all the time trying to send messages, we never recv any.
            time.sleep(0.0001)

    def setup_environment(self):
        """
        Called before the think loop starts, this allows the user to store any
        variables/objects they'll want access to across subsequent calls to the
        think method.
        """

        self.moved = False

    def think(self):
        """
        Performs a single step of thinking for our agent.  Gets called on every
        iteration of our think loop.
        """

        if not self.moved:
            self.act_handler.move(1000, 1000)
            self.moved = True

        if self.world.ball is not None:
            # kick in a random direction if the ball is close enough
            if self.world.ball.distance <= 1:
                self.act_handler.kick(100, random.randint(0, 181) - 180)
                return
            # dash towards the ball if it's within our field of view
            elif -5 < self.world.ball.direction < 5:
                self.act_handler.dash(100)
                return
            # turn to face the ball
            else:
                self.act_handler.turn(self.world.ball.direction)
                return
        else:
            # search for the ball
            self.act_handler.turn(10 + random.randint(0, 10))
            return

if __name__ == "__main__":
    import sys

    # arg1: team name
    # arg2: number of players to start
    
    agentlist = []
    for agent in xrange(int(sys.argv[2])):
        a = Agent("localhost", 6000, sys.argv[1])
        a.play()

        agentlist.append(a)

    try:
        while 1:
            time.sleep(0.05)
    except KeyboardInterrupt:
        print "Disconnecting agents..."
        for agent in agentlist:
            agent.disconnect()
        print "Agents disconnected."

