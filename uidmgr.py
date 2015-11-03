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

def init_data_file(uid):
    fpath = '{}.dat'.format(uid.upper())
    print('Agregando data a:', fpath)
    return open(fpath, 'a')

def last_session_index(uid):
    with open('{}.dat'.format(uid.upper())) as f:
        sessions = []
        for l in f.readlines():
            if l[:5].upper() == '#SESIÓN'[:5]:
                n = [int(s) for s in l.split() if s.isdigit()][0]
                sessions.append(n)
        last_i = sessions[-1]
        print('Encontrada ultima sesión:', last_i)
        return last_i
    
def get_records_list(uid):
    with open('{}.dat'.format(uid.upper())) as f:
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
        
    
if __name__ == "__main__":
    subject = gen_uid()
    #subject = 'IVQ'
    user_f = init_data_file(subject)
    user_f.write('#Sesión 0\n')
    user_f.close()
    #user_rec = get_records_list(subject)
    #i = last_session_index(subject)
    #for t in user_rec[i]: print(t)