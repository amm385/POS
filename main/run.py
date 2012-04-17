from Analyzer import Analyzer
from ngrams import LAPLACE, GOOD_TURING, NONE

train_filename = "../train.pos"
test_filename = "../test-obs.pos"
test_answers = "../POS solution.txt"

isTest = False #false to use CV, true to use test file
smoothing = GOOD_TURING
cv_validation_percentage = .95

def get_score(predicted, actual):
    score = 0.0
    for (p,a) in zip(predicted, actual):
        if p == a:
            score += 1.0
    return score/len(predicted)
    
def main():
    analyzer = Analyzer(isTest,train_filename,test_filename,
                        test_answers,smoothing,cv_validation_percentage)
    (predicted, actual) = analyzer.run()
    accuracy = get_score(predicted,actual)
    print "Accuracy: " + str(accuracy)

if __name__ == '__main__':
    main()