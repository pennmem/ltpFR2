# Configuration for Long Term Participants Free Recall

"""
This module sets options for running ltpFR.  This experiment was
specifically designed to run in the ltp (Long Term Participants)
project at the Computational Memory Lab.  Most of the setting are
fairly hardcoded in the file session_config.py.  Do not change anything
in either file unless you are sure of what you are doing.
"""

# experiment structure
nSessions = 20
adjustTrial = 10 # after this trial, get chance to rewet the cap
listLength = 16
recogTrialLength = 20 # number of items presented in each recognition block
# nLists = 12 - 17 depending on the session


# stimuli and related statistics
wpfile = '../pools/wasnorm_wordpool.txt'
tnfile = '../pools/wasnorm_task.txt'
wasfile = '../pools/wasnorm_was.txt'

# list creation settings
trainSets = [ [[2,2,4],[2,3,3]], [[2,6],[3,5],[4,4]] ]
ratingRange = (.3,.7)
WASthresh = .55
maxTries = 1200

# stimulus display settings
taskText = ['Size', 'Living/Nonliving']
recallStartText = '*******'
wordHeight = .08 # Word Font size (percentage of vertical screen)
defaultFont = '../fonts/Verdana.ttf'

# study response keys
# K: big
# L: small
# ,: living
# .: nonliving
respPool = {'K':(0,1), 'L':(0,0), ',':(1,1), '.':(1,0)}

# math distractor settings
doMathDistract = True
MATH_numVars = 3
MATH_maxNum = 9
MATH_minNum = 1
MATH_plusAndMinus = False
MATH_displayCorrect = True
MATH_textSize = .1
MATH_correctBeepDur = 500
MATH_correctBeepFreq = 400
MATH_correctBeepRF = 50
MATH_correctSndFile = None
MATH_incorrectBeepDur = 500
MATH_incorrectBeepFreq = 200
MATH_incorrectBeepRF = 50
MATH_incorrectSndFile = None
MATH_practiceDisplayCorrect = True

# recognition period settings
doRecog = True
recogConfig = [[288,42], [252,84], [210,126], [168,168]]
order = [[0,2,3,1]*5, 
         [1,3,2,0]*5, 
         [2,0,1,3]*5, 
         [3,1,0,2]*5,
         [0,3,1,2]*5, 
         [1,2,0,3]*5, 
         [2,1,3,0]*5, 
         [3,0,2,1]*5]

doRecogFeedback = False
doRecogFeedbackSound = True
recogFeedbackTrainingDir = '~/experiments/trainRec/data/'
recogFeedbackWaitDuration = 350
recogFeedbackDuration = 600
feedbackSoundCorrect = '../sounds/correct.wav'
feedbackSoundIncorrect = '../sounds/incorrect.wav'
feedbackSoundNotRecognized = '../sounds/not_recognized.wav'
recogProgressKey = 'SPACE'
recogCrText = "How confident are you?"
recogRtText = "Your response time was: "

# recognition response keys
confPool = {'[1]':1,'[2]':2,'[3]':3,'[4]':4,'[5]':5}

# Instructions text files
introFirstSess = 'text/introFirstSess.txt'
introSize = 'text/introSize.txt'
introLiving = 'text/introLiving.txt'
introLists = 'text/introLists.txt'
introMathPractice = 'text/introMathPractice.txt'
introRecall = 'text/introRecall.txt'
introSummary = 'text/introSummary.txt'
introSummaryMath = 'text/introSummaryMath.txt'
introGetReady = 'text/introGetReady.txt'

introOtherSess = 'text/introOtherSess.txt'

trialBreak = 'text/trialBreak.txt'
midSessionBreak = 'text/midSessionBreak.txt'
midRecogBreak = 'text/midRecogBreak.txt'

prepareFFR = 'text/prepareFFR.txt'
prepareRecog = 'text/prepareRecog.txt'

instructEFR = 'text/EFR_extra_instruct.txt'
introOtherSessEFR = 'text/introOtherSessEFR.txt'

# Files needed to run the experiment
files = (wpfile,
	 tnfile,
	 wasfile,
	 introFirstSess,
	 introSize,
	 introLiving,
	 introLists,
         introMathPractice,
	 introRecall,
	 introSummary,
	 introSummaryMath,
	 introGetReady,
	 introOtherSess,
         trialBreak,
         midSessionBreak,
         midRecogBreak,
	 prepareFFR,
	 prepareRecog,
         defaultFont)

# experiment timing
fastConfig = True

if fastConfig: # run fast version to quickly check for errors
    # timing of recall trials
    wordDuration = 30
    msgDur = 150
    wordISI = 80
    jitter = 40
    
    preListDelay = 150
    preRecallDelay = 120
    jitterBeforeRecall = 20
    recallDuration = 900
    
    # math timing
    MATH_minProblemTime = 10
    MATH_minDelay = 20
    MATH_practiceMaxDistracterLimit = 3000
    # list of the distractor conditions; ISI, RI tuples
    
    distractLens = ((0,0), (0,8000), (0,16000), (8000,8000), (16000,16000))

    # final free recall
    preffrDelay = 500
    ffrDuration = 5000
    
    # recognition
    recogISI = 24
    recogISI_jitter = 20
    recogFeedbackISI = 24
    recogFeedbackISI_jitter = 20
    recogDurationJitter = 40
    recogMinDuration = 150
    recogMaxDuration = 50

else: # run actual experiment
    # timing of recall trials
    wordDuration = 3000
    msgDur = 1500
    wordISI = 800
    jitter = 400
    
    preListDelay = 1500
    preRecallDelay = 1200
    jitterBeforeRecall = 200
    recallDuration = 90000
    
    # math timing
    MATH_minProblemTime = 1500
    MATH_minDelay = 6000
    MATH_practiceMaxDistracterLimit = 20000
    # list of the distractor conditions; ISI, RI tuples
    distractLens = ((0,0), (0,8000), (0,16000), (8000,8000), (16000,16000))

    # final free recall
    preffrDelay = 5000
    ffrDuration = 360000

    # recognition
    recogISI = 800
    recogISI_jitter = 400
    recogFeedbackISI = 100
    recogFeedbackISI_jitter = 100
    recogDurationJitter = 400
    recogMinDuration = 700
    recogMaxDuration = None

# Beep at start and end of recording (freq,dur,rise/fall)
startBeepFreq = 800
startBeepDur = 500
startBeepRiseFall = 100
stopBeepFreq = 400
stopBeepDur = 500
stopBeepRiseFall = 100

# Realtime configuration
# ONLY MODIFY IF YOU KNOW WHAT YOU ARE DOING!
# HOWEVER, IT SHOULD BE TWEAKED FOR EACH MACHINE
doRealtime = False
rtPeriod = 120
rtComputation = 9600
rtConstraint = 1200

# Have subject recall all items coming to mind, pressing space if they belive an item they said wasn't on a list.       
totalRecall = False
