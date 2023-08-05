#!/usr/bin/python
from pyepl.locals import *

import pdb
# other modules
import os
import sys
import shutil
import prep
import session_config
from vcdMathMod import doMathProblem
from itertools import chain as itertools_chain

# Set the current version
VERSION = '0.0.1'
MIN_PYEPL_VERSION = '1.0.0'

def prepare(exp, config):
    """
    Prepare the long list of words and tasks.  Randomize the order of
    words.

    Stimuli, which task they will be presented with, distractor
    lengths between each stimulus, and the order of presentation for
    the recognition period are all saved as part of the state vector.
    Once prepare has been run and the state has been saved for a given
    subject, changes to the config file that deal with stimulus
    creation and presentation order will not affect the experiment.

    Inputs
    ------
    exp : Experiment
    config : Configuration
    """
    # verify that we have all the files
    prep.verifyFiles(config.files)

    # get the state
    state = exp.restoreState()

    # copy the word pool to the directory containing these sessions
    try:
        shutil.copy(config.wpfile, exp.session.fullPath())
        shutil.copy(config.excfile, exp.session.fullPath())
    except:
        pass

    # 
    subj_no = int(exp.options['subject'][-2:])
    params = session_config.createSessions(subj_no,config)
    #(subjISI,subjRI,subjTasks,doFFR,doRecog,doMath,doEFR) = session_config.vectorizeParams(params)

    sess_distract_types=[0]*config.nSessions
    for i in range(config.nSessions):
        # concatenates all of the distractor types from a session into a single list, 
        # then removes duplicates (set())
        # to figure out which distractor types are in that session
        sess_distract_types[i] = list(set(itertools_chain(*params[i])))

    # set word order for this subject
    (wp, subjItems, pairDicts, semMat) = prep.subjWordOrder(config)
    # write out all the to-be-presented items to text files ???
    for i, sessionItems in enumerate(subjItems):
        exp.setSession(i)

        for j, listItems in enumerate(sessionItems):
            # each list written to data/[subject]/session_[i]/[j].lst
            listFile = exp.session.createFile('%d.lst' % j)

            # one word per line
            for k in xrange(config.listLength):
                item = subjItems[i][j][k]
                listFile.write('%s\n' % item)
            listFile.close()
        
    random.shuffle(config.taskColors)
    subjColors = config.taskColors
    random.shuffle(config.taskFonts)
    subjFonts = config.taskFonts
    random.shuffle(config.taskCases)
    subjCases = config.taskCases
    
    pairDicts = fixPairDicts(pairDicts, wp, semMat)
    # save the prepared data; set state to first session, block, trial
    exp.saveState(state, 
                  wp=wp, 
                  subjItems=subjItems,
                  pairDicts=pairDicts,
                  sessionNum=0, 
                  blockNum=0, 
                  trialNum=0, 
                  tcorrect=0,
                  subj_distractor=params,
                  sess_distract_types=sess_distract_types,
                  subjColors=subjColors,
                  subjFonts=subjFonts,
                  subjCases=subjCases)

def fixPairDicts(pairDicts, wp, semMat):
    """
    changes the pairDicts structure so that it contains the semantic relatedness
    between the two pairs of words as well as the words themselves.

    Makes it so we don't have to store the semMat in every state file, 
    significantly reducing the size.
    """
    for i, sess_pairDict in enumerate(pairDicts):
        for key in sess_pairDict:
            pair = sess_pairDict[key]
            semValue = semMat[wp.index(key)][wp.index(pair)]
            sess_pairDict[key] = (pair, semValue)
        pairDicts[i] = sess_pairDict

    return pairDicts

