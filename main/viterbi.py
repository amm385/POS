'''
Created on Apr 10, 2012

@author: zach
'''
import HMM
import cProfile
from math import log

SMALL_NUM = 1. ** -100
"""
    TODO:
        - Only use the tags encountered in training, and use smoothing/unknown word 
          handling to deal with unencountered tags
        - Make special tagging rule for numbers that automatically tags them as CD
"""
# pulled from train set
training_tags = ['PRP$', 'VBG', 'VBD', '``', 'VBN', 'POS', "''",
                  'VBP', 'WDT', 'JJ', 'WP', 'VBZ', 'DT', '#',
                   'RP', '$', 'NN', '<s>', 'FW', ',', '.', 'TO',
                    'PRP', 'RB', '-LRB-', ':', 'NNS', 'NNP', 'VB',
                     'WRB', 'CC', 'LS', 'PDT', 'RBS', 'RBR', 'CD',
                      'EX', 'IN', 'WP$', 'MD', 'NNPS', '-RRB-', 'JJS',
                       'JJR', 'SYM', 'UH']

# Penn Treebank Tags + extra tags added for this class
TAGS = training_tags

#set(['CC', 'CD', 'DT', 'EX', 'FW', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 
#        'MD', 'NN', 'NNS', 'NP', 'NPS', 'PDT', 'POS', 'PP', 'PP$', 'RB', 
#        'RBR', 'RBS', 'RP', 'SYM', 'TO', 'UH', 'VB', 'VBD', 'VBG', 'VBN', 
#        'VBP', 'VBZ', 'WDT', 'WP', 'WP$', 'WRB', ',', '.', '<s>', '-RRB-', ]+training_tags)


def viterbi(hmm, filename=None, text=None):
    if filename:
        with open(filename) as fp:
                text = fp.read()
    elif text:
        text = text
    else:
        print "Error: need to pass in either filename or text"
        
    # removes empty tokens
    tokens = filter(lambda x: bool(x), text.split('\n'))
    
    viterbi = {}
    backpointer = {}
    
    # initialization step
    # assumes first token is '<s>'
    assert(tokens[0] == '<s>')
    tokens = tokens[1:]
    for tag in TAGS:
        viterbi[tag] = [log(hmm.getPriorProbability(('<s>', tag)) + SMALL_NUM) + \
                            log(hmm.getLikelihoodProbability(tokens[0], tag)+SMALL_NUM)]
        backpointer[tag] = ['<s>']
    
    # recursion step
    timestep = 0
    for token in tokens[1:]:
        timestep += 1
        if timestep >= 123 and token == 'III':
            pass
        for tag in TAGS:
            if timestep >= 123 and token == 'III' and tag == 'NNP':
                pass    
            # to address issue where 0% likelihood for a given word destroys
            # the rest of the tag sequence
            best_tag = max(TAGS, key=lambda t: viterbi[t][timestep-1] + \
                        log(hmm.getPriorProbability((t, tag))+SMALL_NUM))
            
            if not hmm.isInVocabulary(token):
                vit = viterbi[best_tag][timestep-1]
                pri = log(hmm.getPriorProbability((best_tag, tag))+ SMALL_NUM)
                best_tag_prob = vit + pri
#                best_tag_prob = viterbi[best_tag][timestep-1] * \
#                            hmm.getPriorProbability((best_tag, tag))
            else:
                vit = viterbi[best_tag][timestep-1]
                pri = log(hmm.getPriorProbability((best_tag, tag)) + SMALL_NUM)
                like = log(hmm.getLikelihoodProbability(token, tag) + SMALL_NUM)
                best_tag_prob = vit + pri + like
#                best_tag_prob = viterbi[best_tag][timestep-1] * \
#                                hmm.getPriorProbability((best_tag, tag)) * \
#                                hmm.getLikelihoodProbability(token, tag)
                        
            backpointer[tag].append(best_tag)
            viterbi[tag].append(best_tag_prob)
        
    # backtracing 
    last_timestep = timestep
    cur_tag = max(TAGS, key=lambda t:viterbi[t][last_timestep])
    sequence = [cur_tag]
    for i in range(0, last_timestep+1):
        timestep = last_timestep - i
        cur_tag = backpointer[cur_tag][timestep]
        sequence.insert(0,cur_tag)
    
    return sequence

            