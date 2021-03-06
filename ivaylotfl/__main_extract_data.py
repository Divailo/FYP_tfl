import win32com.client as com  # com library

import logging

import puahelper
import vaphelper
import vissimhelper
import pddlhelper
import jsonhelper
import __dialoghelper
from __main_base_functions import close_program, get_absolute_path_for_file, get_timestamp_string

def main():
    sc_counter = 0
    # initiliaze logger
    logger = logging.getLogger('tfl_ivaylo')
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler('extract_data.log')
    fh.setLevel(logging.INFO)
    logger.addHandler(fh)
    logger.info('==' + get_timestamp_string() + '==')
    logger.info('START OF SCRIPT')
    inpx_file = __dialoghelper.ask_for_model()
    if not __dialoghelper.is_file_chosen(inpx_file):
        close_program(logger, 'Please choose a file')
    if not __dialoghelper.check_model_file(inpx_file):
        close_program(logger, 'Please choose a valid Vissim model file/inpx file')

    # create Vissim COM object
    vissim = vissimhelper.initialise_vissim(com)
    if vissim is None:
        close_program(logger, 'Vissim program not found.'
                       'It might be because the program is not installed on the machine')

    vissimhelper.bring_vissim_to_front(vissim)
    vissimhelper.load_vissim_network(vissim, inpx_file)
    signal_controller_collection = vissimhelper.get_signal_controllers(vissim)
    scs_in_total = len(signal_controller_collection)
    sc_json_array = []

    for sc in signal_controller_collection:
        sc_data = {}
        sgs = []

        sc_type = vissimhelper.get_sc_type(sc)
        # sc_data[jsonhelper.JSON_SC_TYPE_KEY] =
        pua_to_global_ids = {}
        if sc_type == 'VAP':
            sc_id = vissimhelper.get_sc_id(sc)
            sc_name = vissimhelper.get_sc_name(sc)
            vap_file_location = get_absolute_path_for_file(str(vissimhelper.get_vapfile(sc)))
            pua_file_location = get_absolute_path_for_file(str(vissimhelper.get_puafile(sc)))
            cycle_length = vaphelper.get_cycle_length_from_vap(vap_file_location)
            pua_to_global_ids = puahelper.read_and_map_signalgroups_from_pua(pua_file_location)
            pua_stages = puahelper.get_phases_in_stages_from_pua(pua_file_location)
            initial_stage = puahelper.get_starting_stage_from_pua(pua_file_location)
            max_stage = puahelper.get_max_stage_from_pua(pua_file_location)
            stage_timings = vaphelper.get_stage_lenghts_from_vap(vap_file_location, max_stage)
            logger.info('Signal Controller Id: ' + str(vissimhelper.get_sc_id(sc)))
            logger.info('Signal Controller Supply File 1: ' + str(vap_file_location))
            logger.info('Signal Controller Supply File 2: ' + str(pua_file_location))
            logger.info('Pua to global ids: ' + str(pua_to_global_ids))
            # serialize
            sc_data[jsonhelper.JSON_SC_ID_KEY] = str(sc_id)
            sc_data[jsonhelper.JSON_SC_NAME_KEY] = sc_name
            sc_data[jsonhelper.JSON_SC_VAPFILE_KEY] = vap_file_location
            sc_data[jsonhelper.JSON_SC_PUAFILE_KEY] = pua_file_location
            sc_data[jsonhelper.JSON_SC_INITIAL_STAGE_KEY] = initial_stage
            sc_data[jsonhelper.JSON_SC_MAX_STAGE_KEY] = max_stage
            # specific for TFL models, will return -1 if it works with different models
            sc_data[jsonhelper.JSON_SC_CYCLE_LENGTH_KEY] = cycle_length
            sc_data[jsonhelper.JSON_SC_STAGE_TIMINGS_KEY] = stage_timings
            sc_counter += 1
        else:
            logger.info('Non-VAP signal controllers not supported!')
            continue

        sgCollection = sc.SGs.GetAll()
        for sg in sgCollection:
            sg_data = {}
            sg_id = vissimhelper.get_sg_id(sg)
            sg_id_string = str(sg_id)
            sg_link_names = vissimhelper.get_link_names(sg)
            sg_links = []
            for link_name in sg_link_names:
                sg_link = {}
                sg_link['name'] = link_name
                sg_links.append(sg_link)
            logger.info('Signal Group No: ' + sg_id_string)
            logger.info('Signal group from links: ' + str(sg_links))
            if pua_to_global_ids is not None:
                if sg_id_string in pua_to_global_ids:
                    local_key = str(pua_to_global_ids[sg_id_string])
                    green_stages = []
                    if local_key in pua_stages:
                        green_stages = pua_stages[local_key]
                    sg_data[jsonhelper.JSON_SG_PHASE_IN_STAGES_KEY] = green_stages
                sg_data[jsonhelper.JSON_SG_ID_KEY] = sg_id
                sg_data[jsonhelper.JSON_SG_LINKS_KEY] = sg_links

            sgs.append(sg_data)
            logger.info('= END OF SIGNAL GROUP = \n')

        sc_data[jsonhelper.JSON_SC_SG_KEY] = sgs
        sc_json_array.append(sc_data)
        logger.info('= END OF SIGNAL CONTROLLER =')
    logger.info('= ALL DATA COLLECTED =')

    # Create JSON file
    json_file_path = jsonhelper.create_json_filename_for_model(inpx_file)
    jsonhelper.write_data_to_json_file(json_file_path, sc_json_array)
    # Create PDDL file
    pddl_filename = __dialoghelper.ask_to_save()
    if pddl_filename is None:
        close_program(logger, '')
    pddlhelper.convert_jsonfile_to_pddlproblem(json_file_path, pddl_filename)
    sc_dialog_line = str(sc_counter) + '/' + str(scs_in_total) + ' signal controllers data exported\n'
    json_dialog_line = 'JSON file saved to: ' + json_file_path + '\n'
    pddl_dialog_line = 'PDDL file saved to' + pddl_filename
    __dialoghelper.show_info_box_with_message(sc_dialog_line + json_dialog_line + pddl_dialog_line)
    close_program(logger, '')
