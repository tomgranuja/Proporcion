#!/usr/bin/python3 -tt
#-*- coding:utf-8 -*-

import random, string, os
LENGTH = 3
POOL   = string.digits + string.ascii_uppercase

def gen_uid(previas = None):
    if previas == None:
        previas = [f[:LENGTH] for f in os.listdir('./')]
    while True:
      chars = [random.choice(POOL) for i in range(LENGTH) ]
      uid = ''.join(chars)
      if uid not in previas:
          print('Creado el identificador:', uid)
          return uid

def isValidUid(chars, length=LENGTH, pool=POOL):
    test = False
    if chars and len(chars) == length:
        for c in chars:
            if c not in pool:
                break
        else:
            test = True
    return test

def isValidName(chars):
    test = False
    if chars:
        for c in chars:
            if c != ' ':
                if not c.isalpha():
                    break
        else:
            test = True
    return test
            

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
    
    def delSession(self, sId):
        record = self.getRecordsDic()
        if sId in record:
            del(record[sId])
        with open(self.recFPath,'w') as f:
            for session in sorted(record.keys()):
                f.write('#{}\n'.format(session))
                for i, t, r in record[session]:
                    f.write('{} {} {}\n'.format(i,t,r))
        
if __name__ == "__main__":
    #subject = User()
    #with open(subject.recFPath, 'a') as f:
        #f.write('#S01\n')
    subject = User('H26')
    recordsDic = subject.getRecordsDic()
    last_i      = subject.getLastSessionId()
    for tup in recordsDic.get(last_i,[]): print(tup)