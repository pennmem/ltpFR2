#!/bin/bash
# ltpFR.sh; run the Long-Term Participants (LTP) version of Task Free Recall,
# preceded by a session of trackball.

function usage () {
  echo "Usage: $0 [SUBJECT], where:"
  echo "SUBJECT is a subject identifier."
  echo
  echo "e.g.,"
  echo "$ $0 LTP038"
  echo
  echo "This will create sessions of ltpFR2, but not"
  echo "run the first sesssion"
}

LTPFR_DIR=/Users/exp/experiments/ltpFR2/trunk/exp/ltpFR2/
LTPFR_CONFIG="config.py"
ARCHIVE="data"
LOGFILE=session.log
SUBJECT=$1


# only valid to call with 0 or 1 argument
if [[ $# != 0 && $# != 1 ]]
then
  echo "You did not specify a valid set of arguments..."
  usage
  exit 1;
fi

# usage
if [[ $# == 0 ]]
then
  usage
  exit 1;
fi

# we need to specify config and archive, since CDTFR uses the same code
cd $LTPFR_DIR
python makeSubj.py --config=$LTPFR_CONFIG --archive=$ARCHIVE -s $SUBJECT 
