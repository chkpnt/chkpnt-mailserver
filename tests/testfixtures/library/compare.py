#!/usr/bin/python

from ansible.module_utils.basic import *
from os.path import expanduser
import itertools

def __do_not_escape_between(string, start_delimiter, end_delimiter):
    pos = 0
    is_looking_for_start_delimiter = True
    result = []
    while True:
        if is_looking_for_start_delimiter:
            start = string.find(start_delimiter, pos)
            if start == -1: break
            is_looking_for_start_delimiter = False
            pos = start + len(start_delimiter)
        else:
            end = string.find(end_delimiter, pos)
            if end == -1: break
            is_looking_for_start_delimiter = True
            pos = end + len(end_delimiter)
            result.extend(range(start, end + len(end_delimiter)))
            start = None
            end = None
    return result

_special_chars = frozenset('()[]{}?*+-|^$\\.&~# \t\n\r\v\f')

def __escape(string, regex_start_delimiter, regex_end_delimiter):
    do_not_escape_between = __do_not_escape_between(string, regex_start_delimiter, regex_end_delimiter)
    s = list(string)
    special_chars = _special_chars
    for i, c in enumerate(string):
        if i in do_not_escape_between:
            continue
        if c in special_chars:
            s[i] = "\\" + c
    escaped_string = ''.join(s)
    return escaped_string \
        .replace(regex_start_delimiter, '') \
        .replace(regex_end_delimiter, '')

def compare(file, expected_content, regex_start_delimiter, regex_end_delimiter):
    file = expanduser(file)
    with open(file) as f:
        content = f.read().splitlines()
    
    result = []
    line_number = 0
    for line, expected_line in itertools.izip_longest(content, expected_content.splitlines(), fillvalue=""):
        line_number += 1
        escaped_expected_line = __escape(expected_line, regex_start_delimiter, regex_end_delimiter)
        if not re.search("^{}$".format(escaped_expected_line), line):
            result.append("Line {}: '{}' does not match '{}'".format(line_number, line, expected_line))

    return len(result) == 0, result

def main():
    fields = {
        "file": { "required": True, "type": "str" },
        "with_content": { "required": True, "type": "str" },
        "regex_start_delimiter": { "required": False, "type": "str", "default": "$$ " },
        "regex_end_delimiter": { "required": False, "type": "str", "default": " $$" },
    }
    module = AnsibleModule(argument_spec=fields)
    is_matching, result = compare(
        module.params['file'],
        module.params['with_content'],
        module.params['regex_start_delimiter'],
        module.params['regex_end_delimiter']
    )
    if is_matching:
        module.exit_json(changed=False, meta=result)
    else:
        module.fail_json(msg=result)


if __name__ == '__main__':
    main()