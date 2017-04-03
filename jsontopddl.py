import json

import jsonhelper

# JSON keys
JSON_SC_ID_KEY = jsonhelper.SC_ID_KEY
JSON_SC_NAME_KEY = jsonhelper.SC_NAME_KEY
JSON_SC_TYPE_KEY = jsonhelper.SC_TYPE_KEY
JSON_SC_SG_KEY = jsonhelper.SC_SG_KEY
JSON_SC_INITIAL_STAGE_KEY = jsonhelper.SC_INITIAL_STAGE_KEY
JSON_SC_MAX_STAGE_KEY = jsonhelper.SC_MAX_STAGE_KEY

JSON_SG_PHASE_IN_STAGES_KEY = jsonhelper.SG_PHASE_IN_STAGES_KEY
JSON_SG_LINKS_KEY = jsonhelper.SG_LINKS_KEY

# PDDL function and property names
CURR_STAGE_KEY = 'current_stage '  # Parameters: intersection, value
MAX_STAGE_KEY = 'max_stage '  # Parameters: intersection, value
PHASE_IN_STAGE_KEY = 'phase_in_stage '  # Parameters: link, intersection, value
MIN_GREEN_KEY = 'min_green_time '  # Parameters: intersection, value. Not sure if needed

START_COMMENT_KEY = ';; '

def _extract_phase_in_stages_map(sgsarray):
    phase_in_stages = {}
    for sg in sgsarray:
        sg_stages = sg[JSON_SG_PHASE_IN_STAGES_KEY]
        sg_links = sg[JSON_SG_LINKS_KEY]
        for link in sg_links:
            phase_in_stages[link] = sg_stages

    return  phase_in_stages

def convert_jsonfile_to_pddlproblem(json_filename, pddl_filename):
    print "= CONVERTING JSON TO PDDL ="
    json_file = open(json_filename)
    data = json.load(json_file)

    pddl_file = open(pddl_filename, 'w')
    for signal_controller in data:
        sc_id = signal_controller[JSON_SC_ID_KEY]
        sc_name = signal_controller[JSON_SC_NAME_KEY]
        sc_curr_stage = signal_controller[JSON_SC_INITIAL_STAGE_KEY]
        sc_max_stage = signal_controller[JSON_SC_MAX_STAGE_KEY]
        sc_sgs = signal_controller[JSON_SC_SG_KEY]

        lines = []
        # Start section
        lines.append(_create_signal_controller_section(sc_name))
        # initial stage
        lines.append(_make_max_stage_line(sc_curr_stage, sc_name))
        # max stage
        lines.append(_make_max_stage_line(sc_max_stage, sc_name))
        # phase in stage
        phases_in_stages_lines = _make_phase_in_stage_lines(_extract_phase_in_stages_map(sc_sgs), sc_name)
        for line in phases_in_stages_lines:
            lines.append(line)


        pddl_file.writelines(lines)


    json_file.close()
    print "= CONVERTING JSON TO PDDL ="

def _create_signal_controller_section(name):
    return START_COMMENT_KEY + name + '\n'

def _make_current_stage_line(initial_stage_value, intersection_name):
    line = '\t'
    if initial_stage_value == -1:
        line = line + START_COMMENT_KEY + ' NO INFROMATION FOR ' + CURR_STAGE_KEY + intersection_name + '\n'
    else:
        initial_stage_value = str(initial_stage_value * 10)
        line = line + '(= (' + CURR_STAGE_KEY + intersection_name + ') ' + initial_stage_value + ')' + '\n'
    return line

def _make_max_stage_line(max_stage_value, intersection_name):
    line = '\t'
    if max_stage_value == -1:
        line = line + START_COMMENT_KEY + ' NO INFROMATION FOR ' + MAX_STAGE_KEY + intersection_name + '\n'
    else:
        max_stage_value = str(max_stage_value * 10)
        line = line + '(= (' + MAX_STAGE_KEY + intersection_name + ') ' + max_stage_value + ')' + '\n'
    return line

def _make_phase_in_stage_lines(phases_in_stages, intersection_name):
    lines_to_append = []
    if phases_in_stages == {}:
        line = '\t' + START_COMMENT_KEY + ' NO INFROMATION FOR ' + PHASE_IN_STAGE_KEY + intersection_name + '\n'
        lines_to_append.append(line)
    else:
        for link, stages in phases_in_stages.iteritems():
            for stage in stages:
                stage_value = str(stage * 10)
                line = '\t' + '(= (' + PHASE_IN_STAGE_KEY + link + ' ' + intersection_name + ') ' + stage_value + ')' + '\n'
                lines_to_append.append(line)


    return lines_to_append