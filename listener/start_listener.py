"""Module containing the main func to run the listener"""

# Standard Library imports
import socket

# Local App imports
from listener import Listener

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if __name__ == '__main__':
    listener = Listener(local_ip="192.168.229.130", local_port=4444, listener=listener)
    listener.start_listener()
