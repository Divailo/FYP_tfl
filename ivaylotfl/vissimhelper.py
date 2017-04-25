import re

import jsonhelper
import puahelper
import vaphelper

# SC attribute keys
SC_ID_KEY = 'No'
SC_TYPE_KEY = 'Type'
SC_NAME_KEY = 'Name'
SC_VAPFILE_ATTRIBUTE_KEY = 'SupplyFile1'
SC_PUAFILE_ATTRIBUTE_KEY = 'SupplyFile2'
#
SC_VAP_TYPE = 'VAP'
# SG attribute keys
SG_ID_KEY = 'No'
# Link asttribute keys
LINK_ID_KEY = 'No'
LINK_NAME_KEY = 'Name'

junction_prefix = '__junction_'


def initialise_vissim(com_object):
    return com_object.Dispatch('Vissim.Vissim')


def bring_vissim_to_front(vissim_object):
    vissim_object.BringToFront()


def load_vissim_network(vissim_ojbect, filepath):
    vissim_ojbect.LoadNet(filepath)


def get_signal_controllers(vissim_object):
    return vissim_object.Net.SignalControllers.GetAll()


def get_sc_by_id(vissim_object, sc_id):
    sc = vissim_object.Net.SignalControllers.ItemByKey(sc_id)
    if sc is None:
        return None
    else:
        return sc


def save_network(vissim_object):
    vissim_object.SaveNet()


# ====================================
#              Signal Controllers
# ====================================
def set_vap_file(signal_controller, filepath):
    signal_controller.SetAttValue(SC_VAPFILE_ATTRIBUTE_KEY, filepath)


def get_sc_id(signal_controller):
    return signal_controller.AttValue(SC_ID_KEY)


# Gives it some name, so it better looking PDDL can be constructed
def get_sc_name(signal_controller):
    original_sc_name = signal_controller.AttValue(SC_NAME_KEY)
    if original_sc_name != '':
        unique_sc_name = re.sub('\s', '_', original_sc_name) + '_' + str(signal_controller.AttValue(SC_ID_KEY))
    else:
        unique_sc_name = junction_prefix + str(signal_controller.AttValue(SC_ID_KEY))
    return unique_sc_name


def get_sc_type(signal_controller):
    return str(signal_controller.AttValue(SC_TYPE_KEY))


def get_signal_groups(signal_controller):
    return signal_controller.SGs.GetAll()


def get_vapfile(signal_controller):
    if signal_controller.AttValue(SC_TYPE_KEY) == SC_VAP_TYPE:
        return signal_controller.AttValue(SC_VAPFILE_ATTRIBUTE_KEY)
    else:
        return None


def get_puafile(signal_controller):
    if signal_controller.AttValue(SC_TYPE_KEY) == SC_VAP_TYPE:
        return signal_controller.AttValue(SC_PUAFILE_ATTRIBUTE_KEY)
    else:
        return None


# ====================================
#               Signal Groups
# ====================================
def get_sg_id(signal_group):
    return signal_group.AttValue(SG_ID_KEY)


def get_sg_signalheads(signal_group):
    return signal_group.SigHeads.GetAll()


# Retuns an array of
def get_link_names(signal_group):
    signal_heads_collection = get_sg_signalheads(signal_group)
    _links = []
    for sh in signal_heads_collection:
        # create json object for the link
        sh_link = sh.Lane.Link
        sh_link_name = sh_link.AttValue(LINK_NAME_KEY)
        # Check if there is no name given to the link
        if sh_link_name == "":
            # Give unique name to the link
            sh_link_name = "l_" + str(sh_link.AttValue(LINK_ID_KEY))
        _links.append(sh_link_name)
    return _links
