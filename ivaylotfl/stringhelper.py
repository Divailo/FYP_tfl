import re  # regex library


def does_string_contain_substring(originalstring, substring_to_look):
    if originalstring.find(substring_to_look) == -1:
        return False
    return True


# Returns an integer when the string contains it
# On error return -1
def parse_integer_from_string(search_in):
    to_return = int(re.search(r'\d+', search_in).group())
    if to_return is not None:
        return to_return
    else:
        return -1


def get_good_time_string(time_int):
    good_string = str(time_int)
    if (time_int) < 10:
        good_string = '0' + good_string
    return good_string
