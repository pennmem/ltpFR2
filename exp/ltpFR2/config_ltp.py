# Configuration for Continuous Distractor Task Free Recall

"""
This module sets options for running Continuous Distractor 
Task Free Recall, a variant of Task Free Recall (AKA apem_e7) 
with a continuous distractor and no recognition period.
"""

# experiment structure
nSessions = 4
nLists = 20 # must be a multiple of 4
adjustTrial = 10 # after this trial, get chance to rewet the cap
listLength = 16
recogTrialLength = None # number of items presented in each recognition block
doPracticeLists = False # start session_0 with control S, control L, shift, shift

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
# Task is first, followed by response.
# ((0=size, 1=animacy), (0=small/nonliving, 1=big/living))
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
doRecog = False
recogConfig = None
subjRecogOrder = None

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
fastConfig = False

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
    #distractLens = [0,800,1600]
    # list of the distractor conditions; ISI, RI tuples
    distractLens = ((0,0), (0,8000), (0,16000), (8000,8000), (16000,16000))
    #distractLens = ((0,0), (0,8), (0,16), (8,8), (16,16)) # easier to visualize

    # final free recall
    preffrDelay = 500
    ffrDuration = 300
    
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
    #distractLens = (0,8000,16000)
    distractLens = ((0,0), (0,8000), (0,16000), (8000,8000), (16000,16000))

    # final free recall
    preffrDelay = 5000
    ffrDuration = 360000

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
