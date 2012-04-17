from Analyzer import Analyzer

train_filename = "../train.pos"
test_filename = "../test-obs.pos"
test_answers = "../POS solution.txt"

isTest = True #false to use CV, true to use test file

def get_score(predicted, actual):
    score = 0.0
    for (p,a) in zip(predicted, actual):
        if p == a:
            score += 1.0
    return score/len(predicted)
    #http://en.wikipedia.org/wiki/Precision_and_recall
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    #http://en.wikipedia.org/wiki/F1_score
    f_measure = 2 * precision * recall / (precision + recall)
    accuracy = (tp + tn) / (tp + tn + fn + fp)
    return f_measure, accuracy  
    
def main():
    analyzer = Analyzer(isTest,train_filename,test_filename,test_answers)
    (predicted, actual) = analyzer.run()
    accuracy = get_score(predicted,actual)
    print "Accuracy: " + str(accuracy)

if __name__ == '__main__':
    main()