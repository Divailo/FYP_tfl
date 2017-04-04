import win32com.client as com  # com library
from Tkinter import Tk  # gui library
import tkFileDialog  # file dialog library
# import threading  # library for threads
import json  # json library
import sys  # all kinds of shit library
import os.path

import puahelper
import vaphelper
import vissimclasses
import jsontopddl

folderpath = ''
json_filename = 'out.json'
pddl_filename = 'pddl.pddl'
# pddl_file_name = problem_file + time_stamp + .pddl

# VAP and PUA filess might not give their absolute path if they are in the same folder as the model
# To ensure absolute path is taken, this method is called when getting pua and vap files
def _get_absolute_path_for_file(file):
    try:
        open_file = open(file)
        open_file.close()
    except IOError:
        file = folderpath + '\\' + file

    return file

# initializes a file chooser to load the desired model
def _ask_for_model():
    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing

    FILE_DIALOG_OPTIONS = {'filetypes': [('PTV Vissim network files', '*.inpx'), ('All files', '*.*')],
                           'title': 'Choose VISSIM model'}

    filename = tkFileDialog.askopenfilename(**FILE_DIALOG_OPTIONS)  # show an "Open" dialog box and return the path to the selected file
    directory = os.path.split(filename)[0]
    global folderpath
    folderpath = directory.replace('/', '\\')
    # print folderpath
    return filename.replace('/', '\\')

def _write_data_to_json_file(data):
    json_data = json.dumps(data)
    f = open(json_filename, 'w')
    f.write(str(json_data))
    f.close()

# Closes the COM connection and exits the program
def _close_program(message):
    global Vissim
    Vissim = None
    # Display error message in console if any
    if message != "":
        print "ERROR MESSAGE: " + message
    print "\n== END OF SCRIPT =="
    sys.exit()

print "== START OF SCRIPT =="

inpx_file = _ask_for_model()
if inpx_file is None:
    _close_program("Please choose a file")

if inpx_file[-5:] != ".inpx":
    _close_program("Please choose .inpx file")


# create Vissim COM object
Vissim = com.Dispatch("Vissim.Vissim")

if Vissim is None:
    _close_program("Vissim program not found."
                  "It might be because the program is not installed on the machine")


# version-specific object: Vissim = com.Dispatch("Vissim.Vissim.9")
# Vissim.LoadNet("C:\Users\Ivaylo\Desktop\Examples\PTV Headquarters - Left-hand\Headquarters 14 LH.inpx")
# Vissim.LoadNet("C:\Users\Public\Documents\PTV Vision\PTV Vissim 9\Examples Demo\Roundabout London.UK\Roundabout London.inpx")
Vissim.LoadNet(inpx_file)

signalControllerCollection = Vissim.Net.SignalControllers.GetAll()

sgs = []
scs = []
for sc in signalControllerCollection:

    vissim_signal_controller_object = vissimclasses.VissimSignalController(sc)

    sc_data = {}

    sc_data['id'] = str(vissim_signal_controller_object.id)
    sc_data['name'] = str(vissim_signal_controller_object.name)
    sc_data['type'] = str(vissim_signal_controller_object.type)
    pua_to_global_ids = {}
    if str(vissim_signal_controller_object.type) == 'VAP':

        # test TFL files
        sc_data['vap_file'] = "C:\\Users\\Ivaylo\\Desktop\\A3 FT Model v2\\33.vap"
        sc_data['pua_file'] = "C:\\Users\\Ivaylo\\Desktop\\A3 FT Model v2\\33.pua"
        # sc_data['pua_file'] = "D:\\PyCharmProjects\\tests\\goodpuafile.pua"

        # actual data
        # sc_data['vap_file'] = _get_absolute_path_for_file(str(vissim_signal_controller_object.supply_file_1))
        # sc_data['pua_file'] = _get_absolute_path_for_file(str(vissim_signal_controller_object.supply_file_2))
        sc_data['initial_stage'] = puahelper.get_starting_stage_from_pua(sc_data['pua_file'])
        sc_data['max_stage'] = puahelper.get_max_stage_from_pua(sc_data['pua_file'])
        pua_to_global_ids = puahelper.read_and_map_signalgroups_from_pua(sc_data['pua_file'])
        pua_stages = puahelper.get_phases_in_stages_from_pua(sc_data['pua_file'])

        # specific for TFL models, will return -1 if it works with different models
        sc_data['cycle_length'] = vaphelper.get_cycle_length_from_vap(sc_data['vap_file'])
        sc_data['stage_timings'] = vaphelper.get_stage_lenghts_from_vap(sc_data['vap_file'])

    # key = sg.AttValue("No")
    # type = sg.AttValue("Type")
    print "Signal Controller Key: " + str(vissim_signal_controller_object.id)
    print "Signal Controller Type: " + str(vissim_signal_controller_object.type)
    print "Signal Controller Supply File 1: " + str(vissim_signal_controller_object.supply_file_1)
    print "Signal Controller Supply File 2: " + str(vissim_signal_controller_object.supply_file_2)

    # counter = 0
    sgCollection = sc.SGs.GetAll()
    for sg in sgCollection:
        vissim_signal_group_object = vissimclasses.VissimSignalGroup(sg)

        sg_data = {}
        sg_data['id'] = str(sg.AttValue("No"))

        print "Singal Group No: " + str(sg.AttValue("No"))

        # Crawl through the signal heads so the from link are found
        signal_heads_collection = sg.SigHeads.GetAll()

        vissim_signal_group_object.set_links_from_signalhead_collection(signal_heads_collection)
        print "Signal group from links:" + str(vissim_signal_group_object.links)

        sg_data['links'] = vissim_signal_group_object.links

        sg_no = str(sg.AttValue("No"))
        if pua_to_global_ids is not None:
            if sg_no in pua_to_global_ids:
                local_key = str(pua_to_global_ids[sg_no])
                green_stages = []
                if local_key in pua_stages:
                    green_stages = pua_stages[local_key]
                sg_data['phase_in_stages'] = green_stages

        sgs.append(sg_data)

        print "= END OF SIGNAL GROUP = \n"

    sc_data['signal_groups'] = sgs
    scs.append(sc_data)


print "= END OF SIGNAL CONTROLLER ="

_write_data_to_json_file(scs)

jsontopddl.convert_jsonfile_to_pddlproblem(json_filename, pddl_filename)

_close_program("")