def trial(exp,config,clock,bc,state,log,video,audio,mathlog,startBeep,
          stopBeep,fixationCross):
    """
    Present a list of words, followed by a free recall period.

    Inputs
    ------
    exp : Experiment
    config : Configuration
    clock : PresentationClock
    bc : ButtonChooser
    state : 
    log : LogTrack
    video : VideoTrack
    audio : AudioTrack
    mathlog : LogTrack
    startBeep : Beep
    stopBeep : Beep
    fixationCross : Text

    Design
    ------
    This function can run immediate free recall (IFR), delayed free
    recall (DFR), or continuous distractor free recall (CDFR).
    
    Code  Name                     Config Variable
    ----------------------------------------------
    PLD   pre-list delay           preListDelay
    D     distractor               distractLens[i][0]
    W     word presentation        wordDuration
    ISI   inter-stimulus interval  wordISI + jitter
    DF    final distractor         distractLens[i][1]
    PRD   pre-recall delay         preRecallDelay + jitterBeforeRecall
    R     recall period            recallDuration

    Immediate Free Recall:
    PLD W ISI W ISI ... W ISI PRD R

    Delayed Free Recall:
    PLD W ISI W ISI ... W ISI DF PRD R
    
    Continuous Distractor Free Recall:
    PLD D ISI W ISI D ISI W ISI ... D ISI W ISI DF PRD R

    A judgment is made about each word with a button press.  The type
    of judgment to be made is displayed above the word.

    Task and response codes in session.log:
             Response=0  Response=1
    Task=0   big         small
    Task=1   living      nonliving

    If the participant presses a key corresponding to the wrong task,
    the task is logged as task_code + 2.
    """
    # PRE-LIST DISTRACTOR
    pre_distractor = state.subj_distractor[state.sessionNum][state.trialNum][0]
    if pre_distractor>0:
        prev_tcorrect = state.tcorrect
        ts = clock.get()
        if pre_distractor==1:
            state.tcorrect = doMathProblem(
                             clk = clock,
                             mathlog = mathlog,
                             numVars = config.MATH_numVars,
                             plusAndMinus = config.MATH_plusAndMinus,
                             minProblemTime = config.MATH_minProblemTime,
                             textSize = config.MATH_textSize,
                             displayCorrect = config.MATH_displayCorrect,
                             tcorrect = state.tcorrect,
                             maxDistracterLimit = config.MATH_preDistractLength)
        
            # log the retention interval
            log.logMessage('DISTRACTOR_MATH\t%d\t\t\t%d\t%d' % 
                           (state.trialNum, config.MATH_preDistractLength,
                            state.tcorrect-prev_tcorrect), ts)
            # delay post-math, pre-presentation
            clock.delay(config.wordISI, config.jitter);

    # PRESENT THE LIST
    for n in range(len(state.subjItems[state.sessionNum][state.trialNum])):
        # PREPARE STIMULUS
        # prepare item text
        item = state.subjItems[state.sessionNum][state.trialNum][n]
        itemInd = state.wp.index(item) + 1 # itemnos are one-indexed
        
        itemText = Text(item,size=config.wordHeight)
        compStim = CompoundStimulus([('wordName',itemText,'PROP',(.5,.5))])
        taskColor = 'white'
        taskFont = Font(config.defaultFont)
        taskCase = 'upper'
        task = -1
                                        

        # DISTRACTOR
        continual_distractor = state.subj_distractor[state.sessionNum][state.trialNum][1]
        if False and continual_distractor>0:
            prev_tcorrect = state.tcorrect
            #video.clear('black')
            ts = clock.get()
            #video.updateScreen(clock)
            if continual_distractor==1:
                # run the distractor
                clock.wait()
                state.tcorrect = doMathProblem(clk = clock,
                                 mathlog = mathlog,
                                 numVars = config.MATH_numVars,
                                 plusAndMinus = config.MATH_plusAndMinus,
                                 minProblemTime = config.MATH_minProblemTime,
                                 textSize = config.MATH_textSize,
                                 displayCorrect = config.MATH_displayCorrect,
                                 tcorrect = state.tcorrect,
                                 maxDistracterLimit = distractLength)

                # pause after the distractor before we present the next word
                # note: if there is no distractor, there will be no pause
                clock.delay(config.wordISI, config.jitter)

                # log the distraction interval
                n_correct = state.tcorrect - prev_tcorrect;
                log.logMessage('DISTRACTOR_MATH\t%d\t\t\t%d\t%d' % 
                               (state.trialNum, distractLength, 
                                n_correct), ts)
        # PRESENT STIMULUS
        compStim.show()
        # sending in the clock tares the clock
        ts = video.updateScreen(clock)

        if item in state.pairDicts[state.sessionNum]:
            if not isinstance(state.pairDicts[state.sessionNum][item],tuple):
                pair = state.pairDicts[state.sessionNum][item]
                pairDist = state.semMat[state.wp.index(item)][state.wp.index(pair)]
            else:
                pair = state.pairDicts[state.sessionNum][item][0]
                pairDist = state.pairDicts[state.sessionNum][item][1]
            log.logMessage('FR_PRES\t%d\t%s\t%d\t%s\t%.3f'%\
                    (state.trialNum, item, itemInd, pair, pairDist),ts)
        else:
            log.logMessage('FR_PRES\t%d\t%s\t%d'%\
                    (state.trialNum, item, itemInd), ts)
        # delay only affects things with clocks
        clock.delay(config.wordDuration)

        video.clear('black')
        video.updateScreen(clock)
    
        # pause after the distractor before we present the next word
        #if state.subj_distractor[state.sessionNum][state.trialNum][0]=='NULL MATH':
        clock.delay(config.wordISI, config.jitter)

    # END-OF-LIST DISTRACTOR
    eol_distractor = state.subj_distractor[state.sessionNum][state.trialNum][1]
    if eol_distractor>0:
        distractLength = config.MATH_eolDistractLength
        prev_tcorrect = state.tcorrect
        ts = clock.get()
        if eol_distractor==1:
            state.tcorrect = doMathProblem(
                             clk = clock,
                             mathlog = mathlog,
                             numVars = config.MATH_numVars,
                             plusAndMinus = config.MATH_plusAndMinus,
                             minProblemTime = config.MATH_minProblemTime,
                             textSize = config.MATH_textSize,
                             displayCorrect = config.MATH_displayCorrect,
                             tcorrect = state.tcorrect,
                             maxDistracterLimit = config.MATH_eolDistractLength)
        
            # log the retention interval
            log.logMessage('DISTRACTOR_MATH\t%d\t\t\t%d\t%d' % 
                           (state.trialNum, distractLength, 
                            state.tcorrect-prev_tcorrect), ts)

    # Pause before recall
    clock.delay(config.preRecallDelay, config.jitterBeforeRecall)
        
    # RECALL
    # show the recall start indicator
    startText = video.showCentered(Text(config.recallStartText, 
                                   size=config.wordHeight))
    video.updateScreen(clock)
    startBeep.present(clock)
        
    # hide rec start text
    video.unshow(startText)
    video.updateScreen(clock)

    # show the fixation cross
    fix = video.showCentered(fixationCross)
    video.updateScreen(clock)

    # Record responses, log the rec start
    (rec, timestamp) = audio.record(config.recallDuration, str(state.trialNum),
                                        t=clock)
    log.logMessage('REC_START', timestamp)

    # end of recall period
    stopBeep.present(clock)
    video.unshow(fix)
    video.updateScreen(clock)

    clock.delay(1000, 0)


