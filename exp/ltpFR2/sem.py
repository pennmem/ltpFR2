def buildSessions(sessionConfig)


def subjTaskAndDistractor(nSessions, nLists, listLength, distractLens, 
                          trainSets, tasks=[0,1]):
    """
    Determine task and distractor structure for one subject.

    Task structure is balanced for each length of distractor.  Each
    distractor length has the same number of control lists, with equal
    numbers of each type of control lists, and the same number of
    switch lists.

    There are four types of switch lists.  Switch lists are made to be
    balanced within the subject and as balanced as possible within each
    session.

    If the number of sessions and lists per session is incompatible
    with balancing within subject, an error will be thrown.

    Inputs
    ------
    nSessions : int
        The number of sessions.
    nLists : int
        The number of lists in each session.
    listLength : int
        The number of items in each list.
    distractLens : tuple of tuples
        A tuple of the possible distractor conditions that are to be
        balanced across lists.  Each element is an (ISI, RI) tuple,
        where ISI is the interstimulus interval in milliseconds, and
        RI is the retention interval in milliseconds.
    trainSets : list
        Specifies the lengths of the "trains", or sets, of same-task
        items that are presented on switch lists.  See listTaskOrder
        for details.
    tasks : list, optional
        Gives the labels to be used for the different tasks.

    Outputs
    -------
    subjISI : list of lists of lists of ints
        The interstimulus interval for the item in session i, list j,
        item k is subjISI[i][j][k].
    subjRI : list of lists of ints
        The retention interval at the end of session i, list j is
        subjRI[i][j]
    subjTask : list of lists of lists of ints
        The task for the item in session i, list j, item k is
        subjTask[i][j][k].

    See Also
    --------
    subjTaskOrder: use this if there is no distractor; it uses task
        condition to set the order of lists.  subjTaskAndDistractor
        uses distractor condition to set list order; task conditions,
        while balanced, are in random order within each session.
    """

    print 'Preparing subject...'

    # input checks
    if not (nLists % len(distractLens)) == 0:
        raise ValueError("Number of lists per session must be divisible by "
                         "the number of distractor conditions, so distractor "
                         "conditions will be balanced within each session.")
    elif not ((nLists / len(distractLens)) % 2) == 0:
        raise ValueError("Number of lists per set must be a multiple of 2, so "
                         "control and shift lists will be balanced within each "
                         "distractor condition.")
    elif not ((nLists / len(distractLens)) % 4) == 0:
        raise ValueError("Number of lists per set must be a multiple of 4, so "
                         "each distractor length has all task conditions.")
    elif not (((nLists / 2) * nSessions) % 4) == 0:
        raise ValueError("Number of lists must be a multiple of 4, so task "
                         "conditions will be balanced.")

    # calculate some constants
    nDistracts = len(distractLens)
    listsPerSet = (nLists * nSessions) / nDistracts

    # for each distractor condition, plan to have one of each task condition
    sets = []
    for j in range(nDistracts):
        sets.append(prepareSet(nSessions, listsPerSet))

    subjISI = []
    subjRI = []
    subjTask = []
    for i in range(nSessions):
        print 'Session ' + str(i)
        # get the distractor structure for this session
        (sessISI, sessRI) = sessDistractor(nLists, listLength, distractLens)

        sessTask = []
        for j in range(nLists):
            # translate distractor length to index of distractLens
            distractor = (sessISI[j][0], sessRI[j])
            distractInd = list(distractLens).index(distractor)

            # get the next list type for this distractor
            listType = sets[distractInd].pop(0)

            # set the task structure for this list
            if listType in tasks:
                # control list
                sessTask.append(controlList(listType, listLength))
            else:
                # switch list
                listTask = listTaskOrder(trainSets, listType[0], listType[1])
                sessTask.append(listTask)
        subjTask.append(sessTask)
        subjISI.append(sessISI)
        subjRI.append(sessRI)

    return subjISI, subjRI, subjTask































def listStats(tasks,sems):
    """
    SUCH BEAUTIFUL CODE
    """
    import numpy
    sameTask = 0
    diffTask = 0
    sameTrain = 0
    session = 0
    for taskSess in tasks:
        list = 0
        for taskList in taskSess:
            if len(numpy.unique(taskList)) == 1:
                list += 1
                continue
            semList = sems[session][list]
            sameTask += (len(semList[taskList==1]) - len(numpy.unique(semList[taskList == 1])))
            sameTask += (len(semList[taskList==0]) - len(numpy.unique(semList[taskList == 0])))
            diffTask += len(numpy.intersect1d_nu(semList[taskList==0],semList[taskList==1]))
            for item in numpy.unique(semList[taskList==1]):
                inds = numpy.nonzero(semList[taskList==1]==item)[0]
                if len(inds) == 2 and abs(inds[0] - inds[1]) == 1:
                    sameTrain += 1
            for item in numpy.unique(semList[taskList==0]):
                inds = numpy.nonzero(semList[taskList==0]==item)[0]
                if len(inds) == 2 and abs(inds[0] - inds[1]) == 1:
                    sameTrain += 1
            list += 1
        session += 1
    print sameTask
    print diffTask
    print sameTrain
