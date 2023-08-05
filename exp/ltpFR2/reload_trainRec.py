#!/usr/bin/python
from pyepl.locals import *

# other modules
import os
import sys
import shutil
import prep
reload(prep)
import session_config
import pywr



def run(exp,config):
	state = exp.restoreState()

    # load word recognition models for this subject
    recogModels = None
    recogGarbageModel = None
    if config.doRecog and config.doRecogFeedback:
        trainingDir = os.path.join(os.path.expanduser(config.recogFeedbackTrainingDir), exp.options['subject'], 'session_0')
        if not os.access(trainingDir, os.F_OK):
            raise ValueError("Recognition training directory not found: " + 
                             trainingDir)
        recogModels = pywr.loadModels(trainingDir)
        if len(recogModels) == 0:
            raise ValueError("Recognition training data not found: " + 
                             trainingDir)
        recogGarbageModel = pywr.loadGarbageModel()
    
     exp.saveState(state, 
                   recogModels=recogModels,
                   recogGarbageModel=recogGarbageModel)
    

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
