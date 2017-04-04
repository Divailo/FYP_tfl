import re # regex library

import stringhelper

# Constants
ACTUAL_CONTENT_SEPARATOR = "$"
SIGNAL_GROUPS_KEY = "$SIGNAL_GROUPS"
STAGES_KEY = "$STAGES"
STAGE_PREFIX = "Stage_"
STARTING_STAGE_KEY = "$STARTING_STAGE"

# Looks for a section which starts with the provided key
# Starts extracting the lines to look for after seeing a $
# Finishes extracting lines to read when sees another $
# returns collection of lines to read from
# on error (structure not satisfied) returns empty array
def _get_actual_content_to_extract_in_pua(filepath, key):
    file = open(filepath)

    line = ""
    while line != key:
        try:
            line = file.next().strip()
        except StopIteration:
            # End of file reached
            file.close()
            return []

    while line != ACTUAL_CONTENT_SEPARATOR:
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
            if stringhelper.does_string_contain_substring(line, ACTUAL_CONTENT_SEPARATOR) == False:
                line = re.sub(' +',' ',line)
                lines.append(line)
            else:
                break
        except StopIteration:
            # End of file reached
            file.close()
            return lines

    return lines

# Opens a file and finds all the local (the ones used in the pua file) and global (the ones used in the model) ids of signal groups
def read_and_map_signalgroups_from_pua(filepath):
    lines_to_read = _get_actual_content_to_extract_in_pua(filepath, SIGNAL_GROUPS_KEY)
    map = {}

    for line in lines_to_read:
        # Civil war
        line = line.replace('\t',' ')

        array_split = line.split(" ")

        if len(array_split) == 2:
            map[array_split[1]] = array_split[0]

    # Debugging purpose
    # for key, value in map.items():
    #     print key + " : " + value

    print "END OF MAP SIGNAL GROUPS TO IDS"

    return map

# Gets which phases are green when stage is reached
def get_phases_in_stages_from_pua(filepath):
    lines = _get_actual_content_to_extract_in_pua(filepath, STAGES_KEY)
    green_map = {}

    for line in lines:
        if stringhelper.does_string_contain_substring(line, STAGE_PREFIX) == True:
            # Civil war
            line = line.replace('\t',' ')

            string_split = line.split(" ")

            stage_pointer = int(re.search(r'\d+', line).group())
            for signal_group in string_split[1:]:
                # if the array of the signal group green stages is not initialized
                if signal_group not in green_map:
                    green_map[signal_group] = []
                # add a green stage to the signal
                green_map[signal_group].append(stage_pointer)

        # if _does_string_contain_substring(line, RED_KEY):
        #     string_split = line.split(" ")
        #     if len(string_split) > 1:

    # Debugging purpose
    # for key, value in green_map.items():
    #     print key + " : " + str(value)

    print "END OF GET PHASES IN STAGES"

    return green_map


# Returns integer, representing the first stage of the signal controller
def get_starting_stage_from_pua(filepath):
    lines = _get_actual_content_to_extract_in_pua(filepath, STARTING_STAGE_KEY)

    for line in lines:
        if stringhelper.does_string_contain_substring(line, STAGE_PREFIX) == True:
            # stage_number = int(line.replace(STAGE_PREFIX, ''))
            stage_number = stringhelper.parse_integer_from_string(line)
            # print stage_number
            print "END OF FIND STARTING STAGE"
            return stage_number


    return -1

def get_max_stage_from_pua(filepath):
    lines = _get_actual_content_to_extract_in_pua(filepath, STAGES_KEY)
    max_stage = -1
    for line in lines:
        if stringhelper.does_string_contain_substring(line, STAGE_PREFIX) == True:
            # better with regex
            stage_number = stringhelper.parse_integer_from_string(line)
            if stage_number > max_stage:
                max_stage = stage_number
            # print stage_number

    print "END OF FIND MAX STAGE"
    return max_stage