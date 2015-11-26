import sys
import csv

prep_map = {}

source = sys.argv[1]

target = sys.argv[2]

limit = int(sys.argv[3])

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

                if prep_map[prep] <= limit:
                    writer.writerow({'preposition':prep, 'position':position, 'sentence':sent})
                prep_map[prep] += 1
            else:
                prep_map[prep] = 1