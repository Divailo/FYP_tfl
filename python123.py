#import com library
import win32com.client as com
# import gui library
from Tkinter import Tk
import tkFileDialog
import os
# import threading
import sys
import VissimClasses

def ask_for_model():
    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    filename = tkFileDialog.askopenfilename()  # show an "Open" dialog box and return the path to the selected file
    return os.path.abspath(filename)

def close_program(message):
    global Vissim
    Vissim = None
    print "== END OF SCRIPT =="
    sys.exit()

# def getInput():
#     global  Vissim
#     command = raw_input("TELL ME SOMETHING")
#     if command.lower() == "close":
#         Vissim.Simulation.Stop()
#         Vissim = None
#         print "== END OF SCRIPT =="
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

    # key = sg.AttValue("No")
    # type = sg.AttValue("Type")
    print "Signal Controller Key: " + str(vissim_signal_controller_object.id)
    print "Signal Controller Type: " + str(vissim_signal_controller_object.type)
    print "Signal Controller Supply File 1: " + str(vissim_signal_controller_object.supply_file_1)
    print "Signal Controller Supply File 2: " + str(vissim_signal_controller_object.supply_file_2)

    # counter = 0
    sgCollection = sc.SGs.GetAll()
    for sg in sgCollection:
        vissim_signal_group_object = VissimClasses.VissimSignalGroup(sg)
        #
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
        print "= END OF SIGNAL GROUP = \n"

print "= END OF SIGNAL CONTROLLER ="

close_program("")

# command = raw_input("Load sample? y/n \n")
#
# if command.lower() == "n":
#     print "== END OF SCRIPT =="
#     Vissim = None
#     sys.exit(0)
# else:
#     Vissim.LoadNet("C:\Users\Ivaylo\Desktop\Examples\PTV Headquarters - Left-hand\Headquarters 14 LH.inpx")
#
# command = raw_input("Run Simulation? y/n \n")
# if command.lower() == "y":
#     print "Running simulation"
#     Vissim.Simulation.RunContinuous()


#Close COM "Server"
# Vissim = None