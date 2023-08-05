# Configuration for Task Free Recall

"""
This module sets options for running Task Free Recall, a variant of
Free Recall with two encoding tasks (size and animacy judgments).
Each session contains "shift" lists that change task during the list,
and "control" lists that have only one task.

After a number of free recall lists, there is a final free recall
period, then a recognition period begins.  Participants are shown
words and and asked to respond vocally with "pess" if the word was
shown during this session, and "po" if it was not.  After making their
vocal response to a word, they rate their confidence by pressing 1-5
on the keypad.
"""
# experiment structure
nSessions = 4
nLists = 12 # must be a multiple of 4
adjustTrial = 6 # after this trial, get chance to rewet the cap
listLength = 24 # only affects control lists; switch lists are controlled by
                # trainSets
recogTrialLength = 20 # number of items presented in each recognition block
doPracticeLists = True # start session_0 with control S, control L, shift, shift

# stimuli and related statistics
wpfile = '../pools/wasnorm_wordpool.txt'
tnfile = '../pools/wasnorm_task.txt'
wasfile = '../pools/wasnorm_was.txt'

# list creation settings
# see prep.listTaskOrder for an explanation of trainSet settings
trainSets = [None]*2
trainSets[0] = [[2,2,2,6], [2,2,3,5], [2,2,4,4], [2,3,3,4], [3,3,3,3]]
trainSets[1] = [[2,4,6], [2,5,5], [3,3,6], [3,4,5], [4,4,4]]
ratingRange = (.3,.7)
WASthresh = .55
maxTries = 1200

# stimulus display settings
taskText = ['Size', 'Living/Nonliving']
recallStartText = '*******'
wordHeight = .08 # Word Font size (percentage of vertical screen)
defaultFont = '../fonts/Verdana.ttf'

# response keys; task is first, followed by response.
# ((0=size, 1=animacy), (0=small/nonliving, 1=big/living))
# K: big
# L: small
# ,: living
# .: nonliving
respPool = {'K':(0,1), 'L':(0,0), ',':(1,1), '.':(1,0)}

# math distractor settings
doMathDistract = False
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
distractLens = [0,8000,16000]

# recognition period settings
doRecog = True
recogConfig = [[288,42], [252,84], [210,126], [168,168]]
order = [[0,2,3,1], 
         [1,3,2,0], 
         [2,0,1,3], 
         [3,1,0,2],
         [0,3,1,2], 
         [1,2,0,3], 
         [2,1,3,0], 
         [3,0,2,1]]
subjRecogOrder = order[0]
doRecogFeedback = True
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
midSessionBreak = 'text/midFreeRecallBreak.txt'
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

fastConfig = False #Changed to true

if fastConfig: # run fast version to quickly check for errors
    # timing of recall trials
    wordDuration = 10 #30
    msgDur = 15 #150
    wordISI = 40 #80
    jitter = 40 #40
    
    preListDelay = 50 #150
    preRecallDelay = 20 #120
    jitterBeforeRecall = 20 #20
    recallDuration = 3000 #Make this longer for test space press
    
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
