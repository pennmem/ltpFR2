from pyepl import display
from pyepl import sound
from pyepl.keyboard import Key, KeyTrack
from pyepl import joystick
from pyepl.mouse import MouseRoller, MouseButton
from pyepl import keyboard
from pyepl import mechinput
from pyepl import hardware
from pyepl.textlog import LogTrack
from pyepl import exputils

import math, numpy, pygame
from pyepl import timing

def doMathProblem(clk = None,
                 mathlog = None,
                 problemTimeLimit = None,
                 numVars = 2,
                 maxNum = 9,
                 minNum = 1,
                 maxProbs = 400,
                 plusAndMinus = False,
                 minDuration = None,
                 minProblemTime = 2000,
                 textSize = None,
                 correctBeepDur = 500,
                 correctBeepFreq = 400,
                 correctBeepRF = 50,
                 correctSndFile = None,
                 incorrectBeepDur = 500,
                 incorrectBeepFreq = 200,
                 incorrectBeepRF = 50,
                 incorrectSndFile = None,
                 tfKeys = None,
                 ansMod = [0,1,-1,10,-10],
                 ansProb = [.5,.125,.125,.125,.125],
		 visualFeedback = False,
                 maxDistracterLimit = 10000,
                 displayCorrect = False,
                 tcorrect = None):
    """
    Math distractor for specified period of time.  Logs to a math_distract.log
    if no log is passed in.

    INPUT ARGS:
      clk - Optional PresentationClock for timing.
      mathlog - Optional Logtrack for logging.
      problemTimeLimit - set this param for non-self-paced distractor;
                         buzzer sounds when time's up; you get at least
                         minDuration/problemTimeLimit problems.
      numVars - Number of variables in the problem.
      maxNum - Max possible number for each variable.
      minNum - Min possible number for each varialbe.
      maxProbs - Max number of problems.
      plusAndMinus - True will have both plus and minus.
      minDuration - Minimum duration of distractor.
      minProblemTime - NEW TO VAR DISTRACTER:  The amount of time left for this distracter
                       below which we donlt put  a new problem on the screen.
      textSize - Vertical height of the text.
      correctBeepDur - Duration of correct beep.
      correctBeepFreq - Frequency of correct beep.
      correctBeepRF - Rise/Fall of correct beep.
      correctSndFile - Optional Audio clip to use for correct notification.
      incorrectBeepDur - Duration of incorrect beep.
      incorrectBeepFreq - Frequency of incorrect beep.
      incorrectBeepRF - Rise/Fall of incorrect beep
      incorrectSndFile - Optional AudioClip used for incorrect notification.
      tfKeys - Tuple of keys for true/false problems. e.g., tfKeys = ('T','F')
      ansMod - For True/False problems, the possible values to add to correct answer.
      ansProb - The probability of each modifer on ansMod (must add to 1).
      visualFeedback - Whether to provide visual feedback to indicate correctness.
      maxDistracterLimit - NEW TO VAR DISTRACTER: max time the continuous 
                           distracter will go
    """

    # start the timing
    start_time = timing.now()
   
    #convert the distracter limit to an int
    maxDistracterLimit = int(maxDistracterLimit)

    #initialize the ranOutOfTime flag to flase
    ranOutOfTime = False
    
    # print out some debugging information

    # get the tracks
    v = display.VideoTrack.lastInstance()  
    a = sound.AudioTrack.lastInstance()
    k = keyboard.KeyTrack.lastInstance()

    # see if need logtrack
    if mathlog is None:
        mathlog = LogTrack('math_distract')

    # log the start
    mathlog.logMessage('START')
    
    # start timing
    if clk is None:
        clk = exputils.PresentationClock()

    # set the stop time
    if not minDuration is None:
        stop_time = start_time + minDuration
    else:
        stop_time = None
    
    # generate the beeps
    correctBeep = sound.Beep(correctBeepFreq,correctBeepDur,correctBeepRF)
    incorrectBeep = sound.Beep(incorrectBeepFreq,incorrectBeepDur,incorrectBeepRF)
    
    # clear the screen (now left up to caller of function)
    #v.clear("black")

    # generate a bunch of math problems
    vars = numpy.random.randint(minNum,maxNum+1,[maxProbs, numVars])
    if plusAndMinus:
        pm = numpy.sign(numpy.random.uniform(-1,1,[maxProbs, numVars-1]))
    else:
        pm = numpy.ones([maxProbs, numVars-1])

    # see if T/F or numeric answers
    if isinstance(tfKeys,tuple):
        # do true/false problems
        tfProblems = True

        # check the ansMod and ansProb
        if len(ansMod) != len(ansProb):
            # raise error
            pass
        if sum(ansProb) != 1.0:
            # raise error
            pass
        ansProb = numpy.cumsum(ansProb)
    else:
	# not t/f problems 
        tfProblems = False

    # set up the answer button
    if tfProblems:
        # set up t/f keys
        ans_but = k.keyChooser(*tfKeys) #this is a mechinput.buttonchooser object
    else:
        # set up numeric entry
        ans_but = k.keyChooser('0','1','2','3','4','5','6','7','8','9','-','RETURN',
                               '[0]','[1]','[2]','[3]','[4]','[5]','[6]',
                               '[7]','[8]','[9]','[-]','ENTER','BACKSPACE')
    
    # do equations till the time is up
    curProb = 0
