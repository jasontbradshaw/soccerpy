#!/usr/bin/env python

import threading
import time
import random

import sock
import sp_exceptions
import handler
from world_model import WorldModel

class Agent:
    def __init__(self):
        # whether we're connected to a server yet or not
        self.__connected = False

        # set all variables and important objects to appropriate values for
        # pre-connect state.

        # the socket used to communicate with the server
        self.__sock = None

        # models and the message handler for parsing and storing information
        self.wm = None
        self.msg_handler = None

        # parse thread and control variable
        self.__parsing = False
        self.__msg_thread = None

        self.__thinking = False # think thread and control variable
        self.__think_thread = None

        # whether we should run the think method
        self.__should_think_on_data = False

        # whether we should send commands
        self.__send_commands = False

    def connect(self, host, port, teamname, version=11):
        """
        Gives us a connection to the server as one player on a team.  This
        immediately connects the agent to the server and starts receiving and
        parsing the information it sends.
        """

        # if already connected, raise an error since user may have wanted to
        # connect again to a different server.
        if self.__connected:
            msg = "Cannot connect while already connected, disconnect first."
            raise sp_exceptions.AgentConnectionStateError(msg)

        # the pipe through which all of our communication takes place
        self.__sock = sock.Socket(host, port)

        # our models of the world and our body
        self.wm = WorldModel(handler.ActionHandler(self.__sock))

        # set the team name of the world model to the given name
        self.wm.teamname = teamname

        # handles all messages received from the server
        self.msg_handler = handler.MessageHandler(self.wm)

        # set up our threaded message receiving system
        self.__parsing = True # tell thread that we're currently running
        self.__msg_thread = threading.Thread(target=self.__message_loop,
                name="message_loop")
        self.__msg_thread.daemon = True # dies when parent thread dies

        # start processing received messages. this will catch the initial server
        # response and all subsequent communication.
        self.__msg_thread.start()

        # send the init message and allow the message handler to handle further
        # responses.
        init_address = self.__sock.address
        init_msg = "(init %s (version %d))"
        self.__sock.send(init_msg % (teamname, version))

        # wait until the socket receives a response from the server and gets its
        # assigned port.
        while self.__sock.address == init_address:
            time.sleep(0.0001)

        # create our thinking thread.  this will perform the actions necessary
        # to play a game of robo-soccer.
        self.__thinking = False
        self.__think_thread = threading.Thread(target=self.__think_loop,
                name="think_loop")
        self.__think_thread.daemon = True

        # set connected state.  done last to prevent state inconsistency if
        # something goes wrong beforehand.
        self.__connected = True

    def play(self):
        """
        Kicks off the thread that does the agent's thinking, allowing it to play
        during the game.  Throws an exception if called while the agent is
        already playing.
        """

        # ensure we're connected before doing anything
        if not self.__connected:
            msg = "Must be connected to a server to begin play."
            raise sp_exceptions.AgentConnectionStateError(msg)

        # throw exception if called while thread is already running
        if self.__thinking:
            raise sp_exceptions.AgentAlreadyPlayingError(
                "Agent is already playing.")

        # run the method that sets up the agent's persistant variables
        self.setup_environment()

        # tell the thread that it should be running, then start it
        self.__thinking = True
        self.__should_think_on_data = True
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

        # don't do anything if not connected
        if not self.__connected:
            return

        # tell the loops to terminate
        self.__parsing = False
        self.__thinking = False

        # tell the server that we're quitting
        self.__sock.send("(bye)")

        # tell our threads to join, but only wait breifly for them to do so.
        # don't join them if they haven't been started (this can happen if
        # disconnect is called very quickly after connect).
        if self.__msg_thread.is_alive():
            self.__msg_thread.join(0.01)

        if self.__think_thread.is_alive():
            self.__think_thread.join(0.01)

        # reset all standard variables in this object.  self.__connected gets
        # reset here, along with all other non-user defined internal variables.
        Agent.__init__(self)

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
            msg_type = self.msg_handler.handle_message(raw_msg)

            # we send commands all at once every cycle, ie. whenever a
            # 'sense_body' command is received
            if msg_type == handler.ActionHandler.CommandType.SENSE_BODY:
                self.__send_commands = True

            # flag new data as needing the think loop's attention
            self.__should_think_on_data = True

    def __think_loop(self):
        """
        Performs world model analysis and sends appropriate commands to the
        server to allow the agent to participate in the current game.

        Like the message loop, this SHOULD NOT be called externally.  Use the
        play method to start play, and the disconnect method to end it.
        """

        while self.__thinking:
            # tell the ActionHandler to send its enqueued messages if it is time
            if self.__send_commands:
                self.__send_commands = False
                self.wm.ah.send_commands()

            # only think if new data has arrived
            if self.__should_think_on_data:
                # flag that data has been processed.  this shouldn't be a race
                # condition, since the only change would be to make it True
                # before changing it to False again, and we're already going to
                # process data, so it doesn't make any difference.
                self.__should_think_on_data = False

                # performs the actions necessary for the agent to play soccer
                self.think()
            else:
                # prevent from burning up all the cpu time while waiting for data
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

        # DEBUG:  tells us if a thread dies
        if not self.__think_thread.is_alive() or not self.__msg_thread.is_alive():
            raise Exception("A thread died.")

        # move to a random field position on first call
        if not self.moved:
            self.wm.ah.move(1000, 1000)
            self.moved = True

        # perform random-play strategy
        if self.wm.ball is not None and self.wm.ball.direction is not None:
            # kick in towards the opposing goal if we're close to ball enough
            if self.wm.ball.distance <= 1:

                for g in self.wm.goals:
                    # kick towards the goal if we can see it and know it's not
                    # ours.
                    if g.goal_id is not None:
                        if g.goal_id != self.wm.side:
                            self.wm.ah.say("K")
                            self.wm.ah.kick(100, g.direction)
                            return
                    # kick towards the first friendly player
                    else:
                        for p in self.wm.players:
                            if p.side == self.wm.side:
                                self.wm.ah.kick(100, p.direction)
                                return
                else:
                    # search for goal otherwise 
                    d = random.randint(0, 10)
                    self.wm.ah.kick(-5, -5 + d)
                    return
            # dash towards the ball if it's within our field of view and we can
            # move.
            elif (-7 < self.wm.ball.direction < 7 and
                    self.wm.play_mode != WorldModel.PlayModes.BEFORE_KICK_OFF):
                self.wm.ah.dash(50)
                return
            # turn to face the ball
            else:
                self.wm.ah.turn(self.wm.ball.direction / 2)
                return
        else:
            # search for the ball
            self.wm.ah.turn(30 + random.randint(0, 10))
            return

if __name__ == "__main__":
    import sys

    # enforce corrent number of arguments, print help otherwise
    if len(sys.argv) < 3:
        print "args: ./agent.py <team_name> <num_players>"
        sys.exit()

    # arg1: team name
    # arg2: number of players to create

    agentlist = []
    total_agents = 0
    for agent in xrange(min(11, int(sys.argv[2]))):
        print "Creating Agent %d:" % agent

        print "  Initializing...",
        a = Agent()
        print "\t[DONE]"

        print "  Connecting...",
        a.connect("localhost", 6000, sys.argv[1])
        print "\t[DONE]"

        print "  Starting play...",
        a.play()
        print "\t[DONE]"

        agentlist.append(a)
        total_agents += 1

    print
    print "Launched %d agents." % total_agents

    try:
        while 1:
            time.sleep(0.05)
    except KeyboardInterrupt:
        print "Disconnecting agents..."
        for agent in agentlist:
            print "  Disconnecting...",
            agent.disconnect()
            print "\t[DONE]"
        print "Agents disconnected."

