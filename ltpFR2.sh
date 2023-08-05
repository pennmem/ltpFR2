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
  echo "This will run subject LTP038 in a session of trackball,"
  echo "followed by a session of Task Free Recall."
}

# hard-coded; must modify for machine/screen running LTP experiments
#TRACKBALL_DIR=~/experiments/trackball
TRACKBALL_DIR=/Volumes/MacintoshHD3/experiments/trackball/
#LTPFR_DIR=~/experiments/ltpFR/exp/ltpFR
LTPFR_DIR=/Users/exp/experiments/ltpFR2/trunk/exp/ltpFR2/
#LTPFR_DIR=./exp/ltpFR2/
TRAINREC_DIR=~/experiments/trainRec/
#TRAINREC_DIR=/Volumes/MacintoshHD3/experiments/trainRec/
#RESOLUTION="1280x1024"
#RESOLUTION="1600x1000"
RESOLUTION="1680x1050"
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

# run trainRec if this is the subject's first session
#if [[ ! -d $TRAINREC_DIR/data/$SUBJECT ]]
#then
#    echo -e "\nTrain rec data does not exist for $SUBJECT"
#    echo -n "Please enter PLTP subject number and press return "
#    echo "or just press enter to tun train rec"
#    read PLTP
#    if [[ `echo ${#PLTP}` == 0 ]]
#    then
#        cd $TRAINREC_DIR
#        python trainRec.py  --resolution=$RESOLUTION -s $SUBJECT;
#    else
#        if [[ ! -d $TRAINREC_DIR/data/$PLTP ]]
#	then
#	    echo "No train rec data for $PLTP"
#            echo "Running train rec"
#            cd $TRAINREC_DIR
#            python trainRec.py  --resolution=$RESOLUTION -s $SUBJECT;
#        else
#            echo "copying $TRAINREC_DIR/data/$PLTP"
#            echo "to $TRAINREC_DIR/data/$SUBJECT"
#            cp -r $TRAINREC_DIR/data/$PLTP $TRAINREC_DIR/data/$SUBJECT
#        fi
#    fi
#fi
#
## run trackball; use the same subject id as we're using for taskFR
#cd $TRACKBALL_DIR
#python trackball.py --resolution=$RESOLUTION -s $SUBJECT

# we need to specify config and archive, since CDTFR uses the same code
cd $LTPFR_DIR
python ltpFR2.py --resolution=$RESOLUTION --config=$LTPFR_CONFIG --archive=$ARCHIVE -s $SUBJECT 
#if [[ -e ./$ARCHIVE/$SUBJECT/sess_done ]]; then
#    rm ./$ARCHIVE/$SUBJECT/sess_done
#    ~/bin/ltpFR_upload.sh
#fi

# make a link from the trackball session directory to the session we just ran
#trackball_link.sh $TRACKBALL_DIR/data $LTPFR_DIR/$ARCHIVE $LOGFILE $SUBJECT
