import sys
import numpy as np

def check_argv():
    if len(sys.argv) != 3:
        print 'Script should take in 3 arguments, be like script.py source.dat \
        target.data'
        sys.exit()

def get_correct_format_from(file_path):

    result = []
    with open(file_path, 'r') as f:
        for line in f:
            new_line = line.strip()
            if new_line:
                temp_result = []
                lst = new_line.split()
                label = str(int(lst[0]) + 1)
                temp_result.append(label)
                temp = map(int, lst[1:])
                temp = list(set(temp))
                temp = np.array(temp)
                temp.sort()
                for feature in temp:
                    temp_result.append(str(feature) + ':1')
                result.append(' '.join(temp_result))
    return result

def write_to_target(file_path, examples):
    with open(file_path, 'w') as f:
        f.write('\n'.join(examples))

def begin_work():
    examples = get_correct_format_from(sys.argv[1])
    write_to_target(sys.argv[2], examples)

if __name__ == '__main__':
    check_argv()
    begin_work()
