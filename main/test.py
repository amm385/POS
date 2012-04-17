'''
Created on Apr 11, 2012

@author: zach
'''
from HMM import HiddenMarkovModel
from viterbi import viterbi
from ngrams import NONE, GOOD_TURING, LAPLACE
import cProfile
import time

hmm = HiddenMarkovModel(filename='../train.pos', smoothed=LAPLACE)

filename = '../test-obs.pos'
output_filename = "final-test-output.txt"
string=\
"""
<s>
The
U.S.
has
befriended
and
later
turned
against
many
dictators
,
but
none
quite
so
resourceful
.
"""

use_filename = False

#cProfile.run("viterbi(hmm, filename='../test-big-sample.pos')")

tic = time.clock()
if use_filename:
    pos = viterbi(hmm, filename=filename)
    toc = time.clock()
    with open(output_filename, 'w') as fp:
        fp.write('\n'.join(pos))
else:
    text = string 
    #"\n".join(string.split(' '))
    pos = viterbi(hmm, text=text, test=False)
    toc = time.clock()
    print str(pos)
print str(toc-tic)