#    while not (not stop_time is None and timing.now() >= stop_time) and curProb < maxProbs:
    # This is the first while loop that represents the point when the first equatio is on the 
    # screen and no button has been pressed. 
    while ( (timing.now() - start_time) < maxDistracterLimit):
        # loop over each variable to generate the problem
        probtxt = ''
        for i,x in enumerate(vars[curProb,:]):
            if i > 0:
                # add the sign
                if pm[curProb,i-1] > 0:
                    probtxt += ' + '
                else:
                    probtxt += ' - '

            # add the number
            probtxt += str(x)

        # calc the correct answer
        cor_ans = eval(probtxt)

        # add the equal sign
        probtxt += ' = '

        # do tf or numeric problem
        if tfProblems:
            # determine the displayed answer
            # see which answermod
            ansInd = numpy.nonzero(ansProb >= numpy.random.uniform(0,1))
            if isinstance(ansInd,tuple):
                ansInd = ansInd[0]
            ansInd = min(ansInd)
            disp_ans = cor_ans + ansMod[ansInd]

            # see if is True or False
            if disp_ans == cor_ans:
                # correct response is true
                corRsp = tfKeys[0]
            else:
                # correct response is false
                corRsp = tfKeys[1]

            # set response str
            rstr = str(disp_ans)
        else:
            rstr = ''

        # This is the first time we enter the distracter.  We need to:
	#    (1) Initialize tcorrect to zero if it is not yet defined
	#    (2) create the new text object using this value
	#    (3) display the new text object
        if displayCorrect is True:
            if tcorrect is None:
                tcorrect = 0
	    cortxt = str(tcorrect)
	    ct = v.showProportional(display.Text(cortxt, size = textSize), .8,.1)

        # Now display the problem on the screen
        pt = v.showProportional(display.Text(probtxt,size = textSize),.4,.5)
        rt = v.showRelative(display.Text(rstr, size = textSize),display.RIGHT,pt)
        probstart = v.updateScreen(clk)

        # wait for input
        answer = .12345  # not an int
        hasMinus = False

        # This check will not start a new word unless we have above the time remaining
        maxTimeLeft = maxDistracterLimit - (timing.now() - start_time)
        if maxTimeLeft < minProblemTime:
            #mark that you ran out of time
            ranOutOfTime = True
            timing.wait(int(maxTimeLeft))
            #go all the way down where we log the words
            break
            
        # wait for keypress
        # we wait here while the problem is on the screen and there have been no buttons 
        # pressed.  If the maximuj time is up while we are here, kret = None
        #
        # If the mx time is reached while we are here then...
        #   (1) isCorrect = 0
        #   (2) we jump down to the point where we test if the answer is correct, log the rt
        #       and log the clear the problem that is currently on the screen
        #   (3) We then move to the next pass in the while llop (but that will be 
        #       gaurenteed to be false) so the function exits
        maxTimeLeft = maxDistracterLimit - (timing.now() - start_time)
        kret,timestamp = ans_but.waitWithTime(maxDuration = maxTimeLeft, clock=clk)
        # check to see that we did not run out of time while we waited
        if kret is None:
            ranOutOfTime = True
            break
        
        # process as T/F or as numeric answer
        if tfProblems:            
            # check the answer
            if not kret is None and kret.name == corRsp:
                isCorrect = 1
            else:
                isCorrect = 0
        else:
            # is part of numeric answer
            #
            #  We wait in this loop if we pressed a button.  Currently the problem is on the screen.
            #  Also, in this state the program will display any new keypresses on the screen.
            #  While in this loop we should:
            #  (1) allow the user the rest of the time to try and finish the current problem
            #  (2) clear the current problem if time expires
            #  (3) break out of this loop (This will take you up to the first loop, but the
            #      condition on that loop is guaranteed to be false (b/c time is expired).
            #      So you can just raise the ranOutOfTime flag to make sure that you don't
            #      sound the buzzer before you exit, and then the break statement will cleanly exit 
            #      the function.

            # just because we can, check the timing at this point 
            if ((timing.now() - start_time) >= maxDistracterLimit):
                ranOutOfTime = True
                break

            while kret and \
                      ((kret.name != "RETURN" and kret.name != "ENTER") or \
                       (hasMinus is True and len(rstr)<=1) or (len(rstr)==0)):
                # process the response
                if kret.name == 'BACKSPACE':
                    # remove last char
                    if len(rstr) > 0:
                        rstr = rstr[:-1]
                        if len(rstr) == 0:
                            hasMinus = False
                elif kret.name == '-' or kret.name == '[-]':
                    if len(rstr) == 0 and plusAndMinus:
                        # append it
                        rstr = '-'
                        hasMinus = True
                elif kret.name == 'RETURN' or kret.name == 'ENTER':
                    # ignore cause have minus without number
                    pass
                elif len(rstr) == 0 and (kret.name == '0' or kret.name == '[0]'):
                    # Can't start a number with 0, so pass
                    pass
                else:
                    # if its a number, just append
                    numstr = kret.name.strip('[]')
                    rstr = rstr + numstr

                # check the timing again 
                if ((timing.now() - start_time) >= maxDistracterLimit):
                    ranOutOfTime = True
                    break
                    
                # update the text
                rt = v.replace(rt,display.Text(rstr,size = textSize))
                v.updateScreen(clk)

                # check the timing again 
                if ((timing.now() - start_time) >= maxDistracterLimit):
                    ranOutOfTime = True
                    break

                # wait for the next keyboard input
                maxTimeLeft = maxDistracterLimit - (timing.now() - start_time)
                kret,timestamp = ans_but.waitWithTime(maxDuration =  maxTimeLeft,clock=clk)

                #raise the flag here as well if time expired while we were waiting
                if kret is None:
                    ranOutOfTime = True
                    break


                # check the timing again 
                if ((timing.now() - start_time) >= maxDistracterLimit):
                    ranOutOfTime = True
                    break

            #Now We are out of the loop where we wait while the problem is on the screen
            # check the answer
            if len(rstr)==0 or eval(rstr) != cor_ans:
                isCorrect = 0
            else:
                isCorrect = 1

            # check the timing again 
            if ((timing.now() - start_time) >= maxDistracterLimit):
                ranOutOfTime = True
                break

            # calculate total number correct
            if displayCorrect is True:
                if isCorrect == 1:
                    #increment the correct counter
                    tcorrect = tcorrect + 1
                cortxt = str(tcorrect)
                #update the text
                ct = v.replace(ct,display.Text(cortxt,size = textSize))
		v.updateScreen(clk)

            # check the timing again 
            if ((timing.now() - start_time) >= maxDistracterLimit):
                ranOutOfTime = True
                break
        
        # only play a sound if we did not run out of time
        if not ranOutOfTime:
            # give feedback
            if isCorrect == 1:
                # play the beep
                # pTime = a.play(correctBeep,t=clk,doDelay=False)
                
	        # see if set color of text
                if visualFeedback: 
                    pt = v.replace(pt,display.Text(probtxt,size=textSize,color='green'))
                    rt = v.replace(rt,display.Text(rstr, size=textSize, color='green'))
                    v.updateScreen(clk)
                    clk.delay(correctBeepDur)
            else:
                # play the beep
                pTime = a.play(incorrectBeep,t=clk,doDelay=False)

	        # see if set color of text
                if visualFeedback: 
                    pt = v.replace(pt,display.Text(probtxt,size=textSize,color='red'))
                    rt = v.replace(rt,display.Text(rstr, size=textSize, color='red'))
                    v.updateScreen(clk)
                    clk.delay(incorrectBeepDur)
                    
        # calc the RT as (RT, maxlatency)
        prob_rt = (timestamp[0]-probstart[0],timestamp[1]+probstart[1])
 
        # probstart, PROB, prob_txt, ans_txt, Correct(1/0), RT
        mathlog.logMessage('PROB\t%r\t%r\t%d\t%ld\t%d' %
                           (probtxt,rstr,isCorrect,prob_rt[0],prob_rt[1]),
                           probstart)
        
        # clear the problem
	v.unshow(pt,rt,ct)
        v.updateScreen(clk)
        
        # increment the curprob
        curProb+=1

            
    # clear the problem
    v.unshow(pt,rt,ct)
    v.updateScreen(clk)

    # log the end
    mathlog.logMessage('STOP',timestamp)

    # DEBUGGING: display how much time was actually spent in the distracter
    actualElapsedTime = timing.now() - start_time
#     print 'actualElapsedTime = ', actualElapsedTime

    # finally, return the current state of how many we answered correctly
    return tcorrect


    
    
