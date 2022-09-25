#!/usr/env/bin python

from listener import Listener

if __name__ == '__main__':
    listener = Listener("192.168.229.130", 4444)
    listener.startListener()
