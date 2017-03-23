import re # regex library

import stringhelper

ACTUAL_CONTENT_SEPARATOR = "$"
SIGNAL_GROUPS_KEY = "$SIGNAL_GROUPS"
STAGES_KEY = "$STAGES"
STAGE_PREFIX = "Stage_"
STARTING_STAGE_KEY = "$STARTING_STAGE"


def _get_actual_content_to_extract_in_pua(file, key):
    # print "Filepath: " + filepath

    global ACTUAL_CONTENT_SEPARATOR

    line = ""
    while line != key:
        line = file.readline().strip()
        # Key not found
        if line is None:
            return []

    while line != ACTUAL_CONTENT_SEPARATOR:
        line = file.readline().strip()
        # Key not found
        if line is None:
            return []

    lines = []
    while True:
        line = file.readline().strip()
        if stringhelper.does_string_contain_substring(line, ACTUAL_CONTENT_SEPARATOR) == False:
            line = re.sub(' +',' ',line)
            lines.append(line)
            # print "Added line: " + line
        else:
            break

    return lines

# Opens a file and finds all the local (the ones used in the pua file) and global (the ones used in the model) ids of signal groups
def read_and_map_signalgroups_from_pua(filepath):
    global SIGNAL_GROUPS_KEY
    opened_file = open(filepath)

    lines_to_read = _get_actual_content_to_extract_in_pua(opened_file, SIGNAL_GROUPS_KEY)

    map = {}
    for line in lines_to_read:
        array_split = line.split(" ")
        if len(array_split) == 2:
            map[array_split[1]] = array_split[0]

    # Debugging purpose
    # for key, value in map.items():
    #     print key + " : " + value

    print "END OF MAP SIGNAL GROUPS TO IDS"

    return map

# Gets which phases are green when stage is reached
def get_pua_stages(filepath):

    global STAGES_KEY

    opened_file = open(filepath)
    lines = _get_actual_content_to_extract_in_pua(opened_file, STAGES_KEY)
    global STAGE_PREFIX
    RED_KEY = "red"

    green_map = {}
    # stage_pointer = -1

    for line in lines:
        if stringhelper.does_string_contain_substring(line, STAGE_PREFIX) == True:
            string_split = line.split(" ")
            stage_pointer = int(re.search(r'\d+', line).group())
            for signal_group in string_split[1:]:
                # if the array of the signal group green stages is not initialized
                if not signal_group in green_map:
                    green_map[signal_group] = []
                # add a green stage to the signal
                green_map[signal_group].append(stage_pointer)

        # if _does_string_contain_substring(line, RED_KEY):
        #     string_split = line.split(" ")
        #     if len(string_split) > 1:

    # Debugging purpose
    # for key, value in green_map.items():
    #     print key + " : " + str(value)

    print "END OF GET STAGES"

    return green_map


# Returns integer, representing the first stage of the signal controller
def get_starting_stage_from_pua(filepath):
    global STARTING_STAGE_KEY
    opened_file = open(filepath)
    lines = _get_actual_content_to_extract_in_pua(opened_file, STARTING_STAGE_KEY)
    global STAGE_PREFIX

    for line in lines:
        if stringhelper.does_string_contain_substring(line, STAGE_PREFIX) == True:
            stage_number = int(line.replace(STAGE_PREFIX, ''))
            # print stage_number
            print "END OF FIND STARTING STAGE"
            return stage_number

    return -1