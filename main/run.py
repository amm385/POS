from Analyzer import Analyzer

train_filename = "../train.pos"
test_filename = "../test-obs.pos"

isTest = False #false to use CV, true to use test file

def get_scores(predicted, actual):
    tp, fp, fn, tn = 0., 0., 0., 0.
    for (p,a) in zip(predicted, actual):
        tn += len(tags) - 2
        if p == a:
           tp += 1.
           tn += 1.
        else:
           fp += 1.
           fn += 1.
    #http://en.wikipedia.org/wiki/Precision_and_recall
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    #http://en.wikipedia.org/wiki/F1_score
    f_measure = 2 * precision * recall / (precision + recall)
    accuracy = (tp + tn) / (tp + tn + fn + fp)
    return f_measure, accuracy  
    
def main():
    analyzer = Analyzer(isTest,train_filename,test_filename)
    out = analyzer.run_baseline(train_filename,test_filename)
    '''(predicted, actual) = analyzer.run()
    #(f_measure, accuracy) = get_scores(predicted,actual)
    #print "F1 Score: " + str(f_measure)
    #print "Accuracy: " + str(accuracy)
    score = 0.0
    for i in range(len(predicted)):
        if predicted[i] == actual[i]:
            score += 1.0
    print "Accuracy: " + str(score/len(predicted))
	'''

if __name__ == '__main__':
    main()