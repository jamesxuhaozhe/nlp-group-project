import sys
import csv
import os
import language_detector as ld
from nltk import wordpunct_tokenize
from nltk import pos_tag

WINDOW_LENGTH = 2

PREPS = {'of':1, 'in':2, 'to':3, 'for':4, 'with':5, 'on':6, 'at':7, \
'from':8, 'by':9, 'about':10, 'as':11, 'into':12, 'like':13, \
'through':14, 'after':15, 'over':16, 'between':17, 'out':18, 'against':19, \
'during':20, 'without':21, 'before':22, 'under':23, 'around':24, 'among':25}


def start_program():
    """Top level caller, call this to start the program."""

    Features_dict.fea_dict = get_features_map()
    Features_dict.inverse_dict = get_inverse_map()
    while True:
        sent = raw_input('Enter a sentence: ')
        sent = sent.strip()
        if not is_sent_qualified(sent):
            print 'Yo man, you should give me an English sentence and contain\
            some prepositions please.'
            continue
        examples = extract_examples_from_sent(sent)
        features = extract_features_from_examples(examples)
        write_features_into_file(features)
        start_to_predict()
        eval_pred()
        clean_up()

def eval_pred():
    """Evaluate the prediction and print out to console"""
    mines, preds = get_both_labels()
    for mine, pred in zip(mines, preds):
        if mine == pred:
            print 'Preposition [%s] is correct.' % Features_dict.inverse_dict[mine]
        else:
            print 'Preposition [%s] is incorrect, and it should be [%s].' % \
            (Features_dict.inverse_dict[mine], Features_dict.inverse_dict[pred])

def clean_up():
    """Delete all the intermediate result."""

    os.system('rm *.app')

def get_both_labels():
    """Get both mine and pred_labels"""

    mines = []
    preds = []
    with open('app_test.app', 'r') as f:
        for line in f:
            mines.append(int(line.strip().split()[0]))
    with open('pred.app', 'r') as f:
        for line in f:
            preds.append(int(line.strip().split()[0]))

    return mines, preds


def start_to_predict():
    """Use python os.system module to call svm_multiclass_classify
    precision goes to precicion.app, the predicion goes to pred.app"""

    os.system('svm_multiclass_classify app_test.app svm.model pred.app > prec.app')

def write_features_into_file(features):
    """Write features into file."""

    try:
        with open('app_test.app', 'w') as f:
            f.write('\n'.join(features))
    except:
        print 'Something is wrong when writing into test file.'
        pass

def extract_examples_from_sent(sent):
    """Extract prep usage example from the sentence."""

    results = []
    preposition_set = init_prep_set()
    tokens = get_tokens_from_sent(sent)
    mem = set()
    for idx, token in enumerate(tokens):
        if token not in preposition_set:
            continue
        if token in mem:
            continue
        mem.add(token)
        results.append(Example(token, str(idx), sent))

    return results

def extract_features_from_examples(examples):
    """Extract a list of features from examples.
    for instance, examples = [example1, example2..]
    return will be features = ['1 1:1 2:1 3:1','2 2:1 3:1 4:1'...]"""

    features = []
    for example in examples:
        feature = extract_feature_from_example(example)
        features.append(feature)

    return features

def extract_feature_from_example(example):
    """Extract feature for single example. Return will be '1 1:1 2:1 3:1'"""

    result = []
    result.append(str(PREPS[example.preposition]))
    left_win, right_win = get_l_r_window(example)
    pv = pn = fn = False

    feature_temp = []
    # Add lexical features
    if len(left_win) >= 1:
        for pair in left_win:
            if pair[1].startswith('VB'):
                pv = True
                feature_temp.append('PV=' + pair[0].lower())
            if pair[1].startswith('NN'):
                pn = True
                feature_temp.append('PN=' + pair[0].lower())
        if len(left_win) == 2:
            feature_temp.append(left_win[0][0].lower() + '-' \
            + left_win[1][0].lower())
            feature_temp.append(left_win[0][1] + '-' + \
            left_win[1][1])
    else:
        feature_temp.append('FST')

    if len(right_win) >= 1:
        for pair in right_win:
            if pair[1].startswith('NN'):
                fn = True
                feature_temp.append('FN=' + pair[0].lower())
        if len(right_win) == 2:
            feature_temp.append(right_win[0][0].lower() + '-' +\
            right_win[1][0].lower())
            feature_temp.append(right_win[0][1] + '-' + \
            right_win[1][1])
    else:
        feature_temp.append('LST')

    # Add Combination features
    if pv and pn and fn:
        feature_temp.append('PV' + '-' + 'PN' + '-' + 'FN')
    elif pn and fn:
        feature_temp.append('PN' + '-' + 'FN')
    elif pv and fn:
        feature_temp.append('PV' + '-' + 'FN')
    elif pv and pn:
        feature_temp.append('PV' + '-' + 'PN')

    encoded_features = get_encode_feature(feature_temp)
    result.extend(encoded_features)

    return ' '.join(result)


def get_encode_feature(feature_strs):
    """Transform the string form of feature into number """
    result = []
    for feature_str in feature_strs:
        if feature_str not in Features_dict.fea_dict:
            continue
        num = Features_dict.fea_dict[feature_str]
        result.append(num)
    if not result:
        return ['1:1', '2:1', '3:1', '4:1']
    result = list(set(result))
    result = sorted(result)

    return [str(x) + ':1' for x in result]

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

class Pos_tag_cache(object):
    last_sent = ''
    last_pos_tags = []

def get_pos_tags(example):
    """Wrapper for pos_tags, with cached functions."""

    result = []
    if example.sent == Pos_tag_cache.last_sent:
        result = Pos_tag_cache.last_pos_tags
    else:
        result = pos_tag(wordpunct_tokenize(example.sent))
        Pos_tag_cache.last_sent = example.sent
        Pos_tag_cache.last_pos_tags = result

    return result

class Example(object):
    """Simple data structure to hold an example."""
    preposition = ''
    position = ''
    sent = ''

    def __init__(self, prep, pos, sent):
        self.preposition = prep
        self.position = pos
        self.sent = sent

def get_tokens_from_sent(sent):
    """Get wordpunct tokens from the sentence"""

    return [x.lower() for x in wordpunct_tokenize(sent)]

def init_prep_set():
    """Get a set of wanted prep"""

    prep_set = set()
    for key in PREPS:
        prep_set.add(key)

    return prep_set

def is_sent_qualified(sent):
    """Check if the sentence makes sense for us to process/proceed.
    qualification1: is it English?
    qualification2: does it contain any prep that falls into our 25 preps?"""

    return is_sent_english(sent) and contain_prep(sent)

def is_sent_english(sent):
    """Check if the sentence is English or not"""

    return ld.detect_language(sent) == 'english'

def contain_prep(sent):
    """Check if the sentence contain wanted prep"""

    does_contain = False
    tokens = wordpunct_tokenize(sent)
    for token in tokens:
        if token.lower() in PREPS:
            does_contain = True
            break

    return does_contain

def get_features_map():
    """Read the feature map from features.csv and return the map."""

    features_dict = {}
    try:
        with open('features.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                features_dict[row['feature']] = int(row['index'])
    except:
        print 'Something is wrong when reading the features.csv.'
        pass

    return features_dict

def get_inverse_map():

    inverse_map = {}
    for key in PREPS:
        inverse_map[PREPS[key]] = key

    return inverse_map

class Features_dict(object):
    fea_dict = {}
    inverse_dict = {}

if __name__ == '__main__':
    start_program()