# to debug (in the python command prompt):
# import pdb
# pdb.run(import test_taskOrder) for the first run
# pbd.run(reload(test_taskOrder)) after first run
# if it gives you an error, try running the same command again.

#!/usr/bin/python
from pyepl.locals import *

# other modules
import random
import time
import RandomArray
import os
import sys
import shutil

exp = Experiment()
exp.setup()
config = exp.getConfig()

import taskOrder
reload(taskOrder)
to = taskOrder

trainSets = []
trainSets.append([[2,2,2,6], [2,2,3,5], [2,2,4,4], [2,3,3,4], [3,3,3,3]])
trainSets.append([[2,4,6], [2,5,5], [3,3,6], [3,4,5], [4,4,4]])

subj_to = to.subjTaskOrder(config)
print subj_to[0]
print subj_to[1]

import wordOrder
reload(wordOrder)
wo = wordOrder

wpfile = '/Volumes/mortonne/Matlab/apem_e7/pools/wasnorm_wordpool.txt'
tnfile = '/Volumes/mortonne/Matlab/apem_e7/pools/wasnorm_task.txt'
wasfile = '/Volumes/mortonne/Matlab/apem_e7/pools/wasnorm_was.txt'

minRating = .3
maxRating = .7
WASthresh = .55
maxTries = 1200
lureRatios = (0.125, 0.25, 0.375, 0.5)

wp_tot, subj_wo, subj_recog = wo.subjWordOrder(subj_to, config)

words = []
for i in range(len(subj_recog)):
    sess_words = []
    for j in range(len(subj_recog[i])):
	for k in range(len(subj_recog[i][j])):
	    sess_words.append(subj_recog[i][j][k])
    
    print '\nsession %d:\n' % i
    sess_count = []
    for j in range(len(sess_words)):
	sess_count.append(sess_words.count(sess_words[j]))
    
    print max(sess_count)
    words.extend(sess_words)

print '\ntotal:\n'
all_count = []
for i in range(len(words)):
    all_count.append(words.count(words[i]))

print max(all_count)
