import json

import jsonhelper

JSON_SC_ID_KEY = jsonhelper.SC_ID_KEY
JSON_SC_TYPE_KEY = jsonhelper.SC_TYPE_KEY
# JSON_SC_ID_KEY = jsonhelper.SC_ID_KEY
# JSON_SC_ID_KEY = jsonhelper.SC_ID_KEY
# JSON_SC_ID_KEY = jsonhelper.SC_ID_KEY
# JSON_SC_ID_KEY = jsonhelper.SC_ID_KEY

CURR_STAGE_KEY = 'current_stage '  # Parameters: intersection, value
MAX_STAGE_KEY = 'max_stage '  # Parameters: intersection, value
PHASE_IN_STAGE_KEY = 'phase_in_stage '  # Parameters: link, intersection, value
MIN_GREEN_KEY = 'min_green_time '  # Parameters: intersection, value. Not sure if needed

START_COMMENT_KEY = ';; '

def convert_jsonfile_to_pddlproblem(json_filename, pddl_filename):
    print "= CONVERTING JSON TO PDDL ="
    json_file = open(json_filename)
    data = json.load(json_file)

    pddl_file = open(pddl_filename, 'w')
    for signal_controller in data:
        sc_name = signal_controller[JSON_SC_ID_KEY]
        sc_curr_stage = signal_controller['curr_stage']

        lines = []
        # Start section
        lines.append(_create_signal_controller_section(sc_name))
        # max stage
        lines.append()
        pddl_file.writelines(lines)


    json_file.close()
    print "= CONVERTING JSON TO PDDL ="

def _create_signal_controller_section(name):
    return START_COMMENT_KEY + name + '\n'

def _make_max_stage_line(max_stage_value, intersection_name):
    line = '\t'
    if max_stage_value == -1:
        line = line + START_COMMENT_KEY + ' NO INFROMATION FOR ' + MAX_STAGE_KEY + intersection_name + '\n'
    else:
        line = line + '((' + MAX_STAGE_KEY + intersection_name + ') ' + max_stage_value + ')' + '\n'
    return line