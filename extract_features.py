import sys

def check_arg():
    """
    Check if there are two arguments for this script to execute.
    """

    if len(sys.argv) != 2:
        print '[!] The script should take in two arguments.'
        sys.exit()

def extract_features_from_single_file(file_path):
    """
    Extract features from a single file.

    @param file_path: path to the file
    @type file_path: str


    """

def extract_features_from_single_sent(sent):
    """
    Extract features from a sentence.

    @param sent: a single sentence
    @type sent: str

    @return features extracted from the given sentence.
    @type list
    """
