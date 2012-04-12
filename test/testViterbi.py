'''
Created on Apr 11, 2012

@author: zach
'''
import unittest
from main.HMM import HiddenMarkovModel
from main.viterbi import viterbi

class Test(unittest.TestCase):

    def testViterbiHalfCorrect(self):
        """
            Tests that half of words are classified correctly.
        """
        hmm = HiddenMarkovModel(filename="../train.pos")
        sequence = viterbi(hmm, filename="../test-obs-sample.pos")

        expected = ['<s>', 'NNP', 'NNP', 'NNP', 'POS', 'NNP', 'NN', 'VBD', 'PRP', 'VBD',
                    'DT', 'JJ', 'NN', 'VBG', 'PRP$', 'NN', 'IN', 'NNP', 'NNP', 'TO', 'VB',
                    'JJ', 'NNS', 'IN', 'NNP', 'POS', 'CD', 'NNS', '.']
        
        self.assertEquals(len(sequence), len(expected))
        # number of equal pairs is greater than half
        self.assertGreater(len(filter(lambda x: x[0]==x[1], zip(sequence,expected))), 
                           len(expected)/2)
        
    def testViterbi75PercentCorrect(self):
        """
            Tests that half of words are classified correctly.
        """
        hmm = HiddenMarkovModel(filename="../train.pos") 
        sequence = viterbi(hmm, filename="../test-obs-sample.pos")
    
        expected = ['<s>', 'NNP', 'NNP', 'NNP', 'POS', 'NNP', 'NN', 'VBD', 'PRP', 'VBD',
                    'DT', 'JJ', 'NN', 'VBG', 'PRP$', 'NN', 'IN', 'NNP', 'NNP', 'TO', 'VB',
                    'JJ', 'NNS', 'IN', 'NNP', 'POS', 'CD', 'NNS', '.']
        
        self.assertEquals(len(sequence), len(expected))
        # number of equal pairs is greater than half
        self.assertGreater(len(filter(lambda x: x[0]==x[1], zip(sequence,expected))), 
                           3. * float(len(expected))/ 4.)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testViterbiHalfCorrect']
    unittest.main()