def session_break(config,clock,video):
    """
    Provides the subject with a break between trials of recall.
    """

    # The key to press to pause the countdown 
    pause_bc = ButtonChooser(Key(config.pauseButton))

    trialBreak = open(config.trialBreak,'r').read()

    # Beep at 3,2,1
    shortBeep = Beep(config.countdownBeepShortFreq,
        config.countdownBeepShortDur,
        config.countdownBeepShortRiseFall)
    # Beep at 0
    longBeep = Beep(config.countdownBeepLongFreq,
            config.countdownBeepLongDur,
            config.countdownBeepLongRiseFall)
 
    # The length of the countdown
    timeLeft = config.trialBreakTime
    
    breakText = Text(trialBreak%(timeLeft/1000))
    countdown = video.showCentered(breakText)
    video.updateScreen(clock)
    while timeLeft>0:
        if timeLeft<=3000:
            shortBeep.present(clock)

        # Pause for a second, unless the pause key is pressed
        b = pause_bc.wait(maxDuration=1000, clock=clock)
        timeLeft-=1000

        # If the key is pressed, pause execution until space is pressed
        if b==Key(config.pauseButton):
            pauseText = Text('Press space to continue')
            pauseTextShown = video.showCentered(pauseText)
            video.unshow(countdown)
            video.updateScreen(clock)
            pause_bc.wait(clock=clock)
            video.unshow(pauseTextShown)
            timeLeft = config.trialBreakTime
        
        # show amount of time left on screen
        breakText = Text(trialBreak%(timeLeft/1000))
        video.unshow(countdown)
        countdown = video.showCentered(breakText)
        video.updateScreen(clock)

    video.unshow(countdown)
    timestamp = longBeep.present(clock)
    # Return the time of the end of the break
    return timestamp

