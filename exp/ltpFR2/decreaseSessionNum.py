#!/usr/bin/python
from pyepl.locals import *


def run(exp,config):

    state = exp.restoreState()
    if not state.sessionNum:
        state.sessionNum == 0
    print 'OLD SESSION NUM:', state.sessionNum
    state.sessionNum -= 1
    print 'NEW SESSION NUM:', state.sessionNum
    exp.saveState(state)

# only do this if the experiment is run as a stand-alone program (not imported 
# as a library)
if __name__ == "__main__":
    import sys, re

    # start PyEPL, parse command line options, and do subject housekeeping
    exp = Experiment()

    # get subj. config
    config = exp.getConfig()

    # allow users to break out of the experiment with escape-F1 
    # (the default key combo)
    exp.setBreak()
    
    # now run the subject
    run(exp, config)
