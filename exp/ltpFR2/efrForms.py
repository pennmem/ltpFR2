#!/usr/bin/python

from pyepl.locals import *
import os


def makeStimForms(exp,trialList):
    """ 
    Generate and compile LaTeX code containing a table with each
    trial's words on a row, with checkboxes and fields for keeping
    track of a hospital stim-session.  Currently this can cope with
    trials of list length up to 5.
    """
    print "Making latex form..."
    efrForm = open(os.path.join('./data/',exp.options['subject'],'session_14',exp.options['subject'] + '_efrForm.tex'),'w')
    # how many words per trial:
    wpt = len(trialList[0])
    fontsize = 12
    if wpt>3:
        leftval = -2
        if wpt>4:
            fontsize = 10
    else:
        leftval = -1
    preamble = []
    # right now I don't know how to rotate a longtable, so we're
    # coping with the longer list values (just barely) by increasing
    # the negative margin on the left and shrinking the fontsize.
    preamble.append("\\documentclass[%dpt]{article}\n" % fontsize)
    preamble.append("\\usepackage{amssymb}\n")
    preamble.append("\\usepackage{longtable,lscape}\n")
    preamble.append("\\usepackage{graphicx}\n")
    preamble.append("\\usepackage[left=1in,top=1in,right=1in,bottom=1in,nohead]{geometry}\n")
#    preamble.append("\\setlength{\\oddsidemargin}{%dcm}\n" % leftval)
#    preamble.append("\\setlength{\\evensidemargin}{%dcm}\n" % leftval)
    # technically, we're no longer in the preamble here...
    preamble.append("\\begin{document}\n")
#    preamble.append("\\begin{landscape}\n")
    preamble.append("\\begin{enumerate}\n")
    preamble.append("\\item Subject Code: %s \n" % (exp.options['subject']))
    preamble.append("\\end{enumerate}\n")
    efrForm.writelines(preamble)

    def blanksRow(form, startStr, numCols, back):
        row = startStr + ' & '
        row += '\_\_\_\_\_\_\_ & & & & '*numCols
        row = row[:-back]
        row += '\\\\\n'
        form.write(row)

    currentTrialRangeStart = 0
    # outerloop: make tables of trialsPerPage columns till we've done all trials.
    while currentTrialRangeStart<16:

        # declare 2 columns (word + checkbox) for each word in a trial
        table_format = ''
        numColsToMake = 4#min(config.trialsPerPage, config.numTrials-currentTrialRangeStart)
        table_format = '|cc'*numColsToMake
        efrForm.write("\\begin{longtable}{c%s}\n" % table_format)

        # make column headers:
        headerline = 'trial & '
        for i in range(numColsToMake):
            headerline += '%d & R & ' % (currentTrialRangeStart+i+1)

        headerline = headerline[:-3]
        headerline += '\\\\ \\hline \\hline\n'
        efrForm.write(headerline)

        # now code the table rows
        for j in range(wpt):
            # do each serial position
            thisline = 'word$_{%d}$ & ' % (j+1)
            for i in range(numColsToMake):
                thisline += '%s & $\\square$ & ' % (trialList[i+currentTrialRangeStart][j])#['name'])
            thisline = thisline[:-3] 	# drop the last ampersand
            thisline += '\\\\\n'
            efrForm.write(thisline)

        efrForm.write("\\end{longtable}\n")
        currentTrialRangeStart += numColsToMake
        if currentTrialRangeStart == 8:
            efrForm.write('\\pagebreak')
            prev_words_list = trialList[:8]
            prev_words = []
            for wList in prev_words_list:
                prev_words.extend(wList)
            prev_words.sort()
            efrForm.write("\\scriptsize\n")
            efrForm.write(" ".join(prev_words))
            efrForm.write("\n\n\n")
            efrForm.write("\\normalsize\n")

    efrForm.write('\\pagebreak')
    efrForm.write('\\textbf{Feedback}\n')
    efrForm.write('\\begin{itemize}\n')
    efrForm.write('\\item Participant makes more than 3 intrusions and/or repetitions in a row.\n')
    efrForm.write('\\item Participant says words very loosely related to list items (or asks about free association task).\n')
    efrForm.write('\\item Participant says words related to the current memory task (e.g., memory, experiment, room, etc.).\n')
    efrForm.write('\\end{itemize}\n')            
    
    fb = "``Although the presented words may make you think of other related words, \
    you should not recall all associated words.  Keep in mind that your main task \
    is still to recall as many words as possible from the most recently presented list. \
    \\textbf{Only say other words if they come to mind as you are trying to recall items on \
    the most recently presented list.}''\n"
    efrForm.write(fb)
    efrForm.write('\\begin{itemize}\n')
    efrForm.write('\\item Participant makes fewer than 5 correct responses.\n')
    efrForm.write('\\end{itemize}\n')     
    fb = "``Please keep in mind that your main task is still to recall as many words as \
    possible from the most recently presented list.''"
    efrForm.write(fb)
#    efrForm.write("\\end{landscape}\n")
    efrForm.write("\\end{document}\n")
    efrForm.close()

    # compile the LaTeX
    print "Compiling latex form..."
    os.chdir(os.path.join('./data/',exp.options['subject'],'session_14'))
    command = 'pdflatex %s' % exp.options['subject'] + '_efrForm.tex'
    os.system(command)
    os.system(command) # need to run twice to get formatting right (!?)
    os.chdir('../../../')

# only do this if the experiment is run as a stand-alone program (not imported as a library)
if __name__ == "__main__":
    
    # start PyEPL, parse command line options, and do subject housekeeping
    exp = Experiment()
    exp.parseArgs()
    exp.setup()

    state = exp.restoreState()
#    print state.subjItems
    makeStimForms(exp,state.subjItems[14])