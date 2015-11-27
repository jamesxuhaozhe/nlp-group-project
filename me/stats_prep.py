import sys
import csv

stats = {}
count = 0
with open(sys.argv[1], 'r') as f:
    count = 0
    for line in f:
        count += 1
        prep = line.strip().split()[0]
        if prep in stats:
            stats[prep] += 1
        else:
            stats[prep] = 1

print 'There are %d examples in this file.' % count

for key in stats:
    print key + ' is: ' + str(stats[key])
