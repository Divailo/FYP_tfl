import sys
import win32com.client as com  # com library
import re

import dialoghelper
import pddlhelper
import vissimclasses
import stringhelper
import vaphelper

def _close_program(message):
    # Display error message in console if any
    if message != "":
        print "ERROR MESSAGE: " + message
    print "\n== END OF SCRIPT =="
    sys.exit()


def _look_for_sg_by_id(sc_id):
    sc = Vissim.Net.SignalControllers.ItemByKey(sc_id)
    if sc is None:
        print 'No Signal Controller with id: ' + str(sc_id)
        return None
    else:
        return sc

def _look_for_sg_by_name(name):
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

for key, value in new_timing.items():
    print 'Looking for : ' + key
    filepath = ''
    look_for_that_prefix = vissimclasses.junction_prefix
    if stringhelper.does_string_contain_substring(key, look_for_that_prefix):
        sc_id = int(re.sub(look_for_that_prefix, '', key))
        print 'Looking for signal controller key: ' + str(sc_id)
        signal_controller = _look_for_sg_by_id(sc_id)
    else:
        print 'Looking for signal controller name: ' + key
        signal_controller = _look_for_sg_by_name(key)
        # filepath = _look_for_sg_by_name(key)

    # vap_filepath = signal_controller.AttValue("SupplyFile1")
    vap_filepath = "C:\\Users\\Ivaylo\\Desktop\\A3 FT Model v2\\33.vap"

    if vap_filepath == '':
        print 'No VAP file for key: ' + key
    else:
        vap_filepath = dialoghelper._get_absolute_path_for_file(vap_filepath)
        print 'Found VAP file for: ' + key + ' : ' + vap_filepath
        # TODO call vaphelper.replace_timings(timings)
        # TODO create a new file. and then signal_controller.SetAttValue('SupplyFile1',nefile_path)
        # TODO make sure to not override anything
        vaphelper.edit_timing_changes(vap_filepath, value)

# look at keys. If __junction_id, look for id
# else look through all the scs and look for AttValue name
# signalControllerCollection = Vissim.Net.SignalControllers.GetAll()