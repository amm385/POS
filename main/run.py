train_filename = "../train.pos"
test_filename = "../test-obs.pos"
output_file = "../testoutput.txt"

tags = []

def get_tags(filename):
    global tags
    for line in open(filename):
        space = line.find(' ')
        if space == -1:
            #some sort of uncharacteristic line in training file
            continue
        tag = line[:space]
        if tag not in tags:
            tags.append(tag)
    
def run_baseline(filename):
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
    out = open(output_file,"w")
    for line in open(filename):
        space = line.find(' ')
        if space == -1:
            continue
        word = line[space+1:-1]
        maxtag = max(counts[word], key = counts[word].get)
        out.write(maxtag + " " + word + "\n")
    out.close()
        
def main():
    get_tags(train_filename)
    run_baseline(train_filename)    
    print "Done!"

if __name__ == '__main__':
    main()