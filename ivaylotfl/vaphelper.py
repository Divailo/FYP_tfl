import re  # regex library
import os.path
from datetime import datetime
import logging

import stringhelper
import dialoghelper

# Constants
CONSTANT_SECTION_KEY = 'CONST'
ARRAY_SECTION_KEY = 'ARRAY'
SECTION_END_KEY = ';'

CYCLE_LENGTH_KEY = r'(CycleLength){1}\s*=\s*\d+'
PLAN_ARRAY_KEY = r'((Plan){1}\s*\[{1})\s*\d+\,{1}\s*\d+\s*\]{1}\s*={1}\s*\[{1}.*\]{1}'
FIRST_ARRAY_ITEM = r'\[\s*\-?\d+\s*\,'


def _escape_vap_comments(to_be_editted):
    return re.sub(r"(\/\*){1}([^\*\/])+(\*\/){1}", r"", to_be_editted)


# Removes the '[' and ']' from the part after the '=' in an array element inside the vap file
def _remove_brackets_for_vap_array(arraystring):
    return arraystring.replace('[', '').replace(']', '')


# Formats the file of a name to be the one provided in the parameter
# A timestamp of format dYYYYMMDD_tHH_MM_SS is appended
def _give_me_name_for_new_vap_file(name):
    # escape ever appending
    name = re.sub(r'd\d+_t\d+_\d+_\d+', '', name)
    date_object = datetime.now().date()
    time_object = datetime.now().time()
    month_string = stringhelper.get_good_time_string(date_object.month)
    day_string = stringhelper.get_good_time_string(date_object.day)
    hours_string = stringhelper.get_good_time_string(time_object.hour)
    minutes_string = stringhelper.get_good_time_string(time_object.minute)
    seconds_string = stringhelper.get_good_time_string(time_object.second)
    date_string = 'd' + str(date_object.year) + month_string + day_string
    time_string = 't' + hours_string + '_' + minutes_string + '_' + seconds_string
    new_name = name + date_string + '_' + time_string + '.vap'
    return new_name


def _create_vap_file(filepath):
    head, tail = os.path.split(filepath)
    name, extension = tail.split('.')
    new_name_path = dialoghelper.get_absolute_path_for_file(_give_me_name_for_new_vap_file(name))
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
            logging.getLogger('tfl_ivaylo').error('Key not found: ' + key + ', in file' + file.name)
            # print 'Key not found: ' + key + ', in file' + file.name
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
                lines.append(_escape_vap_comments(line))
        except StopIteration:
            # End of file reached
            file.close()
            return lines


def _extract_timings_from_array_line(arrayline, stages):
    array_declaration, array_values = arrayline.split('=')
    array_declaration_no_brackets = _remove_brackets_for_vap_array(array_declaration)
    array_values_no_brackets = _remove_brackets_for_vap_array(array_values)
    to_extract = []
    # find x (the number of elements in each array a 2d array)
    x = stringhelper.parse_integer_from_string(array_declaration_no_brackets.split(',')[1])
    # check if the x is actually extracted
    if x == -1:
        return []
    all_elements = array_values_no_brackets.split(',')
    try:
        for i in range(stages):
            index = i * x
            to_append = stringhelper.parse_integer_from_string(all_elements[index])
            to_extract.append(to_append)
    except IndexError:
        return []
    return to_extract


# Looks for a single line that contains CycleLength
def get_cycle_length_from_vap(filepath):
    lines = _extract_section_for_key(filepath, CONSTANT_SECTION_KEY)
    foundline = ''
    for line in lines:
        line = line.strip()
        if re.search(CYCLE_LENGTH_KEY, line) is not None:
            foundline = line
            break
    cycle_length = -1
    try:
        key, value = foundline.split('=')
    except ValueError:
        # print 'Failed to split the cycle_length line in VAP: ' + foundline
        cycle_length = -1
    else:
        cycle_length = stringhelper.parse_integer_from_string(value)
    return cycle_length


# Looks for a single line
def get_stage_lenghts_from_vap(filepath, number_of_stages):
    if number_of_stages < 0:
        return []
    lines = _extract_section_for_key(filepath, ARRAY_SECTION_KEY)
    stages_timing = []
    for line in lines:
        ignore_whitespace_line = line.replace("\s", '')
        if re.search(PLAN_ARRAY_KEY, ignore_whitespace_line) is not None:
            found_line = line
            stages_timing = _extract_timings_from_array_line(found_line, number_of_stages)
            break

    return stages_timing


def edit_timing_changes(filepath, timings):
    x = len(timings)
    # First match is the one in the declaration of the 2d array
    # array initialized with a '' so the first match don't get replaced
    new_timings_strings = ['']
    for i in range(x):
        new_item = '[' + timings[i] + ','
        new_timings_strings.append(new_item)
    # create new file
    new_file_path = _create_vap_file(filepath)
    # print 'New array: ' + str(new_timings_strings) + ' to be put in new_file_path'
    # put content in the new file
    # 'with' operators close files as soon as they are done
    with open(filepath, "r") as read_from:
        with open(new_file_path, "w") as write_to:
            for line in read_from:
                if re.search(PLAN_ARRAY_KEY, line) is not None:
                    old_timings = re.findall(FIRST_ARRAY_ITEM, line)
                    for i in range(len(new_timings_strings) - 1):
                        old_time = old_timings[i]
                        new_time = new_timings_strings[i]
                        if new_time != '':
                            logging.getLogger('tfl_ivaylo').info('Old time: ' + old_time)
                            logging.getLogger('tfl_ivaylo').info('New time: ' + new_time)
                            # print 'Old time: '+ old_time
                            # print 'New time: ' + new_time
                            line = line.replace(old_time, new_time)
                            logging.getLogger('tfl_ivaylo').info('New line: ' + line)
                            # print 'New line: ' + line
                    write_to.write('/* This was automatically edited by the PDDL plan */\n')
                write_to.write(line)
    return new_file_path