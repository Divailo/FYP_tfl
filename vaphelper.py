import re # regex library

import stringhelper

CYCLE_LENGTH_KEY = "CycleLength"

def get_cycle_length_from_vap(filepath):
    global CYCLE_LENGTH_KEY
    file = open(filepath)

    foundline = ""

    for line in file.readlines():
        line = line.strip()
        if stringhelper.does_string_contain_substring(line, CYCLE_LENGTH_KEY) == True:
            foundline = line
            break

    cycle_length = -1
    try:
        key, value = foundline.split("=")
    except ValueError:
        print "Failed to split the cycle_length line in VAP"
    else:
        cycle_length = int(re.search(r'\d+', value).group())

    # print "Cycle length = " + cycle_length
    print "END OF FINDING CYCLE LENGTH"

    return cycle_length