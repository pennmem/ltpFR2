# ltpFR configuration.  BE VERY CAREFUL EDITING!!

"""
This module prepares the lists to be used
in the Spring 2010 LTP multisession experiment.
"""

import random
import prep

def createSessions(subj_no,config):
    """
        For each session i, list j, params[i][j] contains
        (pre-list distractor type,
         end-of-list distractor type)
        Where type is one of 0,1, or 2.

        0: no distractor
        1: math distractor
        2: ??? (profit!)
    """
    params = [[]]*config.nSessions
    all_combos = [(0,1),(1,1)]*2
    for i in range(config.nSessions):
        random.shuffle(all_combos)
        params[i]=tuple(all_combos)
    if len(params)!=config.nSessions:
        print 'WARNING: nSessions IN CONFIG FILE DOES NOT MATCH NUMBER OF SESSIONS IN sessionConfig'
    return params
"""
def createSessions(subj_no,config):

    params = {}

    ## SESSION 0 #########################################################
    # FFR: Yes
    # RECOG: Yes
    # Math: No
    # Externalized FR: No
    # Trials 0-3: No Task
    # Trials 4-7: Task A
    # Trials 8-11: Task B
    # Trials 12-15: Switch

    # create the 4 switch lists
    sLists = prep.switchLists(4,config.trainSets)
    
    tasks = [0,1]
    params[0] = {}
    params[0]['config'] = ['FFR','RECOG','NO MATH','NO EFR']
    params[0]['lists'] = [[['NULL TASK']*16,['NULL MATH']*16],
                            [['NULL TASK']*16,['NULL MATH']*16],
                            [['NULL TASK']*16,['NULL MATH']*16],
                            [['NULL TASK']*16,['NULL MATH']*16],
                            [[tasks[subj_no%2]]*16, ['NULL MATH']*16],
                            [[tasks[subj_no%2]]*16, ['NULL MATH']*16],
                            [[tasks[subj_no%2]]*16, ['NULL MATH']*16],
                            [[tasks[subj_no%2]]*16, ['NULL MATH']*16],
                            [[abs(tasks[subj_no%2]-1)]*16, ['NULL MATH']*16],
                            [[abs(tasks[subj_no%2]-1)]*16, ['NULL MATH']*16],
                            [[abs(tasks[subj_no%2]-1)]*16, ['NULL MATH']*16],
                            [[abs(tasks[subj_no%2]-1)]*16, ['NULL MATH']*16]]

    # append switch lists
    for list in sLists:
        params[0]['lists'].append([list,['NULL MATH']*16])


    ## SESSION 1 #########################################################
    # FFR: Yes
    # RECOG: Yes
    # Math: No
    # Externalized FR: No
    # Trials 0-8: No task, task A, task b triplets in random order
    # Trials 9-16: switch lists starting with task A or task b, random order

    # tasks = ['NULL TASK',0,1]
    # random.shuffle(tasks)
    # tasks = tasks*3
    # params[1] = {}
    # params[1]['config'] = ['FFR','RECOG','NO MATH','NO EFR']
    # params[1]['lists'] = [[[tasks[0]]*16, ['NULL MATH']*16],
    #                         [[tasks[1]]*16, ['NULL MATH']*16],
    #                         [[tasks[2]]*16, ['NULL MATH']*16],
    #                         [[tasks[3]]*16, ['NULL MATH']*16],
    #                         [[tasks[4]]*16, ['NULL MATH']*16],
    #                         [[tasks[5]]*16, ['NULL MATH']*16],
    #                         [[tasks[6]]*16, ['NULL MATH']*16],
    #                         [[tasks[7]]*16, ['NULL MATH']*16],
    #                        [[tasks[8]]*16, ['NULL MATH']*16]]

    # tasks = [[0,0],[0,1],[1,0],[1,1],[0,0],[0,1],[1,0],[1,1]]
    # random.shuffle(tasks)
    # for task in tasks:
    #     taskOrder = prep.listTaskOrder(config.trainSets,task[0],task[1])
    #     params[1]['lists'].append([taskOrder,['NULL MATH']*16])



    ## SESSIONS 1 - 6 ####################################################
    # FFR: 3 out of 6 sessions, randomly chosen
    # RECOG: Yes
    # Math: No
    # Externalized FR: No
    # Trials 0-1: switch lists, alternating which task starts the list
    # Trials 2-15: 4 no task, 3 task A, 3 task B, 4 switch, random order

    # pick FFR sessions
    FFR = ['FFR','FFR','FFR','NO FFR','NO FFR','NO FFR']
    random.shuffle(FFR)

    # define all possible tasks for each session (as descibed above)
    sessionTasks = ['NULL TASK','NULL TASK','NULL TASK','NULL TASK',
                    0,0,0,1,1,1,'S','S','S','S']

    # create each session
    for s, session in enumerate(range(1,7)):

        # randomize task order for session
        random.shuffle(sessionTasks)
        params[session] = {}
        params[session]['config'] = [FFR[s],'RECOG','NO MATH','NO EFR']

        # make lists
        # first two lists always switch
        startTask = random.randint(0,1)
        tasks = [[random.randint(0,1),startTask],[random.randint(0,1),abs(startTask-1)]]
        params[session]['lists'] = []
        for task in tasks:
            taskOrder = prep.listTaskOrder(config.trainSets,task[0],task[1])
            params[session]['lists'].append([taskOrder,['NULL MATH']*16])

        # create the 4 switch lists
        sLists = prep.switchLists(4,config.trainSets)

        # next 14 lists (4 no task, 3 task A, 3 task B, 4 switch)
        for listTask in sessionTasks:
            if listTask == 'S':
                params[session]['lists'].append([sLists.pop(),['NULL MATH']*16])
            elif isinstance(listTask,int):
                params[session]['lists'].append([[listTask]*16,['NULL MATH']*16])
            elif listTask == 'NULL TASK':
                params[session]['lists'].append([[listTask]*16,['NULL MATH']*16])




    ## SESSION 7 #########################################################
    # FFR: Yes
    # RECOG: Yes
    # Math: Yes
    # Trials 0-3: 
    # Externalized FR: No
    #            Math: 2 lists each of (8,8) and (0,8), random order
    #            Task: 2 lists of each task, no switch, random order
    # Trials 4-13:
    #            Math: 2 lists of each of the 5 types - (0,0),(0,8),(0,16),(8,8),(16,16)
    #                  Randomized within each set of 5 distra4ctor types                 
    #            Task: 5 lists of each task, no switch, random order

    # define possible practice tasks and distractors, randomize
    tasksPract = [0,0,1,1]
    distractLensPract = [[8000,8000],[8000,8000],[0,8000],[0,8000]]
    random.shuffle(tasksPract)
    random.shuffle(distractLensPract)

    # define non-practice tasks and distractors, randomize
    tasks = [0]*5 + [1]*5
    random.shuffle(tasks)
    distractLens = []
    for i in range(2):
        distracts = [[0,0], [0,8000], [0,16000], [8000,8000], [16000,16000]]
        random.shuffle(distracts)
        distractLens.extend(distracts)

    # create dictionary for session
    params[7] = {}
    params[7]['config'] = ['FFR','RECOG','MATH','NO EFR']
    params[7]['lists'] = []

    # place practice lists
    for i in range(4):
        params[7]['lists'].append([[tasksPract[i]]*16,
                                   [distractLensPract[i][0]]*16,distractLensPract[i][1]])

    # place non-practice lists
    for i in range(10):
        params[7]['lists'].append([[tasks[i]]*16,[distractLens[i][0]]*16,distractLens[i][1]])



    ## SESSIONS 8 - 15 ###################################################
    # FFR: 4 out of 8 sessions, randomly chosen
    # RECOG: Yes
    # Math: Yes
    # Externalized FR: No
    # Trials 0-1: 
    #            Math: 1 list each of (8,8) and (0,8), random order
    # Trials 2-11:
    #            Math: 2 lists of each of the 5 types - (0,0),(0,8),(0,16),(8,8),(16,16)
    #                  Randomized within each set of 5 distractor types                 
    # Tasks: All 12 trials are randomized order of 6 switch and 6 control

    # pick FFR sessions
    FFR = ['FFR','FFR','FFR','FFR','NO FFR','NO FFR','NO FFR','NO FFR']
    random.shuffle(FFR)

    # define practice distractor types
    distractLensPract = [[8000,8000],[0,8000]]

    # get task type for all lists and sessions
    sessionTasks = prep.prepareSet(8,96) # THIS IS AN ISSUE!!

    # create each session
    for s, session in enumerate(range(8,16)):

        params[session] = {}
        params[session]['config'] = [FFR[s],'RECOG','MATH','NO EFR']
        params[session]['lists'] = []

        # create all possible distractory types and shuffle
        distractLens = []
        for i in range(2):
            distracts = [[0,0], [0,8000], [0,16000], [8000,8000], [16000,16000]]
            random.shuffle(distracts)
            distractLens.extend(distracts)
        random.shuffle(distractLensPract)

        # for control lists, use controlList to create lists
        # for switch lists, use listTaskOrder
        for i in range(12):
            listTask = sessionTasks.pop()
            if isinstance(listTask,int):
                taskOrder = prep.controlList(listTask,16)
            else:
                taskOrder = prep.listTaskOrder(config.trainSets,listTask[0],listTask[1])

            # if is practice, use the defined practice distractor conditions
            if i <= 1:
                listDistract = distractLensPract[i]
            else:
                listDistract = distractLens.pop()

            # append lists
            params[session]['lists'].append([taskOrder,[listDistract[0]]*16,listDistract[1]])



    ## SESSIONS 16 - 19 ####################################################
    # FFR: 2 out of 4 sessions, randomly chosen
    # RECOG: Yes
    # Math: No
    # Externalized FR: No (new for 6/5/12)
    # Trials 0-1: switch lists, alternating which task starts the list
    # Trials 2-15: 4 no task, 3 task A, 3 task B, 4 switch, random order

    # pick FFR sessions
    FFR = ['FFR','FFR','NO FFR','NO FFR']
    random.shuffle(FFR)

    # define all possible tasks for each session (as descibed above)
    sessionTasks = ['NULL TASK','NULL TASK','NULL TASK','NULL TASK',
                    0,0,0,1,1,1,'S','S','S','S']

    # create each session
    for s, session in enumerate(range(16,20)):

        # randomize task order for session
        random.shuffle(sessionTasks)
        params[session] = {}
        params[session]['config'] = [FFR[s],'RECOG','NO MATH','NO EFR']

        # make lists
        # first two lists always switch
        startTask = random.randint(0,1)
        tasks = [[random.randint(0,1),startTask],[random.randint(0,1),abs(startTask-1)]]
        params[session]['lists'] = []
        for task in tasks:
            taskOrder = prep.listTaskOrder(config.trainSets,task[0],task[1])
            params[session]['lists'].append([taskOrder,['NULL MATH']*16])

        # create the 4 switch lists
        sLists = prep.switchLists(4,config.trainSets)

        # next 14 lists (4 no task, 3 task A, 3 task B, 4 switch)
        for listTask in sessionTasks:
            if listTask == 'S':
                params[session]['lists'].append([sLists.pop(),['NULL MATH']*16])
            elif isinstance(listTask,int):
                params[session]['lists'].append([[listTask]*16,['NULL MATH']*16])
            elif listTask == 'NULL TASK':
                params[session]['lists'].append([[listTask]*16,['NULL MATH']*16])

    return params

"""

def vectorizeParams(params):
    
    doFFR = []
    doRecog = []
    doMath = []
    doEFR = []
    subjISI = []
    subjRI = []
    subjTasks = []

    sessions = params.keys()
    for session in sessions:

        sessISI = []
        sessRI = []
        sessTasks = []

        doFFR.append(params[session]['config'][0])
        doRecog.append(params[session]['config'][1])
        doMath.append(params[session]['config'][2])
        doEFR.append(params[session]['config'][3])
        
        for list in params[session]['lists']:
            sessTasks.append(list[0])
            sessISI.append(list[1])
            if len(list) == 3:
                sessRI.append(list[2])
            else:
                sessRI.append('NULL DISTRACT')

        subjISI.append(sessISI)
        subjRI.append(sessRI)
        subjTasks.append(sessTasks)

    return subjISI, subjRI, subjTasks, doFFR, doRecog, doMath, doEFR

































        
