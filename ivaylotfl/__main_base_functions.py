from datetime import datetime # datetime library
from sys import exit # system exit function
import __stringhelper
import __dialoghelper

def close_program(logger, message):
    # Display error message in dialog if any
    if message != '':
        logger.error('ERROR MESSAGE: ' + message)
        __dialoghelper.show_error_box_with_message(message)
    print '\n== END OF SCRIPT =='
    exit()


def get_absolute_path_for_file(filepath):
    return __dialoghelper.get_absolute_path_for_file(filepath)


# Gets a timestamp to append it to the log file
def get_timestamp_string():
    date_object = datetime.now().date()
    time_object = datetime.now().time()
    month_string = __stringhelper.get_good_time_string(date_object.month)
    day_string = __stringhelper.get_good_time_string(date_object.day)
    hours_string = __stringhelper.get_good_time_string(time_object.hour)
    minutes_string = __stringhelper.get_good_time_string(time_object.minute)
    seconds_string = __stringhelper.get_good_time_string(time_object.second)
    date_string = 'D:' + day_string + '/' + month_string + '/' + str(date_object.year)
    time_string = '\tT:' + hours_string + ':' + minutes_string + ':' + seconds_string
    return date_string + time_string


