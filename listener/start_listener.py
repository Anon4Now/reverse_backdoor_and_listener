"""Module containing the main func to run the listener"""

# Standard Library imports
import socket

# Local App imports
from listener import Listener


if __name__ == '__main__':
    listener = Listener(local_ip="192.168.229.130", local_port=4444, listener=socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    listener.start_listener()
