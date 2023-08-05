# ltpFR configuration.  BE VERY CAREFUL EDITING!!

"""
This module prepares the lists to be used
in the Spring 2010 LTP multisession experiment.
"""

import random
import prep

def createSessions(subj_no,config):
    """
        For each session i, list j, params[i][j] contains
        (pre-list distractor type,
         end-of-list distractor type)
        Where type is one of 0 or 1.

        0: no distractor
        1: math distractor
    """
    params = [[]]*config.nSessions
    all_combos = [(0,1),(1,1)]*(config.nLists/2)
    for i in range(config.nSessions):
        random.shuffle(all_combos)
        params[i]=tuple(all_combos)
    if len(params)!=config.nSessions:
        print 'WARNING: nSessions IN CONFIG FILE DOES NOT MATCH NUMBER OF SESSIONS IN sessionConfig'
    return params


def vectorizeParams(params):
    
    doFFR = []
    doRecog = []
    doMath = []
    doEFR = []
    subjISI = []
    subjRI = []
    subjTasks = []

    sessions = params.keys()
    for session in sessions:

        sessISI = []
        sessRI = []
        sessTasks = []

        doFFR.append(params[session]['config'][0])
        doRecog.append(params[session]['config'][1])
        doMath.append(params[session]['config'][2])
        doEFR.append(params[session]['config'][3])
        
        for list in params[session]['lists']:
            sessTasks.append(list[0])
            sessISI.append(list[1])
            if len(list) == 3:
                sessRI.append(list[2])
            else:
                sessRI.append('NULL DISTRACT')

        subjISI.append(sessISI)
        subjRI.append(sessRI)
        subjTasks.append(sessTasks)

    return subjISI, subjRI, subjTasks, doFFR, doRecog, doMath, doEFR

































        
