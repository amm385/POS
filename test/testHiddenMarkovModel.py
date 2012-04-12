'''
Created on Apr 9, 2012

@author: zach
'''
from main.HMM import HiddenMarkovModel
import unittest


class Test(unittest.TestCase):

    def setUp(self):
        pass
    def tearDown(self):
        pass

    def testTagList(self):
        filename = "../train-test-prior.pos"
        
        hmm = HiddenMarkovModel(filename=filename)
        
        expected = ('<s>', 'NNP', 'NNP', ',', 'CD', 'NNS', 'JJ', ',', 'MD', 'VB')
        self.assertEquals(hmm.tags, expected)

    def testObservations(self):
        filename = "../train-test-prior.pos"
        
        hmm = HiddenMarkovModel(filename=filename)
        
        expected = ('<s>', 'Pierre', 'Vinken', ',', '61', 'years', 'old', ',', 'will', 'join')
        self.assertEquals(hmm.observations, expected)
        
    def testPriorProbabilities(self):
        filename = "../train-test-prior.pos"
        
        hmm = HiddenMarkovModel(filename=filename)
        self.assertAlmostEqual(hmm.getPriorProbability((',', 'CD')), .5, delta=.1)
    
    @unittest.skip("Skipping")
    def testBuckets(self):
        filename = "../train-test-likelihood.pos"
        hmm = HiddenMarkovModel(filename=filename)
        
        expected = {'<s>':['<s>'], 'NNP': ['Pierre', 'Vinken'], ',':[',',','], 'CD':['61','years','years']}
        self.assertEquals(hmm.tag_buckets, expected)
        
    def testLikelihoodProbabilities(self):
        filename = "../train-test-likelihood.pos"
        hmm = HiddenMarkovModel(filename=filename)
        
        expected = {('<s>', '<s>'):1.0, ('Pierre', 'NNP'):.5, (',',','):1.0, ('years', 'CD'): .666}
        
        for key in expected:
            self.assertAlmostEqual(hmm.getLikelihoodProbability(*key), expected[key], delta=.01)
        
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()