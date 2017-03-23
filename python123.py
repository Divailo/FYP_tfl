import win32com.client as com # com library
from Tkinter import Tk # gui library
import tkFileDialog # file dialog library
import os # all kinds of shit library
# import threading # library for threads
import json # json library
import sys # all kinds of shit library x2

import puahelper
import vaphelper
import VissimClasses

# initializes a file chooser to load the desired model
def ask_for_model():
    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    # FILEOPENOPTIONS = dict(filetypes = [('PTV Vissim network files','*.inpx'),('All files', '*.*')])
    filename = tkFileDialog.askopenfilename()  # show an "Open" dialog box and return the path to the selected file
    return os.path.abspath(filename)

# Closes the COM connection and exits the program
def close_program(message):
    global Vissim
    Vissim = None
    # Display error message in console if any
    if message != "":
        print "ERROR MESSAGE: " + message
    print "\n == END OF SCRIPT =="
    sys.exit()

# def get_phases_in_stages(filepath):

def get_interstages_from_pua(filepth):
    # TODO
    return 0

print " == START OF SCRIPT =="

inpx_file = ask_for_model()
if inpx_file is None:
    close_program("Please choose a file")

if inpx_file[-5:] != ".inpx":
    close_program("Please choose .inpx file")



# create Vissim COM object
Vissim = com.Dispatch("Vissim.Vissim")

if Vissim is None:
    close_program("Vissim program not found. It might be because the program is not installed on the machine")

# version-specific object: Vissim = com.Dispatch("Vissim.Vissim.9")
# Vissim.LoadNet("C:\Users\Ivaylo\Desktop\Examples\PTV Headquarters - Left-hand\Headquarters 14 LH.inpx")
# Vissim.LoadNet("C:\Users\Public\Documents\PTV Vision\PTV Vissim 9\Examples Demo\Roundabout London.UK\Roundabout London.inpx")
Vissim.LoadNet(inpx_file)

signalControllerCollection = Vissim.Net.SignalControllers.GetAll()


for sc in signalControllerCollection:

    vissim_signal_controller_object = VissimClasses.VissimSignalController(sc)

    pua_to_global_ids = {}
    pua_stages = {}

    sc_data = {}
    sc_data['id'] = str(vissim_signal_controller_object.id)
    sc_data['name'] = str(vissim_signal_controller_object.name)
    sc_data['type'] = str(vissim_signal_controller_object.type)
    if(str(vissim_signal_controller_object.type) == 'VAP'):
        # test TFL files
        sc_data['vap_file'] = "C:\\Users\\Ivaylo\\Desktop\\A3 FT Model v2\\33.vap"
        # sc_data['pua_file'] = "C:\\Users\\Ivaylo\\Desktop\\A3 FT Model v2\\33.pua"
        # sc_data['vap_file'] = str(vissim_signal_controller_object.supply_file_1)
        sc_data['pua_file'] = str(vissim_signal_controller_object.supply_file_2)
        sc_data['curr_stage'] = puahelper.get_starting_stage_from_pua(sc_data['pua_file'])
        pua_to_global_ids = puahelper.read_and_map_signalgroups_from_pua(sc_data['pua_file'])
        pua_stages = puahelper.get_pua_stages(sc_data['pua_file'])
        sc_data['max_stage'] = len(pua_stages)
        # specific for TFL models, will return -1 if it works with different models
        sc_data['cycle_length'] = vaphelper.get_cycle_length_from_vap(sc_data['vap_file'])

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

        sg_no = str(sg.AttValue("No"))
        if sg_no in pua_to_global_ids:
            local_key = str(pua_to_global_ids[sg_no])
            green_stages = []
            if local_key in pua_stages:
                green_stages = pua_stages[local_key]
            sg_data['phase_in_stage'] = green_stages

        sgs.append(sg_data)

        print "= END OF SIGNAL GROUP = \n"

sc_data['signal_groups'] = sgs

print "= END OF SIGNAL CONTROLLER ="

json_data = json.dumps(sc_data)

f = open('out.txt', 'w')
f.write(str(json_data))
f.close()

close_program("")