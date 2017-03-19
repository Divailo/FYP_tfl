import win32com.client as com # com library
from Tkinter import Tk # gui library
import tkFileDialog # file dialog library
import re # regex library
import os # all kinds of shit library
# import threading # library for threads
import json # json library
import sys # all kinds of shit library x2

import VissimClasses

# initializes a file chooser to load the desired model
def ask_for_model():
    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    # FILEOPENOPTIONS = dict(filetypes = [('PTV Vissim network files','*.inpx'),('All files', '*.*')])
    filename = tkFileDialog.askopenfilename()  # show an "Open" dialog box and return the path to the selected file
    return os.path.abspath(filename)

def _does_string_contain_substring(originalstring, substring_to_look):
    if originalstring.find(substring_to_look) == -1:
        return False
    return True

def _get_actual_content_to_extract(file, key):
    # print "Filepath: " + filepath

    ACTUAL_CONTENT_SEPARATOR = "$"
    line = ""
    while line != key:
        line = file.readline().strip()

    while line != ACTUAL_CONTENT_SEPARATOR:
        line = file.readline().strip()

    lines = []
    while True:
        line = file.readline().strip()
        if _does_string_contain_substring(line, '$') == False:
            line = re.sub(' +',' ',line)
            lines.append(line)
            # print "Added line: " + line
        else:
            break

    return lines

# Closes the COM connection and exits the program
def close_program(message):
    global Vissim
    Vissim = None
    # Display error message in console if any
    if message != "":
        print "ERROR MESSAGE: " + message
    print "\n == END OF SCRIPT =="
    sys.exit()

# Opens a file and finds all the local (the ones used in the pua file) and global (the ones used in the model) ids of signal groups
def read_and_map_signalgroups_from_pua(filepath):
    SIGNAL_GROUPS_KEY = "$SIGNAL_GROUPS"
    opened_file = open(filepath)

    lines_to_read = _get_actual_content_to_extract(opened_file, SIGNAL_GROUPS_KEY)

    map = {}
    for line in lines_to_read:
        array_split = line.split(" ")
        if len(array_split) == 2:
            map[array_split[0]] = array_split[1]

    # for key, value in map.items():
    #     print key + " : " + value

    print "END OF MAP SIGNAL GROUPS TO IDS"

def get_pua_stages(filepath):
    # TODO
    STAGES_KEY = "$STAGES"

    green_stages = {}

# Returns integer, representing the first stage of the signal controller
def get_starting_stage_from_pua(filepath):
    STARTING_STAGE_KEY = "$STARTING_STAGE"
    opened_file = open(filepath)
    lines = _get_actual_content_to_extract(opened_file, STARTING_STAGE_KEY)
    STAGE_PREFIX = "Stage_"

    for line in lines:
        if _does_string_contain_substring(line, STAGE_PREFIX) == True:
            stage_number = int(line.replace(STAGE_PREFIX, ''))
            # print stage_number
            print "END OF FIND STARTING STAGE"
            return stage_number

    return -1


# def get_phases_in_stages(filepath):

def get_interstages_from_pua(filepth):
    # TODO
    return 0


# def getInput():
#     global  Vissim
#     command = raw_input("TELL ME SOMETHING")
#     if command.lower() == "close":
#         Vissim.Simulation.Stop()
#         Vissim = None
#         print "== END OF SCRIPT =="``
#         sys.exit(0)

print "== START OF SCRIPT =="

inpx_file = ask_for_model()
if inpx_file == None or inpx_file[-5:] != '.inpx':
    close_program("")



# create Vissim COM object
Vissim = com.Dispatch("Vissim.Vissim")
# version-specific object: Vissim = com.Dispatch("Vissim.Vissim.9")
# Vissim.LoadNet("C:\Users\Ivaylo\Desktop\Examples\PTV Headquarters - Left-hand\Headquarters 14 LH.inpx")
# Vissim.LoadNet("C:\Users\Public\Documents\PTV Vision\PTV Vissim 9\Examples Demo\Roundabout London.UK\Roundabout London.inpx")
Vissim.LoadNet(inpx_file)

