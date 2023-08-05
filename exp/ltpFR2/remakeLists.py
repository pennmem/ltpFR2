#!/usr/bin/python
from pyepl.locals import *

# other modules
import os
import sys
import shutil
import prep
reload(prep)
import session_config



def run(exp,config):
	state = exp.restoreState()

	subj_no = int(exp.options['subject'][-2:])
	params = session_config.createSessions(subj_no,config)
	(subjISI,subjRI,subjTasks,doFFR,doRecog,doMath,doEFR) = session_config.vectorizeParams(params)
	
	# set word order for this subject
	(wp, subjItems, subjRecog, subjSemBins) = prep.subjWordOrder(subjTasks, config, subj_no)

	if not state.sessionNum:
		state.sessionNum == 0


	
	
	state.wp=wp
	state.subjItems[state.sessionNum:]=subjItems[state.sessionNum:]
	state.subjTasks[state.sessionNum:]=subjTasks[state.sessionNum:]
	state.subjRecog[state.sessionNum:]=subjRecog[state.sessionNum:]
	#state.subjISI[state.sessionNum:]=subjISI[state.sessionNum:]
	#state.subjRI[state.sessionNum:]=subjRI[state.sessionNum:]
	#state.doFFR[state.sessionNum:]=doFFR[state.sessionNum:]
	#state.doRecog[state.sessionNum:]=doRecog[state.sessionNum:]
	#state.doMath[state.sessionNum:]=doMath[state.sessionNum:]
	#state.doEFR[state.sessionNum:]=doEFR[state.sessionNum:]
	exp.saveState(state)
	
	
	
	# write out all the to-be-presented items to text files
	for i, sessionItems in enumerate(state.subjItems):
		exp.setSession(i)
		for j, listItems in enumerate(sessionItems):
			# each list written to data/[subject]/session_[i]/[j].lst
			listFile = exp.session.createFile('%d.lst' % j)

			# one word per line
			for k in xrange(config.listLength):
				listFile.write('%s\n' % state.subjItems[i][j][k])
			listFile.close()



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
