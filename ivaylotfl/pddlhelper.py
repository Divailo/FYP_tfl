import json
import re

import jsonhelper

# JSON keys
__JSON_SC_ID_KEY = jsonhelper.JSON_SC_ID_KEY
__JSON_SC_NAME_KEY = jsonhelper.JSON_SC_NAME_KEY
__JSON_SC_TYPE_KEY = jsonhelper.JSON_SC_TYPE_KEY
__JSON_SC_SG_KEY = jsonhelper.JSON_SC_SG_KEY
__JSON_SC_INITIAL_STAGE_KEY = jsonhelper.JSON_SC_INITIAL_STAGE_KEY
__JSON_SC_MAX_STAGE_KEY = jsonhelper.JSON_SC_MAX_STAGE_KEY

__JSON_SG_PHASE_IN_STAGES_KEY = jsonhelper.JSON_SG_PHASE_IN_STAGES_KEY
__JSON_SG_LINKS_KEY = jsonhelper.JSON_SG_LINKS_KEY
__JSON_LINK_NAME_KEY = jsonhelper.JSON_LINK_NAME_KEY

# PDDL function and property names
__CURR_STAGE_KEY = 'current_stage '  # Parameters: intersection, value
__MAX_STAGE_KEY = 'max_stage '  # Parameters: intersection, value
__PHASE_IN_STAGE_KEY = 'phase_in_stage '  # Parameters: link, intersection, value
__START_COMMENT_KEY = ';; '


def __extract_phase_in_stages_map(sgsarray):
    phase_in_stages = {}
    for sg in sgsarray:
        sg_stages = sg[__JSON_SG_PHASE_IN_STAGES_KEY]
        sg_links = sg[__JSON_SG_LINKS_KEY]
        for link in sg_links:
            link_name = link[__JSON_LINK_NAME_KEY]
            phase_in_stages[link_name] = sg_stages
    return phase_in_stages


def __generate_pddl_lines(json_filename):
    lines = []
    json_file = open(json_filename)
    data = json.load(json_file)
    for signal_controller in data:
        sc_id = signal_controller[__JSON_SC_ID_KEY]
        sc_name = signal_controller[__JSON_SC_NAME_KEY]
        sc_curr_stage = signal_controller[__JSON_SC_INITIAL_STAGE_KEY]
        sc_max_stage = signal_controller[__JSON_SC_MAX_STAGE_KEY]
        sc_sgs = signal_controller[__JSON_SC_SG_KEY]
        # Start section
        lines.append(__create_signal_controller_section(sc_name))
        # initial stage
        lines.append(__make_current_stage_line(sc_curr_stage, sc_name))
        # max stage
        lines.append(__make_max_stage_line(sc_max_stage, sc_name))
        # phase in stage
        lines.append(__make_phase_in_stage_lines(__extract_phase_in_stages_map(sc_sgs), sc_name))
    json_file.close()
    return lines


def __create_signal_controller_section(name):
    return __START_COMMENT_KEY + name + '\n'


def __make_current_stage_line(initial_stage_value, intersection_name):
    line = '\t'
    if initial_stage_value == -1:
        line = line + __START_COMMENT_KEY + ' NO INFROMATION FOR ' + __CURR_STAGE_KEY + intersection_name + '\n'
    else:
        initial_stage_value = str(initial_stage_value * 10)
        line = line + '(= (' + __CURR_STAGE_KEY + intersection_name + ') ' + initial_stage_value + ')' + '\n'
    return line


def __make_max_stage_line(max_stage_value, intersection_name):
    line = '\t'
    if max_stage_value == -1:
        line = line + __START_COMMENT_KEY + ' NO INFROMATION FOR ' + __MAX_STAGE_KEY + intersection_name + '\n'
    else:
        max_stage_value = str(max_stage_value * 10)
        line = line + '(= (' + __MAX_STAGE_KEY + intersection_name + ') ' + max_stage_value + ')' + '\n'
    return line


def __make_phase_in_stage_lines(phases_in_stages, intersection_name):
    line = ''
    if phases_in_stages == {}:
        line = '\t' + __START_COMMENT_KEY + ' NO INFROMATION FOR ' + __PHASE_IN_STAGE_KEY + intersection_name + '\n'
    else:
        lines_to_be_joined = []
        for link, stages in phases_in_stages.iteritems():
            for stage in stages:
                stage_value = str(stage * 10)
                line_to_append = '\t' + '(= (' \
                                 + __PHASE_IN_STAGE_KEY + link + ' ' + intersection_name + ') ' + stage_value + ')' + '\n'
                lines_to_be_joined.append(line_to_append)
        line = line.join(lines_to_be_joined)

    return line


# Converts the contents of a json file to pddl file
def convert_jsonfile_to_pddlproblem(json_filename, pddl_filename):
    pddl_filename.writelines(__generate_pddl_lines(json_filename))
    pddl_filename.close()


RELEVANT_LINE_REGEX = r'\d+\.\d+:\s*\(\s*switchtrafficsignal\s*\S+\)'
IRRELEVANT_REGEX1 = r'.\d+:\s*\(\s*switchtrafficsignal'
IRRELEVANT_REGEX2 = r'\)'


# Returns a map: juction : [signal timings]
def get_new_stages_information(filepath):
    to_return = {}
    opened_file = open(filepath)
    for line in opened_file.readlines():
        if re.match(RELEVANT_LINE_REGEX, line) is not None:
            line = re.sub(IRRELEVANT_REGEX1, '', line)
            line = re.sub(IRRELEVANT_REGEX2, '', line)
            split_lne = re.split(' ', line)
            stage_timing = split_lne[0]
            junction_name = split_lne[1]
            if junction_name not in to_return:
                to_return[junction_name] = []
            to_return[junction_name].append(stage_timing)
    opened_file.close()
    return to_return
