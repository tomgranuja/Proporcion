#!/usr/bin/python3 -tt
#-*- coding:utf-8 -*-

import os
from functools import partial

#INPUT_DIR = os.path.join(os.path.dirname(__file__), '../Media/Dots')
#INPUT_DIR = os.path.join(os.path.relpath(os.path.dirname(__file__)), '../Inputs')
INPUT_DIR = '../Inputs'

def rel_path(dname, fname=None):
    '''Convert dirname and fname to relative path using INPUT_DIR.'''
    mod_dir = os.path.dirname(__file__)
    path_list = [ p for p in [dname, fname] if p is not None ]
    path = os.path.join(mod_dir, INPUT_DIR, *path_list)
    return os.path.relpath(path)

def pull_dir_data(dir_name, rcol=0, scol=1, wcol=2):
    '''Filtered col string from txt file in dir.'''
    SUFF_LIST = ['txt']
    datafiles = [s for s in os.listdir(rel_path(dir_name))
                 if s.split('.')[-1].lower() in SUFF_LIST]
    if len(datafiles) != 1:
        msg = '{} datafiles in {}.'.format(len(datafiles), dir_name)
        raise ValueError(msg)
    with open(rel_path(dir_name, datafiles[0])) as f:
        validlines = [ s for s in f.read().splitlines()
                       if s.strip() != '' and s[0] not in ['%', '#']]
        colt = (rcol, scol, wcol)
        datacols = [ [ s.split()[col] for col in colt ]
                    for s in validlines ]
        datalines = [ '{} {} {}'.format(*t) for t in datacols ]
        return '\n'.join(datalines)

def images_in_dir(dir_name):
    '''Sorted list of images paths in dir_path.'''
    SUFF_LIST = ['bmp', 'jpg', 'jpeg', 'png']
    images = [rel_path(dir_name, s) for s in os.listdir(rel_path(dir_name))
              if s.split('.')[-1].lower() in SUFF_LIST]
    return sorted(images)

def data_and_image_str(data_dir_name, rcol=0, scol=1, wcol=2):
    '''Append image paths to data in dir.'''
    colt = (rcol, scol, wcol)
    datalines = pull_dir_data(data_dir_name, *colt).splitlines()
    ipaths = images_in_dir(data_dir_name)
    if len(ipaths) != len(datalines):
        msg = '{} images and {} data lines.'.format(
               len(ipaths), len(datalines))
        raise ValueError(msg)
    data = ['{} {}'.format(d,i) for d,i in zip(datalines, ipaths)]
    return '\n'.join(data)

data            = partial(pull_dir_data)
data_img        = partial(data_and_image_str)
n4col_data      = partial(pull_dir_data, rcol=0, scol=2, wcol=3)
a4col_data      = partial(pull_dir_data, rcol=1, scol=2, wcol=3)
n4col_data_img  = partial(data_and_image_str, rcol=0, scol=2, wcol=3)
a4col_data_img  = partial(data_and_image_str, rcol=1, scol=2, wcol=3)

##########Inputs obsoletos (ratio, downscaling, width)##########
tPractice = '''
0.6 1 0.5
0.4 1 1
0.55 1 0.5
'''[1:]

cPractice = '''
0.6 2 0.5
0.45 2 1
0.58 1 0.5
'''[1:]

##Estimulos experimentales por sesion

##Grupo Test

t_Exp_01 = '''
0.21 1 1
0.76 1.5 0.5
0.01 1 0.5
0.5 1.5 1
0.95 1 0.5
0.03 1 0.5
0.5 1 0.5
0.16 1 1
0.76 4 1
0.26 4 0.5
0.21 4 1
0.61 1.5 1
0.8 1.5 0.5
0.03 1.5 0.5
0.03 4 0.5
0.43 1.5 0.5
0.95 4 1
0.7 4 1
0.76 1 0.5
0.7 1 0.5
0.26 1.5 1
0.8 1 0.5
0.16 1.5 1
0.5 4 1
0.26 1 1
0.21 1.5 0.5
0.61 1 1
0.43 1 1
0.7 1.5 1
0.16 4 0.5
0.01 1.5 0.5
0.95 1.5 1
0.43 4 0.5
0.01 4 1
0.61 4 0.5
0.8 4 1
'''[1:]

