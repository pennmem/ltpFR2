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
