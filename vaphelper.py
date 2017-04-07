import re # regex library
import os.path

import stringhelper
import dialoghelper

# Constants
CONSTANT_SECTION_KEY = "CONST"
ARRAY_SECTION_KEY = "ARRAY"
SECTION_END_KEY = ';'

CYCLE_LENGTH_KEY = 'CycleLength'
PLAN_ARRAY_KEY = '((Plan){1}\s*\[{1})\s*\d+\,{1}\s*\d+\s*\]{1}\s*\={1}\s*\[{1}.*\]{1}'


def _give_me_name_for_new_vap_file(name, counter):
    new_name = name + "_pddl_" + str(counter) + '.vap'
    path = dialoghelper.folderpath + '\\' + new_name
    if not os.path.isfile(path):
        return new_name
    else:
        return _give_me_name_for_new_vap_file(name, counter+1)

def _create_vap_file(filepath):
    head, tail = os.path.split(filepath)
    name, extension = tail.split('.')
    new_name_path = dialoghelper.folderpath + '\\' + _give_me_name_for_new_vap_file(name, 1)
    return new_name_path


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
            print "Key not found: " + key + ", in file" + file.name
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
    array_declaration, array_values = arrayline.split("=")
    array_declaration_no_brackets = stringhelper.remove_brackets_for_vap_array(array_declaration)
    array_values_no_brackets = stringhelper.remove_brackets_for_vap_array(array_values)
    to_extract = []
    # find x (the number of elements in each array a 2d array)
    x = stringhelper.parse_integer_from_string(array_declaration_no_brackets.split(',')[1])
    # check if the x is actually extracted
    if x == -1:
        return []
    all_elements = array_values_no_brackets.split(',')
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


def edit_timing_changes(filepath, timings):
    x = len(timings)
    line_to_put = 'Plan[ ' + str(x)+ ', 1 ] = [ '
    for i in range(x - 1):
        line_to_put = line_to_put + '[ ' + timings[i] + ' ]'
        should_put_comma = i == x - 1
        if should_put_comma:
            line_to_put = line_to_put + ', '
    line_to_put = line_to_put + ' ]'

    new_file_path = _create_vap_file(filepath)
    print 'New array: ' + line_to_put + ' to be put in new_file_path'

    with open(filepath, "r") as read_from:
        with open(new_file_path, "w") as write_to:
            for line in read_from:
                write_to.write(re.sub(PLAN_ARRAY_KEY,line_to_put,line))
    # else:
        # print

