from Analyzer import Analyzer
from ngrams import LAPLACE, GOOD_TURING, NONE

train_filename = "../train.pos"
test_filename = "../test-obs.pos"
test_answers = "../POS solution.txt"

isTest = True #false to use CV, true to use test file
smoothing = NONE
cv_validation_percentage = .95

def get_score(predicted, actual, tokens):
    ten_mistakes = []
    score = 0.0
    for (p,a,t) in zip(predicted, actual, tokens):
        if p == a:
            score += 1.0
        else:
            if len(ten_mistakes) < 10:
                ten_mistakes.append((p,a,t))
    return score/len(predicted), ten_mistakes
    
def main():
    analyzer = Analyzer(isTest,train_filename,test_filename,
                        test_answers,smoothing,cv_validation_percentage)
    (predicted, actual, tokens) = analyzer.run()
    accuracy, ten_mistakes = get_score(predicted,actual, tokens)
    print "Accuracy: " + str(accuracy)
    print "Ten Misclassifications: %s"%str(ten_mistakes)
    
if __name__ == '__main__':
    main()