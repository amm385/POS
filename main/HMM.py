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
        
        self.likelihood_cache, self.prior_cache = {}, {}
        
    def getPriorProbability(self, bigram):
        if bigram not in self.prior_cache:
            self.prior_cache[bigram] = self.bigram_model.get_probability(bigram)
        return self.prior_cache[bigram]
    
    def getLikelihoodProbability(self, word, tag):
        tuple_ = (word,tag)
        if tuple_ not in self.likelihood_cache:
            # this is provisional
            if tag not in self.tag_buckets:
                self.likelihood_cache[tuple_]= 0.
            elif word not in self.tag_buckets[tag]:
                self.likelihood_cache[tuple_]= 0.
            else:
                self.likelihood_cache[tuple_] = \
                float(self.tag_buckets[tag][word])/float(self.tag_counts[tag])
        return self.likelihood_cache[tuple_]