def check_impedance(video):
    instructText = Text('Researcher:\nPlease confirm that the \nimpedance window is closed\n'+\
            'and that sync pulses are showing')
    video.clear('black')
    bc = ButtonChooser(Key('Y'))
    video.showCentered(instructText)
    video.updateScreen()
    bc.wait()
    video.clear('black')
 

def run(exp, config):
    """
    Run a session of task free recall/recognition.

    If you break (Esc+F1) during presentation of a list or a recall
    period, starting that subject again will start at the beginning
    of the list.  Any part of the list they already went through
    will be presented again.  This will cause extra lines in the
    logfile; analysis scripts should be prepared to deal with this.

    """
    # set priority
    if config.doRealtime:
        setRealtime(config.rtPeriod, config.rtComputation, config.rtConstraint)
    
    # verify that we have all the files
    prep.verifyFiles(config.files)
    
    # get the state
    state = exp.restoreState()

    # if all sessions have been run, exit
    if state.sessionNum >= config.nSessions:
        print "No more sessions!"
        return
    
    # set the session number, get this session's config file
    exp.setSession(state.sessionNum)
    sconfig = config.sequence(state.sessionNum)

    # create tracks
    video = VideoTrack("video")
    audio = AudioTrack("audio")
    keyboard = KeyTrack("keyboard")
    log = LogTrack("session")
    mathlog = LogTrack("math")

    # set the default font
    setDefaultFont(Font(config.defaultFont))

    # get a presentation clock
    clock = PresentationClock()

    # create the beeps
    startBeep = Beep(config.startBeepFreq,
                     config.startBeepDur,
                     config.startBeepRiseFall)
    stopBeep = Beep(config.stopBeepFreq,
                    config.stopBeepDur,
                    config.stopBeepRiseFall)

    # create the fixation cross
    fixationCross = Text('+', size=config.wordHeight)
    
    # Show what session we're on
    video.clear('black')
    sessionText = Text('Session '+str(state.sessionNum+1))
    waitForAnyKey(clock, sessionText)
    
    # do instructions on first trial of each session
    if state.blockNum == 0 and state.trialNum == 0:
        
        # log start of experiment
        timestamp = clock.get()
        log.logMessage('SESS_START\t%d' % (state.sessionNum + 1), timestamp)

        # do mictest
        video.clear("black")
        soundgood = micTest(2000,1.0)
        if not soundgood:
            return

        video.clear("black")

        if state.sessionNum == 0:
            # show complete instructions
            instruct(open(sconfig.introFirstSess,'r').read())
        else:
            instruct(open(sconfig.introOtherSess,'r').read())

        #elif state.sessionNum != 7 and state.sessionNum < 15 :
        #    instruct(open(sconfig.introOtherSess, 'r').read())
        #    instruct(open(sconfig.introLists,'r').read())
        #elif state.sessionNum > 14 and state.doEFR[state.sessionNum] == 'EFR' :
        #    instruct(open(sconfig.introOtherSess, 'r').read())
        #    instruct(open(sconfig.instructEFR, 'r').read())
        #    instruct(open(sconfig.introLists,'r').read())
        #elif state.sessionNum == 7:
        #    # show briefer instructions
        #    instruct(open(sconfig.introOtherSess, 'r').read())

        # If there is math in this session
        if 1 in state.sess_distract_types[state.sessionNum]:
            # show instructions for the math distractor
            instruct(open(sconfig.introMathPractice,'r').read())
            
            clock.delay(1000)
            #clock.wait()

            # PRACTICE DISTRACTOR
            distractLength = config.MATH_practiceMaxDistracterLimit
            numCorrect = doMathProblem(clk = clock,
                         mathlog = mathlog,
                         numVars = config.MATH_numVars,
                         plusAndMinus = config.MATH_plusAndMinus,
                         minProblemTime = config.MATH_minProblemTime,
                         textSize = config.MATH_textSize,
                         displayCorrect = config.MATH_practiceDisplayCorrect,
                         maxDistracterLimit = distractLength)

            # add math problems to the summary
            instruct(open(sconfig.introRecall,'r').read())
            #if state.sessionNum > 0:
            #    instruct(open(sconfig.sizeColor,'r').read(),color=state.subjColors[0])
            #    instruct(open(sconfig.animColor,'r').read(),color=state.subjColors[1])
            instruct(open(sconfig.introSummaryMath,'r').read())
        else:
            # just give recall instructions and summary
            instruct(open(sconfig.introRecall,'r').read())
            if state.sessionNum > 0:
                instruct(open(sconfig.sizeColor,'r').read(),color=state.subjColors[0])
                instruct(open(sconfig.animColor,'r').read(),color=state.subjColors[1])
                instruct(open(sconfig.introSummary,'r').read())

        # show prepare screen
        instruct(open(sconfig.introGetReady,'r').read())

    # get the screen ready
    video.clear("black")
    video.updateScreen(clock)

    # FREE RECALL
    if state.blockNum == 0:
        # state tells us we're somewhere in the free recall block
        
        # make the buttonchooser
        bkeys = config.respPool.keys()
        bc = ButtonChooser(Key(bkeys[0]), Key(bkeys[1]), 
                           Key(bkeys[2]), Key(bkeys[3]))

        # check if we're still presenting lists
        while state.trialNum < len(state.subjItems[state.sessionNum]):    

            # Countdown to the start of the list
            timestamp = session_break(config, clock,video)
            # log the time the break ended
            log.logMessage('REST', timestamp)
                
            # wait a bit before starting
            crossShown = video.showCentered(fixationCross)
            video.updateScreen(clock)
            clock.delay(config.preListDelay)
            clock.wait()
            video.unshow(crossShown)
            video.updateScreen(clock)

            # run a trial (a trial is a word list plus recall period)
            trial(exp, config, clock, bc, state, log, video, audio, mathlog, 
                  startBeep, stopBeep, fixationCross)
            
            
            # save the state after each trial
            state.trialNum += 1
            exp.saveState(state)

            # display text indicating the break
            if state.trialNum in config.adjustTrials:
                breakText = Text(open(config.midSessionBreak,'r').read())
                timestamp,button,bc_time = breakText.present(clock,None,None,ButtonChooser(Key('RETURN') & Key('SPACE')),None)
                log.logMessage('REST_REWET', timestamp)
                check_impedance(video)

        
        # end of free recall block
        waitForAnyKey(clock,Text("Thank you!\nPlease press RETURN\nto continue."))

        if 1 in state.sess_distract_types[state.sessionNum]:
            log.logMessage('MATH_TOTAL_SCORE\t%d' % state.tcorrect)
    """
    # END OF SESSION
    # set the state for the beginning of the next session
    """
    state.sessionNum += 1
    state.blockNum = 0
    state.trialNum = 0
    state.tcorrect = 0
    exp.saveState(state)

    # tell the participant and the log that we're done
    timestamp = waitForAnyKey(clock, Text("Thank you!\nYou have completed the session.\n\nPress ENTER to exit."))
    if config.writeEndFile == True:
        endFile = open(os.path.join('.',exp.options['archive'],exp.options['subject'],'sess_done'),'w')
        endFile.close()

    log.logMessage('SESS_END', timestamp)

    #clock.wait()


# only do this if the experiment is run as a stand-alone program (not imported 
# as a library)
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

    # make sure we have the min pyepl version
    checkVersion(MIN_PYEPL_VERSION)
    
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
    
    state = exp.restoreState()
    if hasattr(state,'semMat') and len(state.semMat)!=0: 
        state.pairDicts = fixPairDicts(state.pairDicts, state.wp, state.semMat)
        state.semMat=[]
        exp.saveState(state)


    # now run the subject
    run(exp, config)
    
