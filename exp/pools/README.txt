This directory contains wordpools that have been used with the several
versions of the apem_e7 (AKA Task Free Recall) experiment.

The dev subdirectory contains files related to wordpool development.
The main directory should only contain finalized wordpools.

== norm ==

Used in the norming study, which was done to get an average rating for
size, animacy, and pleasantness judgments for each item in the
original wordpool.

== prac ==

Used in the norming study at the beginning of the first session, to
illustrate how to make the size and animacy judgments.

== wasnorm ==

Used in Task Free Recall LTP and Continuous Distractor Task Free
Recall (CDTFR).  A different wordpool was used than the one in the
original behavioral study or the first (non-LTP) scalp study so that
we could use a wordpool that only included nouns that have Word
Association Space (WAS) scores.

Potential words were screened to make sure they weren't too ambiguous,
either in meaning, or with respect to size or animacy judgments.
Finally, several lab members made both judgements about each word, so
that the judgments on each list could be balanced. Using these data,
we can make sure each list contains a balance of small and big, living
and nonliving items.

The final wordpool is saved in wasnorm_wordpool.txt.  The
corresponding WAS scores and frequency scores are in wpWASfreq.mat.
wasnorm_was.txt contains the cosine distance between each pair of
words in WAS space.  This information is used to make sure that,
within a given list, no two words are too similar.

== Landauer ==


== other ==

NWM: I don't know what the *_taskorder.txt files are.  Perhaps files
that were created as preparation for running a particular subject,
which shouldn't be in the repository?

To remove words from the wordpool files
======================================== 

You can use the following commands to find the line number of a
wordpool word and remove just that line from the wordpool file:

# prints LINENO:WORD
$ grep -in word wordpool.txt

# deletes line LINENO from wordpool.txt
# this modifies wordpool.txt IN PLACE, saving a backup copy to wordpool.txt~
$ sed -i~ -e 'LINENOd' wordpool.txt  
                                
Don't forget to remove the corresponding lines from related files
(e.g., wasnorm_was.txt and wasnorm_task.txt).

NOTE: if you are removing multiple words, do NOT grep for the line
numbers all at once and then try to delete those lines one at a time
-- after you delete one line, all the numbers after it have changed!

Bad Pairings to be fixed are listed here.
=========================================

Bad pairs as of revision 881:
phone/telephone
sun/son
mussel/muscle
steak/stake
hair/hare
gene/jeans
dessert/desert
silver/sliver
pitcher/picture
oar/ore
beach/peach
mare/mayor
gin/gym

The following words were removed in revision 882:
phone
son
muscle
steak
hair
gene
desert
sliver
ore
beach
mayor
pitcher
gin

