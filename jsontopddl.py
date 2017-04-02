import json

CURR_STAGE_KEY = 'current_stage'  # Parameters: intersection, value
MIN_STAGE_KEY = 'min_stage'  # Parameters: intersection, value
PHASE_IN_STAGE_KEY = 'phase_in_stage'  # Parameters: link, intersection, value
MAX_GREEN_KEY = 'max_green_time'  # Parameters: intersection, value. Not sure if needed

def convertjsonfiletopddlproblem(filename):
    print "== CONVERTING JSON TO PDDL =="
    json_file = open(file)
    data = json.load(json_file)


    json_file.close()