t_Exp_02 = '''
0.22 1 0.5
0.51 1 1
0.77 1.5 0.5
0.22 1.5 1
0.47 1 0.5
0.27 4 0.5
0.27 1 1
0.17 1 1
0.81 1.5 1
0.69 1.5 1
0.72 4 1
0.69 4 1
0.17 1.5 0.5
0.47 1.5 1
0.05 4 1
0.91 1.5 0.5
0.91 4 1
0.81 4 0.5
0.72 1 0.5
0.27 1.5 0.5
0.69 1 0.5
0.81 1 0.5
0.05 1 1
0.77 4 1
0.77 1 1
0.72 1.5 1
0.51 1.5 0.5
0.91 1 0.5
0.59 1 1
0.05 1.5 1
0.22 4 0.5
0.59 1.5 0.5
0.59 4 0.5
0.17 4 1
0.47 4 0.5
0.51 4 0.5
'''[1:]

t_Exp_03 = '''
0.81 1 0.5
0.82 1 0.5
0.32 1 0.5
0.73 1.5 1
0.23 4 1
0.73 4 0.5
0.5 1 0.5
0.81 1.5 0.5
0.82 1.5 0.5
0.5 4 0.5
0.32 1.5 1
0.68 4 1
0.07 1 0.5
0.45 1.5 0.5
0.57 4 0.5
0.18 4 1
0.07 4 1
0.82 4 1
0.73 1 1
0.68 1 0.5
0.23 1.5 1
0.18 1 1
0.81 4 0.5
0.93 1 1
0.23 1 0.5
0.5 1.5 0.5
0.68 1.5 1
0.57 1 1
0.18 1.5 0.5
0.07 1.5 1
0.45 1 1
0.93 1.5 1
0.45 4 0.5
0.32 4 1
0.93 4 1
0.57 1.5 0.5
'''[1:]

t_Exp_04 = '''
0.24 1 0.5
0.19 1 1
0.71 1.5 0.5
0.83 1 0.5
0.24 4 1
0.79 4 0.5
0.29 1 1
0.29 1.5 1
0.41 1 0.5
0.09 1 0.5
0.19 1.5 0.5
0.55 1.5 0.5
0.33 1.5 1
0.67 4 1
0.89 4 0.5
0.41 1.5 1
0.09 4 1
0.09 1.5 1
0.71 1 0.5
0.24 1.5 0.5
0.67 1 1
0.79 1.5 1
0.67 1.5 0.5
0.83 1.5 1
0.79 1 0.5
0.33 1 1
0.55 1 1
0.89 1 0.5
0.71 4 1
0.19 4 0.5
0.29 4 1
0.89 1.5 0.5
0.41 4 1
0.83 4 0.5
0.55 4 1
0.33 4 0.5
'''[1:]

t_Exp_05 = '''
0.74 1 1
0.28 1.5 1
0.2 1 0.5
0.71 1.5 1
0.3 1.5 0.5
0.28 4 0.5
0.28 1 1
0.74 1.5 0.5
0.2 1.5 0.5
0.11 1 1
0.53 1 1
0.3 4 0.5
0.25 4 1
0.97 1.5 1
0.11 4 0.5
0.99 4 1
0.97 4 1
0.2 4 0.5
0.71 1 0.5
0.84 1 0.5
0.25 1.5 1
0.3 1 0.5
0.39 1 0.5
0.99 1.5 0.5
0.25 1 1
0.99 1 0.5
0.74 4 0.5
0.97 1 1
0.84 1.5 1
0.84 4 0.5
0.71 4 0.5
0.11 1.5 1
0.39 4 1
0.39 1.5 0.5
0.53 4 1
0.53 1.5 1
'''[1:]



##Grupo control

c_Exp_01 = '''
0.41 1 1
0.57 3 1
0.552 1 1
0.41 4 0.5
0.552 3 1
0.466 3 0.5
0.57 1.5 0.5
0.448 3 1
0.482 3 1
0.43 3 1
0.466 1 0.5
0.518 3 1
0.43 4 0.5
0.534 4 1
0.518 1 1
0.552 4 0.5
0.534 3 0.5
0.482 1 1
0.59 4 1
0.43 1.5 0.5
0.448 1 1
0.59 1.5 0.5
0.448 4 0.5
0.466 1.5 1
0.57 1 1
0.448 1.5 0.5
0.482 1.5 0.5
0.57 4 0.5
0.534 1 0.5
0.482 4 0.5
0.43 1 1
0.534 1.5 1
0.518 1.5 0.5
0.552 1.5 0.5
0.466 4 1
0.518 4 0.5
'''[1:]

