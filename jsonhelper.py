import json  # json library

# JSON Keys

# SC Keys
SC_ID_KEY = 'id'
SC_NAME_KEY = 'name'
SC_TYPE_KEY = 'type'
SC_VAPFILE_KEY = 'vap_file'
SC_PUAFILE_KEY = 'pua_file'
SC_SG_KEY = 'signal_groups'
# SC VAP SPECIFIC KEYS
SC_INITIAL_STAGE_KEY = 'initial_stage'
SC_MAX_STAGE_KEY = 'max_stage'
SC_CYCLE_LENGTH_KEY = 'cycle_length'
SC_STAGE_TIMINGS_KEY = 'stage_timings'
# SG KEYS
SG_ID_KEY = 'id'
SG_LINKS_KEY = 'links'
SG_PHASE_IN_STAGES_KEY = 'phase_in_stages'
# LINK KEYS
LINK_NAME_KEY = 'name'


def write_data_to_json_file(json_filename, data):
    json_data = json.dumps(data)
    f = open(json_filename, 'w')
    f.write(str(json_data))
    f.close()