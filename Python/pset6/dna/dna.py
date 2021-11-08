import csv
import sys

db = sys.argv[1]
sq = sys.argv[2]

database = open(db, "r")
sequence = open(sq, "r")

db_reader = csv.DictReader(database)
sq_reader = csv.reader(sequence)

# create a list of keys to be checked
for row in db_reader:
    keys = list(row.keys())
    keys.remove('name')
    
    # reset the reader line to the begining of the file
    database.seek(0)
    db_reader = csv.DictReader(database)
    break

# setup a dictionary to count the results
for row in db_reader:
    counter = row
    
    # set all values to zero
    for key in keys:
        counter[key] = 0
    counter.pop('name')
    database.seek(0)
    db_reader = csv.DictReader(database)
    break

# setup a dictionary to compare the counted results with each row in db
for row in db_reader:
    results_tmp = row
    
    # set all values to zero
    for key in keys:
        results_tmp[key] = 0
    results_tmp.pop('name')
    database.seek(0)
    db_reader = csv.DictReader(database)
    break

# load the sequence to check all keys
for row in sq_reader:
    
    # convert the read content from list to string
    string = str(row[0])
    
    # iterate over each key
    for key in keys:
        start = 0
        end = len(key)
        tmp_counter = 0
        
        # search for match until the end of the string
        while start <= (len(string)) - len(key):

            # if match is found, increase the counter by 1 and look at the next block of size key
            if string[start:end] == key:
                tmp_counter += 1

                # check if the latest sequence is longer than the current
                if counter[key] < tmp_counter:
                    counter[key] = tmp_counter

                # start at the end of the found match
                start += len(key)
                end = start + len(key)

            # start from the next symbol and reset counter
            else:
                tmp_counter = 0
                start += 1
                end = start + len(key)

# compare the counter results with the database
for row in db_reader:
    
    # on each row compare the results for each key
    for key in keys:
        
        # if the key has a match in the db, mark it in the counter
        if counter[key] == int(row[key]):
            results_tmp[key] = 1

    # check if there is a full match of keys for the given row in the db and print the name
    check = True
    for key in keys:
        if results_tmp[key] != 1:
            check = False

    if check is True:
        print(f"{row['name']}")
        sys.exit
    else:
        for key in keys:
            results_tmp[key] = 0

print(f"No match")

database.close()
sequence.close()