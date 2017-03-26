import re # regex library

import stringhelper

# Constants
CONSTANT_SECTION_KEY = "CONST"
ARRAY_SECTION_KEY = "ARRAY"
SECTION_END_KEY = ';'

CYCLE_LENGTH_KEY = "CycleLength"
PLAN_ARRAY_KEY = "Plan"

# checks if the line is end of the section by checking if the line is or ends with ';'
def _check_for_end_of_section(line):
    if line == SECTION_END_KEY or line[-1:] == SECTION_END_KEY:
        return True
    else:
        return False

# extracts the constants section of the vap file
def _extract_section_for_key(filepath, key):
    file = open(filepath)
    line = ""
    while line != key:
        try:
            line = file.next().strip()
        except StopIteration:
            # End of file reached
            print "KEY: " + key + "NOT FOUND IN " + file.name
            file.close()
            return []

    lines = []

    while True:
        try:
            line = file.next().strip()
            # check if the end of the section is reached
            if _check_for_end_of_section(line) == True:
                file.close()
                return lines
            else:
                lines.append(line)
        except StopIteration:
            # End of file reached
            file.close()
            return lines

    file.close()
    return lines

# TODO: try to escape comment lines
# Looks for a single line that contains CycleLength
def get_cycle_length_from_vap(filepath):
    lines = _extract_section_for_key(filepath, CONSTANT_SECTION_KEY)

    foundline = ""

    for line in lines:
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

# Looks for a single line thet
def get_stage_lenghts_from_vap(filepath):
    # TODO
    return []
