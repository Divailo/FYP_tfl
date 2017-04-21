import re

# Attribute Keys
SC_ID_KEY = 'No'
SC_TYPE_KEY = 'Type'
SC_NAME_KEY = 'Name'
SC_VAPFILE_ATTRIBUTE_KEY = 'SupplyFile1'
SC_PUAFILE_ATTRIBUTE_KEY = 'SupplyFile2'

SG_ID_KEY = 'No'

SC_VAP_TYPE = 'VAP'

junction_prefix = '__junction_'

    # class VissimSignalController(object):
    #     """
    #     Atrribtues:
    #
    #         Active
    #             - If this option is not selected, all signal heads which are assigned to this signal control are not active. That means the vehicles / pedestrians do not react to the signal heads
    #         CycSec
    #             - Result attribute: Returns the current cycle second during the simulation
    #         CycTm
    #             - Optional cycle time. Duration in seconds
    #         CycTmIsVar
    #             - Cycle time is variable
    #         Debug
    #             - At type VAP: The debug-mode is active.For this, VisVAP has to be open.
    #         Freq
    #             - Frequency which is been used for the signal control. The value may not exceed the simulation resolution.
    #         GuiFile
    #             - Filename in the GUI
    #         Name
    #         No
    #             - Unique ID
    #         Offset
    #             - For the synchronization, for example, within a green wave
    #         ProgFile
    #             - This is the VS-PLUS version with which the node is to be controlled. Always use the same VS-PLUS version to create the supply file with Visual VS-PLUS in the simulation and for the application on the actual control device.
    #         ProgNo
    #             - The signal program or daily signal program list that you want to simulate (Defining and editing daily signal program lists). A change of program is possible if the simulation run is in single-step mode. If the new signal program number is confirmed with OK, the changeover is triggered in the next simulation second.
    #         SCDetRecLabelDet
    #             - Label type for detectors in signal control detector record.
    #         SCDetRecLabelSG
    #             - Label type for signal groups in signal control detector record.
    #         SCDetRecShortNam
    #             - If this option is selected, the shortname of the attributes is used within the SC-detector protocol evaluation file.
    #         SigTmsTabAutoConfig
    #             - If this option is selected, a default configuration for the signal times table is used.
    #         SigTmsTabLabelDet
    #             - Label type for detectors in signal times table
    #         SigTmsTabLabelSG
    #             - Label type for signal groups in signal times table.
    #         SupplyFile1
    #         SupplyFile2
    #         SupplyFile3
    #         Type    - BalanceCentral
    #                 - D4
    #                 - Econolite
    #                 - EpicsBalanceLocal
    #                 - External
    #                 - FixedTime
    #                 - LISA
    #                 - McCain
    #                 - RBC
    #                 - SCATS
    #                 - SCOOT
    #                 - TL
    #                 - TRENDS
    #                 - VAP
    #                 - VSPlus
    #         WTTFiles
    #             - Value type tables: These contain the data types from the control logic which are to be shown in the Signal Control Detector Record or in the Signal Times Table window, as well as the display type. If the control consists of several modules, you must specify the associated *.wtt file for each module
    #     """


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


    # def sigfile(objectContainer):
    #     if objectContainer.type == "FIXEDTIME":
    #         return objectContainer.supply_file_2
    #     else:
    #         return None

    # """
    # Attributes:
    #     Amber
    #         - Duration of amber in one cycle. Only valif for specific SC types.
    #     ContrByCOM
    #         - If this option is selected, the signal group is controlled by COM.
    #     GreenFlsh
    #         - Duration of green-flashing in one cycle. Only valif for specific SC types
    #     MinGreen
    #         - Minimum duration at green. Only valif for specific SC types.
    #     MinRed
    #         - Minimum duration at red. Only valif for specific SC types
    #     Name
    #         - Name of signal group
    #     No
    #         - Unique number of the signal group
    #     RedAmber
    #         - Duration of red-amber in one cycle. Only valif for specific SC types
    #     SC
    #         - The corresponding signal control from the left list of the coupled list
    #     SigState
    #         - Current signal state during the simulation
    #
    #     Type
    #         - Flashing
    #         - GreenArrow
    #         - Normal
    # """

    # def __init__(self, objectContainer):
    #     self.name = objectContainer.AttValue("Name")
    #     self.id = objectContainer.AttValue("No")
    #     self.type = objectContainer.AttValue("Type")
    #     self.signal_controller = objectContainer.AttValue("SC")

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
