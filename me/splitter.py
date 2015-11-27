
# split_data_set.py
# Author: Haozhe Xu<haozhexu@usc.edu>
# Date: Sept.19, 2015
'''
Script which is used to split the given big training data set.

The original big training data set which is labeled should be
split into 75% and 25% fashion. You can select the way you want
to split the data set. If you choose mode 1 then 75% will be training
set and 25% will be dev set. If you choose mode 2 then 25% will be dev
set and 75% will be dev set.

Method used to split the data set: first shuffle the big set and randomly
pick the first 75% and randomly pick the rest.

Available functions:
- check_argv: Check if the command line arguments are valid.

Available classes:
- Split: Object wrapper for splitting the data set.
'''

import sys
import random

def check_argv():
    '''Check the validity of the command line arguments.
    '''
    if len(sys.argv) != 5:
        print('The script is supposed to take in 5 arguments!!!')
        sys.exit(1)

class Split(object):
    '''Represents a wrapper class to process the splitting logic.

    This class is not supposed to be subclassed.
    Clients call do method to process.

    Attributes:
        size(int): Counter that keeps track of the size of the original file set.
        train(list): Stores the splitted train set.
        dev(list): Stores the splitted dev set.
        examples(list): Contains all the examples in the big labeled training set.
        input_file_name(str): File name of the given big labeled training set.
        train_file_name(str): File name of the training set.
        dev_file_name(str): File name of the dev set.
        mode(str): Mode you want to split the original file. It is either '1' or '2'.
                   When '1', 75% -> training, 25% -> dev
                   When '2', 25% -> dev, 75% -> training
    '''
    count = 0
    examples = []
    train = []
    dev = []

    def __init__(self, input_file_name, train_file_name, dev_file_name, mode):
        '''Initializes the object attributes.'''
        self.input_file_name = input_file_name
        self.train_file_name = train_file_name
        self.dev_file_name = dev_file_name
        self.mode = mode

    def _count_len(self):
        '''Calculates the size of the original big labeled set
        and appends all the examples to the attributes examples.'''
        try:
            with open(self.input_file_name, 'r') as f:
                for line in f:
                    if line.strip():
                        self.examples.append(line.strip())
                        self.count += 1
                    else:
                        print('WoW, you have empty line in your original file, fix it!')
        except IOError:
            print('IOError: Something is wrong!!!')

    def _split(self):
        '''Splits the original list into train list and dev list based on the chosen mode
        '''
        random.shuffle(self.examples)
        if self.mode == '1':
            self.train = self.examples[0 : int(self.count * 0.75)]
            self.dev = self.examples[int(self.count * 0.75) : self.count]
        elif self.mode == '2':
            self.train = self.examples[0 : int(self.count * 0.25)]
            self.dev = self.examples[int(self.count * 0.25) : self.count]
        else:
            print('The mode should be either 1 or 2')

    def _write_to_file(self):
        '''Writes the train list and dev list into their separate file.'''
        try:
            with open(self.train_file_name, 'w') as f:
                for t_example in self.train:
                    f.write(t_example + '\n')

            with open(self.dev_file_name, 'w') as w:
                for d_example in self.dev:
                    w.write(d_example + '\n')
        except IOError:
            print('IOError: Something is wrong!!!')

    def do(self):
        '''Calls private methods in correct sequence.'''
        self._count_len()
        self._split()
        self._write_to_file()

if __name__ == '__main__':
    check_argv()
    input_file = sys.argv[1]
    train_file = sys.argv[2]
    dev_file = sys.argv[3]
    mode = sys.argv[4]
    doer = Split(input_file, train_file, dev_file, mode)
    doer.do()
