import socket

from pprint import pprint
from message_parser import parse

class Communicator:
    """
    Handles the barest level of communication with a server.
    """
    
    def __init__(self, host, port, bufsize=8192):
        """
        host: hostname of soccer server we want to connect to
        port: initial port of soccer server
        """
        
        self.address = (host, port)
        self.bufsize = bufsize
        
        # the socket communication with the server takes place on (ipv4, udp)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def send(self, msg):
        """
        Sends a message to the socket on the assigned host and port.
        """
        
        self.sock.sendto(msg, self.address)
    
    def recv(self, conform_address=True):
        """
        Receives data from the given socket.  Returns the data as a string.
        If conform_address is True, the address the server sent its response
        from replaces the address and port set at object creation.
        """
        
        data, address = self.sock.recvfrom(self.bufsize)
        
        if conform_address:
            self.address = address
        
        return data
