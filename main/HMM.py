from ngrams import Bigram

class HiddenMarkovModel():
    
    def __init__(self, filename=None, text=None, **bigram_parameters):
        
        if filename:
            with open(filename) as fp:
                    self.text = fp.read()
        elif text:
            self.text = text
        else:
            print "Error: need to pass in either filename or text"

        pairs = zip(*[item for item in map(lambda x: x.strip().split(' '), self.text.strip().split('\n')) if item != ''])
        
        self.tags = pairs[0]
        self.observations = pairs[1]
        
        self.tag_buckets = {}
        for index, tag in enumerate(self.tags):
            if tag in self.tag_buckets:
                self.tag_buckets[tag].append(self.observations[index])
            else:
                self.tag_buckets[tag]= [self.observations[index]]
        
        self.bigram_model = Bigram(prepared_tokens=self.tags, **bigram_parameters)
        
    def getPriorProbability(self, bigram):
        return self.bigram_model.get_probability(bigram)
    
    def getLikelihoodProbability(self, word, tag):
        return float(len([item for item in self.tag_buckets[tag] if item == word])) / float(len(self.tag_buckets[tag]))
