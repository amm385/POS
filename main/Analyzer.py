from viterbi import viterbi
from HMM import HiddenMarkovModel
from ngrams import LAPLACE, GOOD_TURING, NONE

CV_VALIDATION_PERCENTAGE = .99995
SMOOTHING = LAPLACE 

class Analyzer():
    def __init__(self,isTest,train_filename,test_filename,test_answers,
                    smoothing = LAPLACE):
        self.train_file = train_filename
        self.test_file = test_filename
        self.test_answers = test_answers
        self.tags = ['PRP$', 'VBG', 'VBD', '``', 'VBN', 'POS', "''",
                  'VBP', 'WDT', 'JJ', 'WP', 'VBZ', 'DT', '#',
                   'RP', '$', 'NN', '<s>', 'FW', ',', '.', 'TO',
                    'PRP', 'RB', '-LRB-', ':', 'NNS', 'NNP', 'VB',
                     'WRB', 'CC', 'LS', 'PDT', 'RBS', 'RBR', 'CD',
                      'EX', 'IN', 'WP$', 'MD', 'NNPS', '-RRB-', 'JJS',
                       'JJR', 'SYM', 'UH']
        self.isTest = isTest
        self.smoothing = smoothing
    
    def parse_file(self,filename):
        with open(filename, 'r') as fp:
            text = fp.read()
        text = map(lambda x: x.strip().split(' '), text.split('\n'))
        return text
    
    def run(self):
        if self.isTest:
            print "Running HMM"
            h = HiddenMarkovModel(self.train_file,smoothed=self.smoothing)
            print "Running Viterbi"
            predicted = viterbi(h,self.test_file, test = False)
            actual = self.getActual(self.parse_file(self.test_answers))
            return (predicted,actual)
        else:
            print "Splitting Data"
            (train,test) = self.splitCV(self.parse_file(self.train_file),CV_VALIDATION_PERCENTAGE)
            print "Converting Lists"
            train_text = "".join(["%s %s\n" % (p,t) for [p,t] in train])
            test_text = "".join(["%s\n" % t for [p,t] in test])
            print "Running HMM"
            h = HiddenMarkovModel(text=train_text, smoothed=self.smoothing)
            print "Running Viterbi"
            predicted = viterbi(h,text=test_text, test=False)
            actual = self.getActual(test)
            return (predicted,actual)
    
    def getActual(self,list):
        return [p for [p,t] in list]
    
    def run_baseline(self, train_file, test_file):
        # key: word
        # value: dictionary of (tag,tag_count) pairs
        counts = {}
        for line in open(train_file):
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
        file = open("../testoutput.txt","w")
        for line in open(test_file):
            word = line[:-1]
            if word not in counts:
                maxtag = "NN"
            else:
                maxtag = max(counts[word], key = counts[word].get)
            out.append(maxtag)
            file.write(maxtag + " " + word + "\n")
            #print (word,maxtag)
        file.close()
        return
    
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
        p = int(len(data)*percent)
        p += data[p:].index(['<s>','<s>'])
        return (data[:p],data[p:-1])