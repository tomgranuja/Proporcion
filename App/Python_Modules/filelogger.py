#!/usr/bin/python3 -tt
#-*- coding:utf-8 -*-

import os
LOGDIR = '../../Logger'

stim_id = {'bars': 'B', 'dots': 'D'}
ans_id  = {'prop': 'PRP', 'ord': 'ORD'}

def log_path(fname):
    '''Convert fname to relative path using LOGDIR.'''
    mod_dir = os.path.dirname(__file__)
    path = os.path.join(mod_dir, LOGDIR, fname)
    return os.path.relpath(path)

def testLogPath(uid, sess = 1, stim = None, ans = None):
    stimul_type = stim_id.get(stim,'n')
    answer_type = ans_id.get(ans, 'n')
    gm_type = stimul_type + answer_type
    fname = '{}_S{:02}_{}'.format(uid, sess, gm_type)
    return log_path(fname)

def practiceLogPath(uid, sess = 1, stim = None, ans = None):
    stimul_type = stim_id.get(stim,'n')
    answer_type = ans_id.get(ans, 'n')
    gm_type = stimul_type + answer_type
    fname = '{}_P{:02}_{}'.format(uid, sess, gm_type)
    return log_path(fname)
    

class Logger():
    def __init__(self, fpath):
        self.fpath = fpath
        self.initFile()
        
    def initFile(self):
        with open(self.fpath, 'w') as f:
            head = '{}\n'.format(self.fpath)
            f.write(head)
        
    def write(self, *args):
        with open(self.fpath, 'a')as f:
            arg_strings = [ str(arg) for arg in args ]
            line = ' '.join(arg_strings) + '\n'
            f.write(line)

if __name__ == "__main__":
    practPath = practiceLogPath('ABC')
    practLogger = Logger(practPath)
    n, t, r = (0, 3000, 0.3)
    practLogger.write(n, t, r)
    
    testPath  = testLogPath('ABC')
    testLogger  = Logger(testPath)
    n, t, r = (0,2500, 0.75)
    testLogger.write(n, t, r)
