import win32com.client as com  # com library
import sys  # all kinds of shit library

import puahelper
import vaphelper
import vissimhelper
import pddlhelper
import jsonhelper
import dialoghelper

def _get_absolute_path_for_file(filepath):
    return dialoghelper.get_absolute_path_for_file(filepath)


# Closes the COM connection and exits the program
def _close_program(message):
    # Display error message in dialog if any
    if message != '':
        print 'ERROR MESSAGE: ' + message
        dialoghelper.showerror(message)
    print '\n== END OF SCRIPT =='
    sys.exit()


print '== START OF SCRIPT =='

inpx_file = dialoghelper.ask_for_model()
if not dialoghelper.is_file_chosen(inpx_file):
    _close_program('Please choose a file')
if not dialoghelper.check_model_file(inpx_file):
    _close_program('Please choose a valid Vissim model file/inpx file')

# create Vissim COM object
vissim = vissimhelper.initialise_vissim(com)
if vissim is None:
    _close_program('Vissim program not found.'
                   'It might be because the program is not installed on the machine')

vissimhelper.bring_vissim_to_front(vissim)
# Vissim.LoadNet("C:\Users\Ivaylo\Desktop\Examples\PTV Headquarters - Left-hand\Headquarters 14 LH.inpx")
# Vissim.LoadNet("C:\Users\Public\Documents\PTV Vision\PTV Vissim 9\Examples Demo\Roundabout London.UK\Roundabout London.inpx")
vissimhelper.load_vissim_network(vissim, inpx_file)
signal_controller_collection = vissimhelper.get_signal_controllers(vissim)
sc_json_array = []

for sc in signal_controller_collection:
    sc_data = {}
    sgs = []

    sc_type = vissimhelper.get_sc_type(sc)
    # sc_data[jsonhelper.JSON_SC_TYPE_KEY] =
    pua_to_global_ids = {}
    if sc_type == 'VAP':
        # test TFL files
        # vap_file_location = 'C:\\Users\\Ivaylo\\Desktop\\A3 FT Model v2\\33.vap'
        pua_file_location = 'C:\\Users\\Ivaylo\\Desktop\\A3 FT Model v2\\33.pua'

        # actual data
        sc_id = vissimhelper.get_sc_id(sc)
        sc_name = vissimhelper.get_sc_name(sc)
        vap_file_location = _get_absolute_path_for_file(str(vissimhelper.get_vapfile(sc)))
        # pua_file_location = _get_absolute_path_for_file(str(vissimhelper.get_puafile(sc)))
        cycle_length = vaphelper.get_cycle_length_from_vap(vap_file_location)
        pua_to_global_ids = puahelper.read_and_map_signalgroups_from_pua(pua_file_location)
        pua_stages = puahelper.get_phases_in_stages_from_pua(pua_file_location)
        initial_stage = puahelper.get_starting_stage_from_pua(pua_file_location)
        max_stage = puahelper.get_max_stage_from_pua(pua_file_location)
        stage_timings = vaphelper.get_stage_lenghts_from_vap(vap_file_location, max_stage)
        print 'Signal Controller Id: ' + str(vissimhelper.get_sc_id(sc))
        print 'Signal Controller Supply File 1: ' + str(vap_file_location)
        print 'Signal Controller Supply File 2: ' + str(pua_file_location)
        print 'PUA TO GLOBAL IDS: ' + str(pua_to_global_ids)
        # serialize
        sc_data[jsonhelper.JSON_SC_ID_KEY] = str(sc_id)
        sc_data[jsonhelper.JSON_SC_NAME_KEY] = sc_name
        sc_data[jsonhelper.JSON_SC_VAPFILE_KEY] = vap_file_location
        sc_data[jsonhelper.JSON_SC_PUAFILE_KEY] = pua_file_location
        sc_data[jsonhelper.JSON_SC_INITIAL_STAGE_KEY] = initial_stage
        sc_data[jsonhelper.JSON_SC_MAX_STAGE_KEY] = max_stage
        # specific for TFL models, will return -1 if it works with different models
        sc_data[jsonhelper.JSON_SC_CYCLE_LENGTH_KEY] = cycle_length
        sc_data[jsonhelper.JSON_SC_STAGE_TIMINGS_KEY] = stage_timings
    else:
        print 'Non-VAP signal controllers not supported!'
        continue

    sgCollection = sc.SGs.GetAll()
    for sg in sgCollection:
        sg_data = {}
        sg_id = vissimhelper.get_sg_id(sg)
        sg_id_string = str(sg_id)
        sg_links = vissimhelper.get_links(sg)
        print 'Singal Group No: ' + sg_id_string
        print 'Signal group from links: ' + str(sg_links)

        if pua_to_global_ids is not None:
            if sg_id_string in pua_to_global_ids:
                local_key = str(pua_to_global_ids[sg_id_string])
                green_stages = []
                if local_key in pua_stages:
                    green_stages = pua_stages[local_key]
                sg_data[jsonhelper.JSON_SG_PHASE_IN_STAGES_KEY] = green_stages
            sg_data[jsonhelper.JSON_SG_ID_KEY] = sg_id
            sg_data[jsonhelper.JSON_SG_LINKS_KEY] = sg_links

        sgs.append(sg_data)
        print '= END OF SIGNAL GROUP = \n'

    sc_data[jsonhelper.JSON_SC_SG_KEY] = sgs
    sc_json_array.append(sc_data)
    print '= END OF SIGNAL CONTROLLER ='
print '= ALL DATA COLLECTED ='

json_filename = 'out_' + inpx_file[:-5] + '.json'
pddl_filename = dialoghelper.ask_to_save()
if pddl_filename is None:
    _close_program('')
jsonhelper.write_data_to_json_file(json_filename, sc_json_array)
pddlhelper.convert_jsonfile_to_pddlproblem(json_filename, pddl_filename)
_close_program('')
