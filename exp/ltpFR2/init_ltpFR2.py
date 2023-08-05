#!/usr/bin/python

from pyepl.locals import *
from subprocess import call
from pipes import quote

def remote_exists(host, path):
    """Test if a file exists at path on a host accessible with SSH."""
    print 'Looking for a file at %s:%s' % (host, path)
    status = call(['ssh', host, 'test -f {0}'.format(quote(path))])
    if status == 0:
        return True
    elif status == 1:
        return False
    else:
        return None

# only do this if the experiment is run as a stand-alone program (not imported 
# as a library)
if __name__ == "__main__":
    import sys, re

    # hack around the catch-22 that Experiment.__init__ creates by calling
    # Experiment.setup internally:
    eeg_comp = sys.argv[-1]
    sys.argv = sys.argv[:-1]
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
    eeg_path = '~/UNDEFINED'
    if not exp.restoreState():
        print '******** SUBJECT DOES NOT EXIST ********'
        subj = exp.getOptions().get('subject')
        eeg_path = '/Users/egi/ltp/ltpFR2/%s/session_%d/eeg/%s_session_%d.bdf' % (subj, 0, subj, 0)
    else:
        video = VideoTrack('video')
        keyboard = KeyTrack('keyboard')
        state = exp.restoreState()
        video.clear('black')
        # Display the session number
        subj = exp.getOptions().get('subject')
        sessionText = Text('Subject: %s\nSession: %d'%(subj, state.sessionNum+1)+\
                '\n\nEnsure that eeg recording\n is in the right directory')
        waitForAnyKey(showable = sessionText)

        eeg = exp.eegtrack
        if eeg==None or eeg.record_mode=="N":
            eegText = Text('NO EEG CONNECTED')
        else:
            eegText = Text('EEG CONNECTED')
        waitForAnyKey(showable = eegText)

        eeg_path = '/Users/egi/ltp/ltpFR2/%s/session_%d/eeg/%s_session_%d.bdf' % (subj, state.sessionNum, subj, state.sessionNum)
    
        pyepl.finalize()

    # Verify that EEG file is being saved in the correct location (added by Jesse Pazdera, July 2017)
    print '\nChecking EEG computer for existence of EEG file.'
    eeg_exists = remote_exists(eeg_comp, eeg_path)
    skip = False
    while not eeg_exists and not skip:
        inp = ''

        # If attempt to SSH into the EEG computer failed
        if eeg_exists is None:
            print '**********\nALERT: UNABLE TO SSH INTO EEG COMPUTER %s!\n\nEEG file location cannot be verified. Please double-check that the EEG file is located at %s.\nIf the file was placed in the wrong location, please REMOVE it and start a NEW RECORDING at the correct location.\n' % (eeg_comp, eeg_path)
            while inp not in ('c', 'r'):
                inp = raw_input('Once you have manually verified the location of the EEG file, type c to continue the experiment. Alternatively, type r to retry automatic verification: ').strip().lower()
                if inp == 'c':
                    print 'EEG file manually verified. Proceeding with experiment...'
                    skip = True
                elif inp == 'r':
                    eeg_exists = remote_exists(eeg_comp, eeg_path)
                else:
                    print 'Invalid input!'

        # If file was not detected in proper location
        else:
            print '**********\nALERT: EEG FILE NOT DETECTED!\n\nIt may be saved in the wrong location. Please verify that the EEG file is correctly located at %s.\nIf the file was placed in the wrong location, please REMOVE it and start a NEW RECORDING at the correct location.\n' % eeg_path
            while inp not in ('v', 's'):
                inp = raw_input('Once you have fixed the location of the EEG file, type v to re-verify: ').strip().lower()
                if inp == 'v':
                    eeg_exists = remote_exists(eeg_comp, eeg_path)
                elif inp == 's':
                    print 'SKIPPING EEG FILE VERIFICATION! Proceeding with experiment...'
                    skip = True
                else:
                    print 'Invalid input!'
    
    if eeg_exists:
        raw_input('\nEEG file successfully verified! Hit enter to continue. ')
