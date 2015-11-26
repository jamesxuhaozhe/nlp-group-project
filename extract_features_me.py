import sys
import os
import csv
import random
from nltk import wordpunct_tokenize
from nltk import pos_tag
import numpy as np

WINDOW_LENGTH = 2

PREPOSITIONS = {'of':1, 'in':2, 'to':3, 'for':4, 'with':5, 'on':6, 'at':7, 'from':8, 'by':9, 'about':10, 'as':11, 'into':12, 'like':13, \
'through':14, 'after':15, 'over':16, 'between':17, 'out':18, 'against':19, 'during':20, 'without':21, 'before':22, 'under':23, 'around':24, 'among':25}

def check_argv():
    if len(sys.argv) != 4:
        print '[!] This program should take in 4 arguments.\
        should look like python script.py source.csv target.dat features.csv'
        sys.exit()

def begin_work():
    """Top level caller"""
    examples = get_examples_from_csv(sys.argv[1])
    features = extract_features_from_examples(examples)
    features = [' '.join(sub_list) for sub_list in features]
    write_features_into_train_file(features)
    write_features_csv()

def write_features_into_train_file(features):
    """Write features into me compatible features"""
    try:
        with open(sys.argv[2], 'w') as f:
            f.write('\n'.join(features))
    except:
        print 'Something is wrong.'
        pass

    print 'Complete writing training file.'

def write_features_csv():
    """Write features into csv file"""
    with open(sys.argv[3], 'w') as csvfile:
        field_names = ['feature', 'index']
        writer = csv.DictWriter(csvfile, fieldnames = field_names)
        writer.writeheader()
        for key in Features_cache.features:
            writer.writerow({'feature': key, 'index': Features_cache.features[key]})

    print 'Complete writing features csv files.'

def get_examples_from_csv(file_path):
    """Read in the csv file and return a list of example objects."""

    examples = []
    with open(file_path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            examples.append(Example(row['preposition'], row['position'], row['sentence']))
    print 'There are %d examples to process in this file.' % len(examples)

    return examples

def extract_features_from_examples(examples):
    """Given a list of Example object, extract features.
    The return will be a list of list [[], [], []....]"""

    features = []
    total_count = 0
    for example in examples[0: min(len(examples), 52000)]:
        feature = extract_features_from_example(example)
        features.append(feature)
        total_count += 1
        if total_count % 1500 == 0:
            print 'Have processed %d examples.' % total_count
    return features

def extract_features_from_example(example):
    """Given one single example, extract features for that."""

    result = []
    label = PREPOSITIONS[example.preposition]
    result.append(label)
    left_window, right_window = get_l_r_window(example)
    pv = pn = fn = False

    # Add lexical features
    if len(left_window) >= 1:
        for pair in left_window:
            if pair[1].startswith('VB'):
                pv = True
                result.append(get_feature_index('PV=' + pair[0].lower()))
            if pair[1].startswith('NN'):
                pn = True
                result.append(get_feature_index('PN=' + pair[0].lower()))
        if len(left_window) == 2:
            result.append(get_feature_index(left_window[0][0].lower() + '-' + left_window[1][0].lower()))
            result.append(get_feature_index(left_window[0][1] + '-' + left_window[1][1]))
    else:
        result.append(get_feature_index('FST'))

    if len(right_window) >= 1:
        for pair in right_window:
            if pair[1].startswith('NN'):
                fn = True
                result.append(get_feature_index('FN=' + pair[0].lower()))
        if len(right_window) == 2:
            result.append(get_feature_index(right_window[0][0].lower() + '-' + right_window[1][0].lower()))
            result.append(get_feature_index(right_window[0][1] + '-' + right_window[1][1]))
    else:
        result.append(get_feature_index('LST'))

    # Add Combination features
    if pv and pn and fn:
        result.append(get_feature_index('PV' + '-' + 'PN' + '-' + 'FN'))
    elif pn and fn:
        result.append(get_feature_index('PN' + '-' + 'FN'))
    elif pv and fn:
        result.append(get_feature_index('PV' + '-' + 'FN'))
    elif pv and pn:
        result.append(get_feature_index('PV' + '-' + 'PN'))

    result = np.array(result)
    result[1:].sort()
    result = map(str, result)

    return result


def get_feature_index(feature):
    """Get the index for the given feature, if the feature exists in cache,
    return the index, if not, increment the index and store the feature, index
    pair in the cache."""

    result = 0
    if feature in Features_cache.features:
        result = Features_cache.features[feature]
    else:
        result = Features_cache.current_index
        Features_cache.features[feature] = result
        Features_cache.current_index += 1

    return result

def get_l_r_window(example):
    """Given an example, return the left and right window"""

    left_window = []
    right_window = []

    position = int(example.position)
    pos_tags = get_pos_tags(example)

    if len(pos_tags[:position]) >= WINDOW_LENGTH:
        left_window = pos_tags[(position - WINDOW_LENGTH) : position]
    else:
        left_window = pos_tags[:position]

    if (len(pos_tags) - position) >= (WINDOW_LENGTH + 1):
        right_window = pos_tags[(position + 1) : (position + 3)]
    elif (len(pos_tags) - position) == WINDOW_LENGTH:
        right_window = pos_tags[(position + 1) :]

    return left_window, right_window

def get_pos_tags(example):
    """Wrapper for pos_tags, with cached functions."""

    sentence = example.sentence
    if sentence == Pos_tags_cache.last_sentence:
        return Pos_tags_cache.last_pos_tags
    else:
        tokens = wordpunct_tokenize(sentence)
        Pos_tags_cache.last_pos_tags = pos_tag(tokens)
        Pos_tags_cache.last_sentence = sentence
        return Pos_tags_cache.last_pos_tags

class Pos_tags_cache(object):
    """Simple data structure to catch the last parsed sentence"""
    last_sentence = ''
    last_pos_tags = []

class Features_cache(object):
    """Simple data structure to hold the seen features"""
    features = {}
    current_index = 1

class Example(object):
    """Simple data structure to represent the example instance."""
    preposition = ''
    position = ''
    sentence = ''

    def __init__(self, preposition, position, sentence):
        self.preposition = preposition
        self.position = position
        self.sentence = sentence

if __name__ == '__main__':
    begin_work()