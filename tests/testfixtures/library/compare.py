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
    if string == None:
        return None
    
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

def _pairwise(iterable):
    "s -> (s0, s1), (s1,s2), (s2, s3), ..., (sn, None)"
    a, b = itertools.tee(iterable)
    next(b, None)
    return itertools.izip_longest(a, b, fillvalue=None)

def compare(file, expected_content, regex_start_delimiter, regex_end_delimiter, skip_line_pattern=None):
    file = expanduser(file)
    with open(file) as f:
        content = f.read().splitlines()
    
    expected_lines_iter = _pairwise(expected_content.splitlines())
    expected_line, expected_next_line = next(expected_lines_iter, (None, None))
    result = []
    line_number = 0
    for line in content:
        line_number += 1
        escaped_expected_line = __escape(expected_line, regex_start_delimiter, regex_end_delimiter)
        escaped_expected_next_line = __escape(expected_next_line, regex_start_delimiter, regex_end_delimiter)

        if escaped_expected_line != None and re.search("^{}$".format(escaped_expected_line), line):
            expected_line, expected_next_line = next(expected_lines_iter, (None, None))
            continue
        
        if escaped_expected_next_line != None and re.search("^{}$".format(escaped_expected_next_line), line):
            next(expected_lines_iter, (None, None))
            expected_line, expected_next_line = next(expected_lines_iter, (None, None))
            continue
        
        if expected_line == skip_line_pattern:
            continue
        
        result.append("Line {}: '{}' does not match '{}'".format(line_number, line, expected_line))
        expected_line, expected_next_line = next(expected_lines_iter, (None, None))
        
    while expected_line != None:
        if expected_line == skip_line_pattern and expected_next_line == None:
            break
        result.append("Line {}: EOF does not match '{}'".format(line_number + 1, expected_line))
        expected_line, expected_next_line = next(expected_lines_iter, (None, None))

    return len(result) == 0, result

def main():
    fields = {
        "file": { "required": True, "type": "str" },
        "with_content": { "required": True, "type": "str" },
        "regex_start_delimiter": { "required": False, "type": "str", "default": "$$ " },
        "regex_end_delimiter": { "required": False, "type": "str", "default": " $$" },
        "skip_line_pattern": { "required": False, "type": "str", "default": None}
    }
    module = AnsibleModule(argument_spec=fields)
    is_matching, result = compare(
        module.params['file'],
        module.params['with_content'],
        module.params['regex_start_delimiter'],
        module.params['regex_end_delimiter'],
        module.params['skip_line_pattern']
    )
    if is_matching:
        module.exit_json(changed=False, meta=result)
    else:
        module.fail_json(msg=result)


if __name__ == '__main__':
    main()