class Analyzer():
    def __init__(self,isTest,train_filename,test_filename):
        self.train_data = self.parse_file(train_filename)
        self.test_data = self.parse_file(test_filename)
        self.tags = []
        self.isTest = isTest
        
    def parse_file(self,filename):
        with open(filename, 'r') as fp:
            text = fp.read()
        text = map(lambda x: x.strip().split(' '), text.split('\n'))
        return text
    
    def run(self):
        pass
    
    def run_baseline(self, filename):
        # key: word
        # value: dictionary of (tag,tag_count) pairs
        counts = {}
        for line in open(filename):
            space = line.find(' ')
            if space == -1:
                continue
            tag = line[:space]
            word = line[space+1:-1]
            if word not in counts:
                counts[word] = {}
            if tag not in counts[word]:
                counts[word][tag] = 0
            counts[word][tag] += 1
        out = []
        for line in open(filename):
            space = line.find(' ')
            if space == -1:
                continue
            word = line[space+1:-1]
            maxtag = max(counts[word], key = counts[word].get)
            out.append(maxtag)
        return out
    
    def get_tags(self,filename):
        for line in open(filename):
            space = line.find(' ')
            if space == -1:
                #some sort of uncharacteristic line in training file
                continue
            tag = line[:space]
            if tag not in self.tags:
                self.tags.append(tag)
    
    def splitCV(self,data,percent):
        p = len(data)*percent
        self.training_data = data[:p]
        self.validation_data = data[p:]