#import com library
import win32com.client as com
import threading
import sys
import VissimClasses

def getInput():
    global  Vissim
    command = raw_input("TELL ME SOMETHING")
    if command.lower() == "close":
        Vissim.Simulation.Stop()
        Vissim = None
        print "== END OF SCRIPT =="
        sys.exit(0)

print "== START OF SCRIPT =="
# create Vissim COM object
Vissim = com.Dispatch("Vissim.Vissim")
# version-specific object: Vissim = com.Dispatch("Vissim.Vissim.9")
# Vissim.LoadNet("C:\Users\Ivaylo\Desktop\Examples\PTV Headquarters - Left-hand\Headquarters 14 LH.inpx")
Vissim.LoadNet("C:\Users\Public\Documents\PTV Vision\PTV Vissim 9\Examples Demo\Roundabout London.UK\Roundabout London.inpx")

# collection = Vissim.Net.SignalControllers.ItemByKey(1).SGs.GetAll()

signalControllerCollection = Vissim.Net.SignalControllers.GetAll()

for sc in signalControllerCollection:

    vissim_signal_controlle_object = VissimClasses.VissimSignalController(sc)

    # key = sg.AttValue("No")
    # type = sg.AttValue("Type")
    print "Signal Controller Key: " + str(vissim_signal_controlle_object.id)
    print "Signal Controller Type: " + str(vissim_signal_controlle_object.type)
    print "Signal Controller Supply File 1: " + str(vissim_signal_controlle_object.supply_file_1)
    print "Signal Controller Supply File 2: " + str(vissim_signal_controlle_object.supply_file_2)

    # counter = 0
    sgCollection = sc.SGs.GetAll()
    for sg in sgCollection:
        vissim_signal_group_object = VissimClasses.VissimSignalGroup(sg)
        # print "Signal group: " + str(counter)
        #
        # print "Amber: " + str(sg.AttValue("Amber"))
        # print "ContrByCOM: " + str(sg.AttValue("ContrByCOM"))
        # print "GreenFlsh: " + str(sg.AttValue("GreenFlsh"))
        print "Singal Group MinGreen: " + str(sg.AttValue("MinGreen"))
        print "Singal Group MinRed: " + str(sg.AttValue("MinRed"))
        # print "Name: " + str(sg.AttValue("Name"))
        print "Singal Group No: " + str(sg.AttValue("No"))
        # print "RedAmber: " + str(sg.AttValue("RedAmber"))
        # print "SC: " + str(sg.AttValue("SC"))
        # print "SigState: " + str(sg.AttValue("SigState"))
        # print "tSigState: " + str(sg.AttValue("tSigState"))
        # print "Type: " + str(sg.AttValue("Type"))
        # print "\n"
        # counter = counter + 1
        signal_heads_collection = sg.SigHeads.GetAll()
        links = []

        for sh in signal_heads_collection:
            shLink = str(sh.Lane.Link.AttValue("No"))
            print "Signal Heaad Link: " + shLink
            links.append(shLink)
            # print "Signal Heaad Key: " + str(sh.AttValue("No"))
            # print "Signal Head's group: " + str(sh.AttValue("SG"))

        uniquelinks = set(links)
        vissim_signal_group_object.setLinks(uniquelinks)
        print "Signal group from links:" + vissim_signal_group_object.links
        print "= END OF SIGNAL GROUP = \n"

print "= END OF SIGNAL CONTROLLER ="

print "== END OF SCRIPT =="


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