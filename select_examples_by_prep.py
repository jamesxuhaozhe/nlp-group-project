import sys
import csv

prep_map = {}

source = sys.argv[1]

target = sys.argv[2]

#limit = int(sys.argv[3])

limit = {'of':900, 'in':1000, 'to':1000, 'for':1000, 'with':1000, 'on':900, 'at':800, \
'from':600, 'by':700, 'about':800, 'as':600, 'into':600, 'like':800, \
'through':349, 'after':681, 'over':700, 'between':184, 'out':1000, 'against':319, \
'during':307, 'without':141, 'before':416, 'under':180, 'around':286, 'among':99}

#option = sys.argv[4]

with open(target, 'w') as csvfile_w:
    field_names = ['preposition', 'position', 'sentence']
    writer = csv.DictWriter(csvfile_w, fieldnames=field_names)
    writer.writeheader()
    with open(source) as csvfile_r:
        reader = csv.DictReader(csvfile_r)
        for row in reader:
            prep = row['preposition']
            position = row['position']
            sent = row['sentence']
            if prep in prep_map:

                if prep_map[prep] <= limit[prep]:
                    writer.writerow({'preposition':prep, 'position':position, 'sentence':sent})
                prep_map[prep] += 1
            else:
                prep_map[prep] = 1