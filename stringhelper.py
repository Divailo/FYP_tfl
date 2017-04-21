import re # regex library

def does_string_contain_substring(originalstring, substring_to_look):
    if originalstring.find(substring_to_look) == -1:
        return False
    return True

# Returns an integer when the string contains it
# On error return -1
def parse_integer_from_string(string):
    to_return = int(re.search(r'\d+', string).group())
    if to_return is not None:
        return to_return
    else:
        print "Array entry not an integer: " + string
        return -1

def escape_vap_comments(tobeeditted):
    return re.sub(r"(\/\*){1}([^\*\/])+(\*\/){1}",r"", tobeeditted)

# Removes the '[' and ']' from the part after the '=' in an array element inside the vap file
def remove_brackets_for_vap_array(arraystring):
    return arraystring.replace('[', '').replace(']', '')

def get_good_time_string(time_int):
    good_string = str(time_int)
    if (time_int) < 10:
        good_string = '0' + good_string
    return good_string