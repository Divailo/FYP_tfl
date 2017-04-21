import re

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

junction_prefix = '__junction_'


def check_vissim_initialised(com_vissim):
    return com_vissim is not None


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


def vapfile(signal_controller):
    if signal_controller.AttValue(SC_TYPE_KEY) == SC_VAP_TYPE:
        return signal_controller.AttValue(SC_VAPFILE_ATTRIBUTE_KEY)
    else:
        return None


def puafile(signal_controller):
    if signal_controller.AttValue(SC_TYPE_KEY) == SC_VAP_TYPE:
        return signal_controller.AttValue(SC_PUAFILE_ATTRIBUTE_KEY)
    else:
        return None


# ====================================
#               Signal Groups
# ====================================
def get_sg_id(signal_group):
    return signal_group.AttValue(SG_ID_KEY)


def get_links_from_signalhead_collection(signal_group, signal_heads_collection):
    _links = []

    for sh in signal_heads_collection:
        # create json object for the link
        sh_data = {}  # get the sh's link
        sh_link = sh.Lane.Link
        sh_link_name = sh_link.AttValue("Name")
        # Check if there is no name given to the link
        if sh_link_name == "":
            # Give unique name to the link
            sh_link_name = "l_" + str(sh_link.AttValue("No"))

        # Put the name in the object
        sh_data['name'] = sh_link_name
        _links.append(sh_data)

    return _links


def set_local_pua_id(signal_group, id):
    signal_group.pua_id = id


def local_pua_id(signal_group):
    return signal_group.pua_id
