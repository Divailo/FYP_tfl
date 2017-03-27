import re # regex library

def does_string_contain_substring(originalstring, substring_to_look):
    if originalstring.find(substring_to_look) == -1:
        return False
    return True

def escape_vap_comments(tobeeditted):
    return re.sub(r"(\/\*){1}([^\*\/])+(\*\/){1}",r"", tobeeditted)