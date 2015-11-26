import sys
import csv

stats = {}
count = 0
with open(sys.argv[1]) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        count += 1
        if count <= 52000:
            prep = row['preposition']
            if prep in stats:
                stats[prep] += 1
            else:
                stats[prep] = 1

print 'There are %d examples in this file.' % count

for key in stats:
    print key + ' is: ' + str(stats[key])
