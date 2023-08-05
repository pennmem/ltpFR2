from pyepl.locals import *

import os.path
from sys import argv
import Numeric
import RandomArray
import random

#run this script after completion of all four sessions of TFR_LTP to  calculate the bonus (in cents) that a given subject should receive for the experiment.

#example: pythonw bonus_calc.py LTP001

nsessions = 1
bonusPerSession = 500 # max bonus per session
penalty = 25 # cents lost for each mistake
error_resp = 0 # number of free mistakes

total_bonus = nsessions*bonusPerSession
subject = argv[1]
session = argv[2]

if session=='0':
    list_count = 1
else:
    list_count = 4

logpath = 'data/%s/session_%s/session.log' % (subject, session)
file = open(logpath, 'r')
lines = file.readlines()
for line in lines:
    stripline = line.strip()
    splitline = stripline.split('\t')
    type = splitline[2]
    
    if type == 'REC_START':
        list_count += 1
    if list_count > 3:
        if type == 'KEY_MSG':
            error_resp += 1
        elif type == 'SLOW_MSG':
            error_resp += 1

if error_resp < 0:
    error_resp = 0
total_bonus -= (error_resp*penalty)

print 'Congratulations! Your bonus for this session is %s!' % (total_bonus)
print error_resp


