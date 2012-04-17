'''
Created on Apr 11, 2012

@author: zach
'''
from HMM import HiddenMarkovModel
from viterbi import viterbi
from ngrams import NONE, GOOD_TURING, LAPLACE
import cProfile
import time

hmm = HiddenMarkovModel(filename='../train.pos')

filename='test130.txt'
output_filename = "test130-output.txt"
string=\
"""
<s>
Frank
Carlucci
III
was
named
to
this
telecommunications
company
's
board
,
filling
the
vacancy
created
by
the
death
of
William
Sobey
last
May
.
"""

use_filename = True

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
    pos = viterbi(hmm, text=text)
    toc = time.clock()
    print str(pos)
print str(toc-tic)
