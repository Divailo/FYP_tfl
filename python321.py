import sys
import win32com.client as com  # com library
import re

import dialoghelper
import pddlhelper
import vissimclasses
import stringhelper

def _close_program(message):
    # Display error message in console if any
    if message != "":
        print "ERROR MESSAGE: " + message
    print "\n== END OF SCRIPT =="
    sys.exit()

def look_for_sg_by_id(sc_id):
    sc = Vissim.Net.SignalControllers.FindItemByKey(sc_id)
    if sc is None:
        print 'No Signal Controller with id: ' + str(sc_id)
        return ''
    else:
        vap_file = sc.AttValue("SupplyFile1")
        return vap_file

def look_for_sg_by_name(name):
    for sc in Vissim.Net.SignalControllers.GetAll():
        if sc.AttValue('Name') == name:
            # TODO: check if it is a vap file
            return sc.AttValue('SupplyFile1')
    return ''


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
    print 'Looking for : ' + key
    filepath = ''
    look_for_that_prefix = vissimclasses.junction_prefix
    if stringhelper.does_string_contain_substring(key, look_for_that_prefix):
        sc_id = int(re.sub(look_for_that_prefix, '', key))
        print 'Looking for signal controller key: ' + str(sc_id)
        filepath = look_for_sg_by_id(sc_id)
    else:
        print 'Looking for signal controller name: ' + key
        filepath = look_for_sg_by_name(key)

    if filepath == '':
        print 'No VAP file for key: ' + key
    else:
        print 'Found VAP file for: ' + key + ' : ' + filepath
        # TODO call vaphelper.replace_timings(new_timing)

# look at keys. If __junction_id, look for id
# else look through all the scs and look for AttValue name
# signalControllerCollection = Vissim.Net.SignalControllers.GetAll()