# collection = Vissim.Net.SignalControllers.ItemByKey(1).SGs.GetAll()

signalControllerCollection = Vissim.Net.SignalControllers.GetAll()


for sc in signalControllerCollection:

    vissim_signal_controller_object = VissimClasses.VissimSignalController(sc)

    sc_data = {}
    sc_data['id'] = str(vissim_signal_controller_object.id)
    sc_data['type'] = str(vissim_signal_controller_object.type)
    if(str(vissim_signal_controller_object.type) == 'VAP'):
        sc_data['vap_file'] = str(vissim_signal_controller_object.supply_file_1)
        sc_data['pua_file'] = str(vissim_signal_controller_object.supply_file_2)
        read_and_map_signalgroups_from_pua(sc_data['pua_file'])
        sc_data['initial_stage'] = get_starting_stage_from_pua(sc_data['pua_file'])

    # key = sg.AttValue("No")
    # type = sg.AttValue("Type")
    print "Signal Controller Key: " + str(vissim_signal_controller_object.id)
    print "Signal Controller Type: " + str(vissim_signal_controller_object.type)
    print "Signal Controller Supply File 1: " + str(vissim_signal_controller_object.supply_file_1)
    print "Signal Controller Supply File 2: " + str(vissim_signal_controller_object.supply_file_2)

    sgs = []
    # counter = 0
    sgCollection = sc.SGs.GetAll()
    for sg in sgCollection:
        vissim_signal_group_object = VissimClasses.VissimSignalGroup(sg)
        #


        sg_data = {}
        sg_data['id'] = str(sg.AttValue("No"))
        sg_data['min_green'] = str(sg.AttValue("MinGreen"))

        print "Singal Group MinGreen: " + str(sg.AttValue("MinGreen"))
        print "Singal Group No: " + str(sg.AttValue("No"))
        # print "Singal Group MinRed: " + str(sg.AttValue("MinRed"))
        # print "Amber: " + str(sg.AttValue("Amber"))
        # print "ContrByCOM: " + str(sg.AttValue("ContrByCOM"))
        # print "GreenFlsh: " + str(sg.AttValue("GreenFlsh"))
        # print "Name: " + str(sg.AttValue("Name"))
        # print "RedAmber: " + str(sg.AttValue("RedAmber"))
        # print "SC: " + str(sg.AttValue("SC"))
        # print "SigState: " + str(sg.AttValue("SigState"))
        # print "tSigState: " + str(sg.AttValue("tSigState"))
        # print "Type: " + str(sg.AttValue("Type"))
        # print "\n"

        # Crawl through the signal heads so the from link are found
        signal_heads_collection = sg.SigHeads.GetAll()
        links = []

        for sh in signal_heads_collection:
            shLink = str(sh.Lane.Link.AttValue("No"))
            print "Signal Heaad Link: " + shLink
            links.append(shLink)
            # print "Signal Heaad Key: " + str(sh.AttValue("No"))
            # print "Signal Head's group: " + str(sh.AttValue("SG"))

        # Using set so unique values are ensured
        unique_links = set(links)
        vissim_signal_group_object.setLinks(unique_links)
        print "Signal group from links:" + str(vissim_signal_group_object.links)

        links_data = []
        counter = 0
        for link in unique_links:
            counter = counter + 1
            sg_data['Link '+ str(counter)] = str(link)

        sgs.append(sg_data)

        print "= END OF SIGNAL GROUP = \n"

sc_data['signal_groups'] = sgs

print "= END OF SIGNAL CONTROLLER ="

json_data = json.dumps(sc_data)

f = open('out.txt', 'w')
f.write(str(json_data))
f.close()


close_program("")

# command = raw_input("Run Simulation? y/n \n")
# if command.lower() == "y":
#     print "Running simulation"
#     Vissim.Simulation.RunContinuous()


#Close COM "Server"
# Vissim = None