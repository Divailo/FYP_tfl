import re # regex library

import stringhelper

# Constants
CONSTANT_SECTION_KEY = "CONST"
ARRAY_SECTION_KEY = "ARRAY"
SECTION_END_KEY = ';'

CYCLE_LENGTH_KEY = "CycleLength"
PLAN_ARRAY_KEY = "((Plan){1}\s*\[{1})\s*\d+\,{1}\s*\d+\s*\]{1}\s*\={1}\s*\[{1}.*\]{1}"

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
            print "Key not found: " + key + " , in file" + file.name
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
                lines.append(stringhelper.escape_vap_comments(line))
        except StopIteration:
            # End of file reached
            file.close()
            return lines

def _extract_timings_from_array_line(arrayline):
    split_found_line = arrayline.split("=")
    remove_brackets_string = stringhelper.remove_brackets_for_vap_array(split_found_line[1])
    all_elements = remove_brackets_string.split(',')
    to_extract = []
    # return all_elements
    x = 9
    try:
        for i in range(x):
            index = i * x
            to_append = stringhelper.parse_integer_from_string(all_elements[index])
            # check for end of timings
            # (technically if the element  to append is less than the previous one, than it is wrong)
            if len(to_extract) > 0:
                last_index = len(to_extract) - 1
                if to_append < to_extract[last_index]:
                    break
            to_extract.append(to_append)

    except IndexError:
        return []

    return to_extract

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
        print "Failed to split the cycle_length line in VAP: " + foundline
    else:
        cycle_length = stringhelper.parse_integer_from_string(value)

    # print "Cycle length = " + cycle_length
    print "END OF FINDING CYCLE LENGTH"

    return cycle_length

# Looks for a single line
def get_stage_lenghts_from_vap(filepath):
    lines = _extract_section_for_key(filepath, ARRAY_SECTION_KEY)
    stages_timing = []
    for line in lines:
        ignore_whitespace_line = line.replace("\s","")
        if re.search(PLAN_ARRAY_KEY, ignore_whitespace_line) is not None:
            found_line = line
            # print "FOUND LINE: " + str(_extract_timings_from_array_line(found_line))
            stages_timing = _extract_timings_from_array_line(found_line)
            break

    return stages_timing
