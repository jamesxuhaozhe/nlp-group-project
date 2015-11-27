import sys
import numpy as np
import csv
from sklearn.naive_bayes import GaussianNB
from sklearn.externals import joblib

def check_argv():
    """
    Check the validity of the command line arguments, otherwise won't proceed.
    """
    if len(sys.argv) != 4:
        print '[!] Script should take in 3 arguments and it will be like,\
        python script.py features.csv train.dat test.dat'
        sys.exit()

def get_feature_index_range(file_path):
    """
    Find the max index of the features. the index starts from 1
    """
    max_idx = -4
    try:
        with open(file_path) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                index = int(row['index'])
                if index >= max_idx:
                    max_idx = index
    except:
        raise Exception('Something is wrong!!')

    return max_idx

def get_features_and_target_in_good_shape(max_idx, file_path):
    """Generate the feature data and target array ready to be used for
    sklearn."""

    target = []
    features = []
    with open(file_path, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            elements = line.strip().split()
            target.append(int(elements[0]))
            fea_set_per_example = get_fea_set(elements[1:])
            data_per_example = [0 for i in range(max_idx)]
            for idx, element in enumerate(data_per_example):
                if idx in fea_set_per_example:
                    data_per_example[idx] = 1
            features.append(data_per_example)


    return np.array(target), np.array(features)

def gen_model_predict():
    """Create nb model and predict"""
    max_idx = get_feature_index_range(sys.argv[1])
    target, data = get_features_and_target_in_good_shape(max_idx, sys.argv[2])
    test_target, test_data = get_features_and_target_in_good_shape(max_idx, sys.argv[3])
    gnb = GaussianNB()
    y_pred = gnb.fit(data, target).predict(test_data)
    joblib.dump(gnb, 'nb.pkl', compress=True)
    print 'Number of mislabeled points out of a total %d points: %d' % (test_data.shape[0], \
    (test_target != y_pred).sum())
    write_pred(y_pred)

def get_fea_set(elements):
    """Get the feature set.
    elements may be ['1:1', '3:1'], the return result should be set(0, 2)"""

    features = []
    for element in elements:
        features.append(int(element.split(':')[0]) - 1)

    return set(features)

def write_pred(arr):
    """Write the prediction to a file called nb.pred"""
    arr = map(str, arr)
    with open('nb.pred', 'w') as f:
        f.write('\n'.join(arr))

if __name__ == '__main__':
    check_argv()
    gen_model_predict()