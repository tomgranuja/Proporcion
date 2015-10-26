#!/usr/bin/python3 -tt
#-*- coding:utf-8 -*-

import time
from threading import Timer

def print_and_launch():
    print("Launched at", time.time())
    f()
def run_at_some_times():
     print('Test start time', time.time())
     Timer(5, print_and_launch, ()).start()
     Timer(10, print_and_launch, ()).start()
     time.sleep(11)
     print('Test stoped at', time.time())

def f():
    pass
    
run_at_some_times()