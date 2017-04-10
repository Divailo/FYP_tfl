import win32com.client as com  # com library
import sys  # all kinds of shit library

import puahelper
import vaphelper
import vissimhelper
import pddlhelper
import jsonhelper
import dialoghelper

json_filename = 'out.json'
pddl_filename = 'pddl.pddl'


def _get_absolute_path_for_file(filepath):
    return dialoghelper.get_absolute_path_for_file(filepath)


# Closes the COM connection and exits the program
def _close_program(message):
    global Vissim
    Vissim = None
    # Display error message in console if any
    if message != '':
        print 'ERROR MESSAGE: ' + message
        dialoghelper.showerror(message)
    print '\n== END OF SCRIPT =='
    sys.exit()


print '== START OF SCRIPT =='

inpx_file = dialoghelper.ask_for_model()
if not dialoghelper.check_file_chosen(inpx_file):
    _close_program('Please choose a file')

if not dialoghelper.check_model_file(inpx_file):
    _close_program('Please choose a valid Vissim model file/inpx file')

# create Vissim COM object
Vissim = com.Dispatch("Vissim.Vissim")

if not vissimhelper.check_vissim_initialised(Vissim):
    _close_program('Vissim program not found.'
                   'It might be because the program is not installed on the machine')

# version-specific object: Vissim = com.Dispatch("Vissim.Vissim.9")
# Vissim.LoadNet("C:\Users\Ivaylo\Desktop\Examples\PTV Headquarters - Left-hand\Headquarters 14 LH.inpx")
# Vissim.LoadNet("C:\Users\Public\Documents\PTV Vision\PTV Vissim 9\Examples Demo\Roundabout London.UK\Roundabout London.inpx")
Vissim.LoadNet(inpx_file)

signalControllerCollection = Vissim.Net.SignalControllers.GetAll()

sgs = []
scs = []
for sc in signalControllerCollection:

    vissim_signal_controller_object = vissimhelper.VissimSignalController(sc)

    sc_data = {}

    sc_data[jsonhelper.SC_ID_KEY] = str(vissim_signal_controller_object.id)
    sc_data[jsonhelper.SC_NAME_KEY] = str(vissim_signal_controller_object.name)
    sc_data[jsonhelper.SC_TYPE_KEY] = str(vissim_signal_controller_object.type)
    pua_to_global_ids = {}
    if str(vissim_signal_controller_object.type) == 'VAP':

        # test TFL files
        # sc_data[jsonhelper.SC_VAPFILE_KEY] = 'C:\\Users\\Ivaylo\\Desktop\\A3 FT Model v2\\33.vap'
        # sc_data[jsonhelper.SC_PUAFILE_KEY] = 'C:\\Users\\Ivaylo\\Desktop\\A3 FT Model v2\\33.pua'
        # sc_data['pua_file'] = "D:\\PyCharmProjects\\tests\\goodpuafile.pua"

        # actual data
        sc_data[jsonhelper.SC_VAPFILE_KEY] = _get_absolute_path_for_file(str(vissim_signal_controller_object.supply_file_1))
        sc_data[jsonhelper.SC_PUAFILE_KEY] = _get_absolute_path_for_file(str(vissim_signal_controller_object.supply_file_2))
        sc_data[jsonhelper.SC_INITIAL_STAGE_KEY] = puahelper.get_starting_stage_from_pua(sc_data[jsonhelper.SC_PUAFILE_KEY])
        sc_data[jsonhelper.SC_MAX_STAGE_KEY] = puahelper.get_max_stage_from_pua(sc_data[jsonhelper.SC_PUAFILE_KEY])
        pua_to_global_ids = puahelper.read_and_map_signalgroups_from_pua(sc_data[jsonhelper.SC_PUAFILE_KEY])
        pua_stages = puahelper.get_phases_in_stages_from_pua(sc_data[jsonhelper.SC_PUAFILE_KEY])

        # specific for TFL models, will return -1 if it works with different models
        sc_data[jsonhelper.SC_CYCLE_LENGTH_KEY] = vaphelper.get_cycle_length_from_vap(sc_data[jsonhelper.SC_VAPFILE_KEY])
        sc_data[jsonhelper.SC_STAGE_TIMINGS_KEY] = vaphelper.get_stage_lenghts_from_vap(sc_data[jsonhelper.SC_VAPFILE_KEY]
                                                                                        , sc_data[jsonhelper.SC_MAX_STAGE_KEY])
    else:
        print 'Non-VAP signal controllers currently not supported!'
        continue

    # key = sg.AttValue("No")
    # type = sg.AttValue("Type")
    print 'Signal Controller Key: ' + str(vissim_signal_controller_object.id)
    print 'Signal Controller Type: ' + str(vissim_signal_controller_object.type)
    print 'Signal Controller Supply File 1: ' + str(vissim_signal_controller_object.supply_file_1)
    print 'Signal Controller Supply File 2: ' + str(vissim_signal_controller_object.supply_file_2)

    # counter = 0
    sgCollection = sc.SGs.GetAll()
    for sg in sgCollection:
        vissim_signal_group_object = vissimhelper.VissimSignalGroup(sg)

        sg_data = {}
        sg_data[jsonhelper.SG_ID_KEY] = str(sg.AttValue(vissimhelper.SG_ID_KEY))

        print 'Singal Group No: ' + str(sg.AttValue(vissimhelper.SG_ID_KEY))

        # Crawl through the signal heads so the from link are found
        signal_heads_collection = sg.SigHeads.GetAll()

        vissim_signal_group_object.set_links_from_signalhead_collection(signal_heads_collection)
        print 'Signal group from links: ' + str(vissim_signal_group_object.links)

        sg_data[jsonhelper.SG_LINKS_KEY] = vissim_signal_group_object.links

        sg_no = str(sg.AttValue(vissimhelper.SG_ID_KEY))
        if pua_to_global_ids is not None:
            if sg_no in pua_to_global_ids:
                local_key = str(pua_to_global_ids[sg_no])
                green_stages = []
                if local_key in pua_stages:
                    green_stages = pua_stages[local_key]
                sg_data[jsonhelper.SG_PHASE_IN_STAGES_KEY] = green_stages

        sgs.append(sg_data)

        print '= END OF SIGNAL GROUP = \n'

    sc_data[jsonhelper.SC_SG_KEY] = sgs
    scs.append(sc_data)

print '= END OF SIGNAL CONTROLLER ='

jsonhelper.write_data_to_json_file(json_filename, scs)

pddlhelper.convert_jsonfile_to_pddlproblem(json_filename, pddl_filename)

_close_program('')
