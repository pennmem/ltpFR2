#!/usr/bin/python

from ltpFR2 import prepare
from pyepl.locals import *


if __name__ == "__main__":
    import sys, re

    # hack around the catch-22 that Experiment.__init__ creates by calling
    # Experiment.setup internally:
    arg_string = ''
    for arg in sys.argv:
        arg_string += arg

    arch_re = re.compile('archive=')
    if not arch_re.search(arg_string):
        raise ValueError("You didn't pass an archive! I need to be able to find any previous sessions for this version of the experiment.")

    # start PyEPL, parse command line options, and do subject housekeeping
    exp = Experiment()

    # get subj. config
    config = exp.getConfig()

    # allow users to break out of the experiment with escape-F1 
    # (the default key combo)
    exp.setBreak()

    # if there was no saved state, run the prepare function
    if not exp.restoreState():
        print "*** CREATING NEW SUBJECT ***"
        prepare(exp, config)
    else:
        print "SUBJECT ALREADY EXISTS"

