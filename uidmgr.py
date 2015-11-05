#!/usr/bin/python3 -tt
#-*- coding:utf-8 -*-

import random, string, os
LENGTH = 3

def gen_uid(previas = None):
    if previas == None:
        previas = [f[:LENGTH] for f in os.listdir('./')]
    while True:
      chars = [random.choice(string.digits + string.ascii_uppercase)
               for i in range(LENGTH) ]
      uid = ''.join(chars)
      if uid not in previas:
          print('Creado el identificador:', uid)
          return uid

def nextSessionId(current=None):
    if current == None:
        current = 'S00'
    i = int(current.strip('S')) + 1
    return 'S{:02}'.format(i)

class User():
    def __init__(self, uid=None):
        if uid == None:
            uid = gen_uid()
        self.uid = uid
        self.recFPath = '{}.dat'.format(self.uid)
    
    def getRecordsDic(self):
        record = {}
        try:
            with open(self.recFPath) as f:
                for l in f.readlines():
                    if l[0] == '#':
                        if l.upper().strip('#S\n').isdigit():
                            key = l.upper().strip('#\n')
                            record[key] = []
                        continue
                    tup = tuple(l.split())
                    try:
                        record[key].append(tup)
                        #print(l[:-1])
                    except UnboundLocalError:
                        print('Warn: Dato sin sesión:',
                            l[:-1],
                            'descartado')
        except FileNotFoundError: pass
        return record
    
    def getLastSessionId(self):
        recdic = self.getRecordsDic()
        sessions = [ k for k in recdic ]
        last = None
        if sessions:
            last = sorted(sessions).pop()
        return last
        
        
if __name__ == "__main__":
    #subject = User()
    #with open(subject.recFPath, 'a') as f:
        #f.write('#S01\n')
    subject = User('H26')
    recordsDic = subject.getRecordsDic()
    last_i      = subject.getLastSessionId()
    for tup in recordsDic.get(last_i,[]): print(tup)