c_Exp_02 = '''
0.58 1.5 1
0.56 1 0.5
0.544 3 0.5
0.42 4 0.5
0.544 1 0.5
0.474 1 0.5
0.44 1.5 1
0.456 1 0.5
0.51 1 0.5
0.56 1.5 1
0.526 1.5 1
0.49 1 0.5
0.44 4 1
0.474 3 0.5
0.51 1.5 1
0.456 3 0.5
0.526 3 0.5
0.49 4 1
0.42 1.5 1
0.56 4 1
0.544 4 1
0.58 1 0.5
0.456 4 1
0.526 1 0.5
0.56 3 0.5
0.544 1.5 1
0.51 3 0.5
0.44 1 0.5
0.526 4 1
0.49 3 0.5
0.44 3 0.5
0.474 1.5 1
0.51 4 1
0.456 1.5 1
0.474 4 1
0.49 1.5 1
'''[1:]

c_Exp_03 = '''
0.57 3 1
0.552 1 1
0.466 3 0.5
0.57 1.5 0.5
0.466 1 0.5
0.482 3 1
0.552 3 1
0.534 4 1
0.502 1 1
0.448 3 1
0.518 3 1
0.498 3 1
0.552 4 0.5
0.518 1 1
0.498 1.5 0.5
0.534 3 0.5
0.482 1 1
0.498 4 0.5
0.43 3 1
0.552 1.5 0.5
0.466 1.5 1
0.43 4 0.5
0.466 4 1
0.518 4 0.5
0.448 4 0.5
0.534 1.5 1
0.502 4 0.5
0.448 1.5 0.5
0.482 4 0.5
0.502 1.5 0.5
0.448 1 1
0.518 1.5 0.5
0.502 3 1
0.534 1 0.5
0.482 1.5 0.5
0.498 1 1
'''[1:]

c_Exp_04 = '''
0.56 1 0.5
0.544 3 0.5
0.474 1 0.5
0.44 1.5 1
0.526 1.5 1
0.51 1 0.5
0.544 1 0.5
0.474 3 0.5
0.502 1 1
0.456 1 0.5
0.49 1 0.5
0.498 3 1
0.456 3 0.5
0.51 1.5 1
0.498 1.5 0.5
0.526 3 0.5
0.49 4 1
0.498 4 0.5
0.56 1.5 0.5
0.544 4 1
0.526 1 0.5
0.44 4 1
0.526 4 1
0.51 3 0.5
0.456 4 1
0.474 1.5 1
0.502 4 0.5
0.544 1.5 1
0.49 3 0.5
0.502 1.5 0.5
0.456 1.5 1
0.51 4 1
0.502 3 1
0.474 4 1
0.49 1.5 1
0.498 1 1
'''[1:]

c_Exp_05 = '''
0.552 1 0.5
0.466 3 0.5
0.482 3 1
0.448 1 1
0.518 3 1
0.51 1 0.5
0.466 1 0.5
0.518 1 1
0.502 1 1
0.534 4 1
0.49 1 0.5
0.498 3 1
0.534 3 0.5
0.51 1.5 1
0.498 1.5 0.5
0.482 1 1
0.49 4 1
0.498 4 0.5
0.552 4 0.5
0.466 1.5 1
0.482 1.5 0.5
0.448 3 1
0.482 4 0.5
0.51 3 0.5
0.466 4 1
0.518 1.5 0.5
0.502 4 0.5
0.534 1.5 1
0.49 3 0.5
0.502 1.5 0.5
0.534 1 0.5
0.49 1.5 1
0.502 3 1
0.518 4 0.5
0.51 4 1
0.498 1 1
'''[1:]



###Otras sesiones útiles para probar el código
dbg_sesion01 = t_Exp_01[251:]
dbgPractice = cPractice[19:]


##########Inputs test for bars and dots.#############################


if __name__ == "__main__":
    input_str = data_and_image_str('session_01')
    print(input_str)
