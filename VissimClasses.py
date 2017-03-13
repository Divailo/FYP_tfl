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

    def __init__(self, objectContainer):
        self.active = objectContainer.AttValue("Active")
        self.id = objectContainer.AttValue("No")
        self.type = objectContainer.AttValue("Type")
        self.progfile = objectContainer.AttValue("ProgFile")
        self.progid = objectContainer.AttValue("ProgNo")
        self.supply_file_1 = objectContainer.AttValue("SupplyFile1")
        self.supply_file_2 = objectContainer.AttValue("SupplyFile2")

    # does not work for some reason
    # def type(self):
    #     return self.type

    def id(self):
        return self.id

    # ffs the com method is called FindItemByKey while the attribute is called No
    # consistency much!
    def key(self):
        return self.id

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

    def progid(self):
        return self.progid

    # def progfile(self):
    #     return self.progfile
    def active(self):
        return self.active



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
        self.amber = objectContainer.AttValue("Amber")
        self.controlled_by_com = objectContainer.AttValue("ContrByCOM")
        self.green_flashing_time = objectContainer.AttValue("GreenFlsh")
        self.min_green = objectContainer.AttValue("MinGreen")
        self.min_red = objectContainer.AttValue("MinRed")
        self.name = objectContainer.AttValue("Name")
        self.id = objectContainer.AttValue("No")
        self.red_amber_time = objectContainer.AttValue("RedAmber")
        self.signal_controller = objectContainer.AttValue("SC")
        self.current_signal_stage = objectContainer.AttValue("SigState")
        self.signal_stage_runtime = objectContainer.AttValue("tSigState")
        self.type = objectContainer.AttValue("Type")

    def key(self):
        return self.id