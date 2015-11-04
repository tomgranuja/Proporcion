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

class User():
    def __init__(self, uid=None):
        if uid == None:
            uid = gen_uid()
        self.uid = uid
        self.recFPath = '{}.dat'.format(self.uid)
    
    def getRecordsList(self):
        with open(self.recFPath) as f:
            recs_list = []
            rec_tups = []
            for l in f.readlines():
                if l[:5].upper() == '#SESIÓN'[:5]:
                    recs_list.append(rec_tups[:])
                    rec_tups = []
                else:
                    rec_tups.append(tuple(l.split()))
            recs_list.append(rec_tups[:])
            return recs_list[1:]
    
    def getLastSessionIndex(self):
        with open(self.recFPath) as f:
            sessions = []
            for l in f.readlines():
                if l[:5].upper() == '#SESIÓN'[:5]:
                    n = [int(s) for s in l.split() if s.isdigit()][0]
                    sessions.append(n)
            last_i = sessions[-1]
            print('Encontrada ultima sesión:', last_i)
            return last_i
        
        
if __name__ == "__main__":
    subject = User()
    with open(subject.recFPath, 'a') as f:
        f.write('#Sesión 0\n')
    #subject = User('WAM')
    #recordsList = subject.getRecordsList()
    #last_i      = subject.getLastSessionIndex()
    #for tup in recordsList[last_i]: print(tup)