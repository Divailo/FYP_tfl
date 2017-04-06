import sys
import win32com.client as com  # com library

import dialoghelper
import pddlhelper

def _close_program(message):
    # Display error message in console if any
    if message != "":
        print "ERROR MESSAGE: " + message
    print "\n== END OF SCRIPT =="
    sys.exit()


print "== START OF SCRIPT =="

plan_file = dialoghelper.ask_for_plan()
if plan_file is None:
    _close_program("Please choose a file")

new_timing  = pddlhelper._get_new_stages_information(plan_file)
if new_timing == {}:
    _close_program("Could not read signal timing from " + plan_file)

inpx_file = dialoghelper.ask_for_model()

Vissim = com.Dispatch("Vissim.Vissim")

if Vissim is None:
    _close_program("Vissim program not found."
                   "It might be because the program is not installed on the machine")

Vissim.LoadNet(inpx_file)

for key in new_timing.keys():
    print key

# look at keys. If __junction_id, look for id
# else look through all the scs and look for AttValue name
# signalControllerCollection = Vissim.Net.SignalControllers.GetAll()