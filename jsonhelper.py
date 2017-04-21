import json  # json library

# JSON Keys

# SC Keys
JSON_SC_ID_KEY = 'id'
JSON_SC_NAME_KEY = 'name'
JSON_SC_TYPE_KEY = 'type'
JSON_SC_VAPFILE_KEY = 'vap_file'
JSON_SC_PUAFILE_KEY = 'pua_file'
JSON_SC_SG_KEY = 'signal_groups'
# SC VAP SPECIFIC KEYS
JSON_SC_INITIAL_STAGE_KEY = 'initial_stage'
JSON_SC_MAX_STAGE_KEY = 'max_stage'
JSON_SC_CYCLE_LENGTH_KEY = 'cycle_length'
JSON_SC_STAGE_TIMINGS_KEY = 'stage_timings'
# SG KEYS
JSON_SG_ID_KEY = 'id'
JSON_SG_LINKS_KEY = 'links'
JSON_SG_PHASE_IN_STAGES_KEY = 'phase_in_stages'
# LINK KEYS
JSON_LINK_NAME_KEY = 'name'


def write_data_to_json_file(json_filename, data):
    json_data = json.dumps(data)
    f = open(json_filename, 'w')
    f.write(str(json_data))
    f.close()