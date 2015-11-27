from __future__ import division
import sys

PREPOSITIONS = {'of':0, 'in':1, 'to':2, 'for':3, 'with':4, 'on':5, 'at':6, 'from':7, 'by':8, \
'about':9, 'as':10, 'into':11, 'like':12, \
'through':13, 'after':14, 'over':15, 'between':16, 'out':17, 'against':18, 'during':19, 'without':20, \
'before':21, 'under':22, 'around':23, 'among':24}


def check_argv():
    if len(sys.argv) != 4:
        print '[!] The program should take in 3 arguments. test then pred, then train'
        sys.exit()

def begin_work():
    trains = get_labels(sys.argv[1])
    preds = get_labels(sys.argv[2])
    train_size = get_labels(sys.argv[3])
    if len(trains) != len(preds):
        print 'Something is wrong and abort'
        sys.exit()
    evaluate(trains, preds, train_size)

def evaluate(trains, preds, size):
    """Evaluate"""
    prep_map = {}
    for key in PREPOSITIONS:
        prep_map[str(PREPOSITIONS[key])] = key

    eval_map = {}
    class_map = {}
    size_map = {}
    for element in size:
        if element in size_map:
            size_map[element] += 1
        else:
            size_map[element] = 1

    for train, pred in zip(trains, preds):
        if train in class_map:
            class_map[train] += 1
        else:
            class_map[train] = 1
        if train == pred:
            if train in eval_map:
                eval_map[train] += 1
            else:
                eval_map[train] = 1

    print 'preposition, ', 'Numbers in test, ', 'Numbers in train, ', 'Accuracy'
    for key in eval_map:
        print prep_map[key], class_map[key], size_map[key], eval_map[key] / class_map[key]
        print '---------------------------------------------------------'

def get_labels(train_f_path):
    """Return a list of train label"""
    results = []
    with open(train_f_path, 'r') as f:
        for line in f:
            n_line = line.strip()
            if n_line:
                results.append(n_line.split()[0])
    return results

if __name__ == '__main__':
    check_argv()
    begin_work()