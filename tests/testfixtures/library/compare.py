#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import re
from os.path import expanduser
import itertools

class FileComparer(object):
    
    class ExpectedLines():
        def __init__(self, lines):
            self._iter = self._pairwise(lines)
            self.current, self.next = next(self._iter, (None, None))
        
        def current_is_consumed(self):
            self.current, self.next = next(self._iter, (None, None))

        def _pairwise(self, iterable):
            # "s -> (s0, s1), (s1,s2), (s2, s3), ..., (sn, None)"
            a, b = itertools.tee(iterable)
            next(b, None)
            return itertools.izip_longest(a, b, fillvalue=None)

    def __init__(self, regex_start_delimiter, regex_end_delimiter, skip_line_pattern):
        self.regex_start_delimiter = regex_start_delimiter
        self.regex_end_delimiter = regex_end_delimiter
        self.skip_line_pattern = skip_line_pattern

    def matches(self, file, expected_content):
        file = expanduser(file)
        with open(file) as f:
            content = f.read().splitlines()
        
        expected_lines = self.ExpectedLines(expected_content.splitlines())

        result = []
        line_number = 0
        for line in content:
            line_number += 1

            if self._is(line=line, matched_by=expected_lines.current):
                expected_lines.current_is_consumed()
                continue
            
            if self._is(line=line, matched_by=expected_lines.next):
                expected_lines.current_is_consumed()
                expected_lines.current_is_consumed()
                continue
            
            if expected_lines.current == self.skip_line_pattern:
                continue
            
            result.append("Line {}: '{}' does not match '{}'".format(line_number, line, expected_lines.current))
            expected_lines.current_is_consumed()

        while expected_lines.current != None:
            if expected_lines.current == self.skip_line_pattern and expected_lines.next == None:
                break
            result.append("Line {}: EOF does not match '{}'".format(line_number + 1, expected_lines.current))
            expected_lines.current_is_consumed()

        return len(result) == 0, result

    def _is(self, line, matched_by):
        if matched_by == None:
            return False
        if matched_by == self.skip_line_pattern:
            return False
        
        escaped_expected_line = self._escape(matched_by, self.regex_start_delimiter, self.regex_end_delimiter)
        return re.search("^{}$".format(escaped_expected_line), line)

    _chars_to_escape = frozenset('()[]{}?*+-|^$\\.&~# \t\n\r\v\f')

    def _escape(self, string, regex_start_delimiter, regex_end_delimiter):
        do_not_escape_between = self._do_not_escape_between(string, regex_start_delimiter, regex_end_delimiter)
        s = list(string)
        special_chars = FileComparer._chars_to_escape
        for i, c in enumerate(string):
            if i in do_not_escape_between:
                continue
            if c in special_chars:
                s[i] = "\\" + c
        escaped_string = ''.join(s)
        return escaped_string \
            .replace(regex_start_delimiter, '') \
            .replace(regex_end_delimiter, '')

    def _do_not_escape_between(self, string, start_delimiter, end_delimiter):
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

def main():
    fields = {
        "file": { "required": True, "type": "str" },
        "with_content": { "required": True, "type": "str" },
        "regex_start_delimiter": { "required": False, "type": "str", "default": "$$ " },
        "regex_end_delimiter": { "required": False, "type": "str", "default": " $$" },
        "skip_line_pattern": { "required": False, "type": "str", "default": "..."}
    }
    module = AnsibleModule(argument_spec=fields)

    comparer = FileComparer(
        regex_start_delimiter=module.params['regex_start_delimiter'],
        regex_end_delimiter=module.params['regex_end_delimiter'],
        skip_line_pattern=module.params['skip_line_pattern']
    )
    is_matching, result = comparer.matches(
        module.params['file'],
        module.params['with_content'],
    )
    if is_matching:
        module.exit_json(changed=False, meta=result)
    else:
        module.fail_json(msg=result)

if __name__ == '__main__':
    main()