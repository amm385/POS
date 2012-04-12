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

        pairs = zip(*map(lambda x: x.strip().split(' '), \
                           filter(bool, self.text.strip().split('\n'))))
        
        self.tags = pairs[0]
        self.observations = pairs[1]
        
        self.tag_buckets = {}
        self.tag_counts = {}
        for index, tag in enumerate(self.tags):
            if tag in self.tag_buckets:
                self.tag_counts[tag] += 1
                if self.observations[index] in self.tag_buckets[tag]:
                    self.tag_buckets[tag][self.observations[index]] += 1
                else:
                    self.tag_buckets[tag][self.observations[index]] = 1
#                self.tag_buckets[tag].append(self.observations[index])
            else:
                self.tag_counts[tag] = 1
                self.tag_buckets[tag]= {self.observations[index]: 1}
        
        self.bigram_model = Bigram(prepared_tokens=self.tags, **bigram_parameters)
        
    def getPriorProbability(self, bigram):
        return self.bigram_model.get_probability(bigram)
    
    def getLikelihoodProbability(self, word, tag):
        # this is provisional
        if tag not in self.tag_buckets:
            return 0.
        if word not in self.tag_buckets[tag]:
            return 0
#        return float(len(filter(lambda x: x==word,self.tag_buckets[tag]))) \
#                / float(len(self.tag_buckets[tag]))
        return float(self.tag_buckets[tag][word])/float(self.tag_counts[tag])