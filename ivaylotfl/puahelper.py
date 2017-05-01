import re  # regex library

import __stringhelper

# Constants
__ACTUAL_CONTENT_SEPARATOR = '$'
__SIGNAL_GROUPS_KEY = '$SIGNAL_GROUPS'
__STAGES_KEY = '$STAGES'
__STAGE_PREFIX = 'Stage_'
__STARTING_STAGE_KEY = '$STARTING_STAGE'

__SIGNAL_GROUP_RE = r'[a-zA-z]\S*\s+\d+'


# Looks for a section which starts with the provided key
# Starts extracting the lines to look for after seeing a $
# Finishes extracting lines to read when sees another $
# returns collection of lines to read from
# on error (structure not satisfied) returns empty array
def __get_actual_content_to_extract_in_pua(filepath, key):
    file = open(filepath)
    line = ''
    while line != key:
        try:
            line = file.next().strip()
        except StopIteration:
            # End of file reached
            file.close()
            return []
    while line != __ACTUAL_CONTENT_SEPARATOR:
        try:
            line = file.next().strip()
        except StopIteration:
            # End of file reached
            file.close()
            return []
    lines = []
    while True:
        try:
            line = file.next().strip()
            if __stringhelper.does_string_contain_substring(line, __ACTUAL_CONTENT_SEPARATOR) == False:
                line = re.sub(' +', ' ', line)
                lines.append(line)
            else:
                break
        except StopIteration:
            # End of file reached
            file.close()
            return lines
    return lines


def __filter_signal_group_lines(filepath):
    lines = __get_actual_content_to_extract_in_pua(filepath, __SIGNAL_GROUPS_KEY)
    to_return = []
    for line in lines:
        if re.search(__SIGNAL_GROUP_RE, line) is not None:
            to_return.append(line)
    return to_return


# Opens a file and finds all the local (the ones used in the pua file) and global (the ones used in the model) ids of signal groups
def read_and_map_signalgroups_from_pua(filepath):
    lines_to_read = __filter_signal_group_lines(filepath)
    map = {}
    for line in lines_to_read:
        line = line.replace('\t', ' ')
        key, value = line.split(' ')
        map[value] = key
    return map


# Gets which phases are green when stage is reached
def get_phases_in_stages_from_pua(filepath):
    lines = __get_actual_content_to_extract_in_pua(filepath, __STAGES_KEY)
    green_map = {}
    for line in lines:
        if __stringhelper.does_string_contain_substring(line, __STAGE_PREFIX) == True:
            line = line.replace('\t', ' ')
            string_split = line.split(' ')
            stage_pointer = int(re.search(r'\d+', line).group())
            for signal_group in string_split[1:]:
                # if the array of the signal group green stages is not initialized
                if signal_group not in green_map:
                    green_map[signal_group] = []
                # add a green stage to the signal
                green_map[signal_group].append(stage_pointer)
    return green_map


# Returns integer, representing the first stage of the signal controller
def get_starting_stage_from_pua(filepath):
    lines = __get_actual_content_to_extract_in_pua(filepath, __STARTING_STAGE_KEY)
    for line in lines:
        if __stringhelper.does_string_contain_substring(line, __STAGE_PREFIX) == True:
            stage_number = __stringhelper.parse_integer_from_string(line)
            return stage_number
    return -1


# Extracts the maximum stager from the pua file
def get_max_stage_from_pua(filepath):
    lines = __get_actual_content_to_extract_in_pua(filepath, __STAGES_KEY)
    max_stage = -1
    for line in lines:
        if __stringhelper.does_string_contain_substring(line, __STAGE_PREFIX) == True:
            stage_number = __stringhelper.parse_integer_from_string(line)
            if stage_number > max_stage:
                max_stage = stage_number
    return max_stage
