from nltk.tokenize import sent_tokenize
from nltk import wordpunct_tokenize
import sys

"""
1. Detect entences within each line.
2. For each sentence, label it with its preposition usage and also the position of\
preposition.
3. write each sentence example to line.
4. the output file will be like:
like 2 He is a good boy, like he should be.
.......
"""

TOP_50_PREPOSITIONS = ['with', 'at', 'from', 'into', 'during', 'including', 'until', 'against', 'among', \
'throughout', 'despite', 'towards', 'upon', 'concerning', 'of', 'to', 'in', 'for', 'on', 'by', 'about', \
'like', 'through', 'over', 'before', 'between', 'after', 'since', 'without', 'under', 'within', 'along', \
'following', 'across', 'behind', 'beyound', 'plus', 'but', 'up', 'out', 'around', 'down', 'off', 'above', 'near']

TOP_25_PREPOSITIONS = ['of', 'in', 'to', 'for', 'with', 'on', 'at', 'from', 'by', 'about', 'as', 'into', 'like', \
'through', 'after', 'over', 'between', 'out', 'against', 'during', 'without', 'before', 'under', 'around', 'among']

def check_arg():
    """
    Check the validity of the system arguments.
    """

    if len(sys.argv) != 2:
        print 'The script you are running should take in 2 arguments.\
        Should run like this: python script.py whater.data'
        sys.exit()

def begin_work():
    """
    Top level caller function.
    """
    # TODO implement write to file logic
    pass


def extract_examps_from_file(file_path):
    """
    Extract all the example from the given file.

    @param: file_path path the given file
    @type: file_path str

    @return: list of list, each element list contain example sents for a line
    @type: list
    """

    examps = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                examps.append(extract_examps_from_line(line))
    except IOError:
        print 'Something is wrong.'
        pass

    return examps

def extract_examps_from_line(line):
    """
    Extract all the example sents from the given line.

    @param: line each line from the file containing multiple example sents.
    @type: line str

    @return: a list containing all the example sents from the line
    @type: list
    """

    results = []
    preposition_set = init_preposition_set()
    # sentences from a line, in the form of list
    sents = extract_sents_from_line(line)
    for sent in sents:
        sent_tokens = tokenize_sent(sent)
        mem = set()
        for idx, sent_token in enumerate(sent_tokens):
            if sent_token not in preposition_set:
                continue
            if sent_token in mem:
                continue
            mem.add(sent_token)
            results.append(sent_token + ' ' + str(idx) + ' ' + sent)

    return results

def init_preposition_set():
    """
    Initialize the preposition set

    @return: set
    """

    return set(TOP_50_PREPOSITIONS)

def extract_sents_from_line(line):
    """
    Extract sentences from the given line.

    @param: line line that may contain multiple sentences.
    @type: str

    @return: list of sentences
    @type: list
    """

    sents = []

    try:
        sents = sent_tokenize(line)
    except:
        pass

    return sents

def tokenize_sent(sent):
    """
    Tokenize a sentence, including the punctuations.
    All tokens have been lowered.

    @param: sent sentence to be tokenized
    @type: sent str

    @return: a list of tokens for the given sentences
    @type: list
    """

    tokens = []
    lowered_tokens = []
    try:
        tokens = wordpunct_tokenize(sent)
        lowered_tokens = [x.lower() for x in tokens]
    except:
        pass

    return lowered_tokens














