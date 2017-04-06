junction_prefix = '__junction_'

class VissimSignalController(object):
    """
    Atrribtues:

        Active
            - If this option is not selected, all signal heads which are assigned to this signal control are not active. That means the vehicles / pedestrians do not react to the signal heads
        CycSec
            - Result attribute: Returns the current cycle second during the simulation
        CycTm
            - Optional cycle time. Duration in seconds
        CycTmIsVar
            - Cycle time is variable
        Debug
            - At type VAP: The debug-mode is active.For this, VisVAP has to be open.
        Freq
            - Frequency which is been used for the signal control. The value may not exceed the simulation resolution.
        GuiFile
            - Filename in the GUI
        Name
        No
            - Unique ID
        Offset
            - For the synchronization, for example, within a green wave
        ProgFile
            - This is the VS-PLUS version with which the node is to be controlled. Always use the same VS-PLUS version to create the supply file with Visual VS-PLUS in the simulation and for the application on the actual control device.
        ProgNo
            - The signal program or daily signal program list that you want to simulate (Defining and editing daily signal program lists). A change of program is possible if the simulation run is in single-step mode. If the new signal program number is confirmed with OK, the changeover is triggered in the next simulation second.
        SCDetRecLabelDet
            - Label type for detectors in signal control detector record.
        SCDetRecLabelSG
            - Label type for signal groups in signal control detector record.
        SCDetRecShortNam
            - If this option is selected, the shortname of the attributes is used within the SC-detector protocol evaluation file.
        SigTmsTabAutoConfig
            - If this option is selected, a default configuration for the signal times table is used.
        SigTmsTabLabelDet
            - Label type for detectors in signal times table
        SigTmsTabLabelSG
            - Label type for signal groups in signal times table.
        SupplyFile1
        SupplyFile2
        SupplyFile3
        Type    - BalanceCentral
                - D4
                - Econolite
                - EpicsBalanceLocal
                - External
                - FixedTime
                - LISA
                - McCain
                - RBC
                - SCATS
                - SCOOT
                - TL
                - TRENDS
                - VAP
                - VSPlus
        WTTFiles
            - Value type tables: These contain the data types from the control logic which are to be shown in the Signal Control Detector Record or in the Signal Times Table window, as well as the display type. If the control consists of several modules, you must specify the associated *.wtt file for each module
    """

    _alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
                 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    _counter = -1

    def __init__(self, objectContainer):
        self.id = objectContainer.AttValue("No")
        self.type = objectContainer.AttValue("Type")
        self._configurename(objectContainer.AttValue("Name"))
        self.supply_file_1 = objectContainer.AttValue("SupplyFile1")
        self.supply_file_2 = objectContainer.AttValue("SupplyFile2")

    def id(self):
        return self.id

    # Gives it some name, so it better looking PDDL can be constructed
    def _configurename(self, name):
        if name != "":
            self.name = name
        else:
            # This was such a fun idea :( . Goodbye sweet prince
            # self._counter = self._counter + 1
            # self.name = "Junction_"
            # so the program supports unlimited amount of signal controllers -> after Z , it goes to AA
            # aretheretoomanyjunctions = self._counter / len(self._alphabet) - 1
            # if aretheretoomanyjunctions >= 0:
            #     self.name = self.name + self._alphabet[aretheretoomanyjunctions]
            # self.name = self.name + self._alphabet[self._counter % len(self._alphabet)]
            self.name = junction_prefix + str(self.id)

    def vapfile(self):
        if self.type == "VAP":
            return self.supply_file_1
        else:
            return None

    def puafile(self):
        if self.type == "VAP":
            return self.supply_file_2
        else:
            return None

    def sigfile(self):
        if self.type == "FIXEDTIME":
            return self.supply_file_2
        else:
            return None


class VissimSignalGroup(object):

    """
    Attributes:
        Amber
            - Duration of amber in one cycle. Only valif for specific SC types.
        ContrByCOM
            - If this option is selected, the signal group is controlled by COM.
        GreenFlsh
            - Duration of green-flashing in one cycle. Only valif for specific SC types
        MinGreen
            - Minimum duration at green. Only valif for specific SC types.
        MinRed
            - Minimum duration at red. Only valif for specific SC types
        Name
            - Name of signal group
        No
            - Unique number of the signal group
        RedAmber
            - Duration of red-amber in one cycle. Only valif for specific SC types
        SC
            - The corresponding signal control from the left list of the coupled list
        SigState
            - Current signal state during the simulation

        Type
            - Flashing
            - GreenArrow
            - Normal
    """

    def __init__(self, objectContainer):
        self.name = objectContainer.AttValue("Name")
        self.id = objectContainer.AttValue("No")
        self.type = objectContainer.AttValue("Type")
        self.signal_controller = objectContainer.AttValue("SC")

    def set_links_from_signalhead_collection(self, signal_heads_collection):
        _links = []

        for sh in signal_heads_collection:
            # create json object for the link
            sh_data = {}
            # get the sh's link
            sh_link = sh.Lane.Link
            sh_link_name = sh_link.AttValue("Name")
            # Check if there is no name given to the link
            if sh_link_name == "":
                # Give unique name to the link
                sh_link_name = "l_" + str(sh_link.AttValue("No"))

            # Put the name in the object
            sh_data['name'] = sh_link_name
            _links.append(sh_data)


        self.links = _links

    def links(self):
        return self.links

    def set_local_pua_id(self, id):
        self.pua_id = id

    def local_pua_id(self):
        return self.pua_id