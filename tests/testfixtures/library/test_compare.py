import pytest
from compare import FileComparer

@pytest.fixture
def sut():
    return FileComparer(
        regex_start_delimiter="$$ ",
        regex_end_delimiter=" $$",
        skip_line_pattern="..."
    )

@pytest.fixture
def file_with_actual_content(tmp_path):
    actual_content = """\
Date: Wed, 24 Apr 2019 00:01:35 +0200
From: vagrant@client.localdomain
To: test@mail-sink.theirdomain.test
Subject: Test
Message-ID: <5cbf8b3f.KRE6KgzO9+saDxMn%vagrant@client.localdomain>
User-Agent: Heirloom mailx 12.5 7/5/10
MIME-Version: 1.0
Content-Type: text/plain; charset=us-ascii
Content-Transfer-Encoding: 7bit

Test-Body
"""
    file = tmp_path / "file.txt"
    file.write_text(actual_content)
    return str(file)

@pytest.fixture
def file_with_only_date_header(tmp_path):
    actual_content = """\
Date: Wed, 24 Apr 2019 00:01:35 +0200
"""
    file = tmp_path / "file.txt"
    file.write_text(actual_content)
    return str(file)

class TestPositive:

    def test_exact_match(self, sut, file_with_actual_content):
        excepted_content = """\
Date: Wed, 24 Apr 2019 00:01:35 +0200
From: vagrant@client.localdomain
To: test@mail-sink.theirdomain.test
Subject: Test
Message-ID: <5cbf8b3f.KRE6KgzO9+saDxMn%vagrant@client.localdomain>
User-Agent: Heirloom mailx 12.5 7/5/10
MIME-Version: 1.0
Content-Type: text/plain; charset=us-ascii
Content-Transfer-Encoding: 7bit

Test-Body
"""
        is_matching, result = sut.matches(file_with_actual_content, excepted_content)

        assert is_matching == True
        assert result == []

    def test_expected_lines_can_contain_regex(self, sut, file_with_actual_content):
        excepted_content = r"""\
Date: Wed, $$ \d{1,2} \w\w\w \d{4} \d\d:\d\d:\d\d $$ +0200
From: vagrant@client.localdomain
To: test@mail-sink.theirdomain.test
Subject: Test
Message-ID: <$$ .* $$@client.localdomain>
User-Agent: Heirloom mailx 12.5 7/5/10
MIME-Version: 1.0
Content-Type: text/plain; charset=us-ascii
Content-Transfer-Encoding: 7bit

Test-Body
"""
        
        is_matching, result = sut.matches(file_with_actual_content, excepted_content)

        assert is_matching == True
        assert result == []

    def test_multiple_regex_in_one_line(self, sut, file_with_only_date_header):
        excepted_content = r"""\
Date: $$ \w{3} $$, 24 Apr 2019 $$ \d\d:\d\d:\d\d $$ +0200$$ .* $$
"""
        
        is_matching, result = sut.matches(file_with_only_date_header, excepted_content)

        assert is_matching == True
        assert result == []

    def test_other_delimiters(self, sut, file_with_only_date_header):
        sut.regex_start_delimiter = "AUF "
        sut.regex_end_delimiter = " ZU"
        excepted_content = r"""\
Date: AUF \w{3} ZU, 24 Apr 2019 AUF \d\d:\d\d:\d\d ZU +0200
"""
        
        is_matching, result = sut.matches(file_with_only_date_header, excepted_content)

        assert is_matching == True
        assert result == []

    def test_with_skipped_lines__one_block_is_matched(self, sut, file_with_actual_content):
        excepted_content = """\
...
To: test@mail-sink.theirdomain.test
Subject: Test
...
"""
        is_matching, result = sut.matches(file_with_actual_content, excepted_content)

        assert is_matching == True
        assert result == []

    def test_with_skipped_lines__two_block_are_matched(self, sut, file_with_actual_content):
        excepted_content = """\
...
To: test@mail-sink.theirdomain.test
Subject: Test
...
Content-Transfer-Encoding: 7bit
...
"""
        is_matching, result = sut.matches(file_with_actual_content, excepted_content)

        assert is_matching == True
        assert result == []

    def test_with_skipped_lines__one_block_specifies_EOF(self, sut, file_with_actual_content):
        excepted_content = """\
...
To: test@mail-sink.theirdomain.test
Subject: Test
...
Content-Transfer-Encoding: 7bit
...
Test-Body
"""
        is_matching, result = sut.matches(file_with_actual_content, excepted_content)

        assert is_matching == True
        assert result == []

    def test_with_skipped_lines__blocks_can_contain_regex(self, sut, file_with_actual_content):
        excepted_content = """\
...
To: $$ .+@.+ $$
Subject: Test
...
Content-Transfer-Encoding: $$ .* $$
...
Test-Body
"""
        is_matching, result = sut.matches(file_with_actual_content, excepted_content)

        assert is_matching == True
        assert result == []


class TestNegative:

    def test_two_lines_are_not_matching(self, sut, file_with_actual_content):
        excepted_content = """\
Date: Wed, 24 Apr 1999 00:01:35 +0200
From: vagrant@client.localdomain
To: test@mail-sink.theirdomain.test
Subject: Test
Message-ID: <id@client.localdomain>
User-Agent: Heirloom mailx 12.5 7/5/10
MIME-Version: 1.0
Content-Type: text/plain; charset=us-ascii
Content-Transfer-Encoding: 7bit

Test-Body
"""
        
        is_matching, result = sut.matches(file_with_actual_content, excepted_content)

        assert is_matching == False
        assert result[0] == "Line 1: 'Date: Wed, 24 Apr 2019 00:01:35 +0200' does not match 'Date: Wed, 24 Apr 1999 00:01:35 +0200'"
        assert result[1] == "Line 5: 'Message-ID: <5cbf8b3f.KRE6KgzO9+saDxMn%vagrant@client.localdomain>' does not match 'Message-ID: <id@client.localdomain>'"

    def test_regex_does_not_match(self, sut, file_with_actual_content):
        excepted_content = r"""
Date: Wed, $$ \d{1,2} Jan \d{4} \d\d:\d\d:\d\d $$ +0200
From: vagrant@client.localdomain
To: test@mail-sink.theirdomain.test
Subject: Test
Message-ID: <$$ .* $$@client.localdomain>
User-Agent: Heirloom mailx 12.5 7/5/10
MIME-Version: 1.0
Content-Type: text/plain; charset=us-ascii
Content-Transfer-Encoding: 7bit

Test-Body
""".strip()
        
        is_matching, result = sut.matches(file_with_actual_content, excepted_content)

        assert is_matching == False
        assert len(result) == 1
        assert result[0] == r"Line 1: 'Date: Wed, 24 Apr 2019 00:01:35 +0200' does not match 'Date: Wed, $$ \d{1,2} Jan \d{4} \d\d:\d\d:\d\d $$ +0200'"

    def test_regex_needs_an_end_delimiter_to_be_recognized_as_such(self, sut, file_with_only_date_header):
        excepted_content = """\
Date: $$ .* $$, 24 Apr 2019 $$ .* $$ +0200$$ .*
"""
        
        is_matching, result = sut.matches(file_with_only_date_header, excepted_content)

        assert is_matching == False
        assert result[0] == r"Line 1: 'Date: Wed, 24 Apr 2019 00:01:35 +0200' does not match 'Date: $$ .* $$, 24 Apr 2019 $$ .* $$ +0200$$ .*'"

    def test_with_skipped_lines__one_line_does_not_match(self, sut, file_with_actual_content):
        excepted_content = """\
...
To: test@mail-sink.theirdomain.test
Subject: Does not match
...
"""
        is_matching, result = sut.matches(file_with_actual_content, excepted_content)

        assert is_matching == False
        assert len(result) == 1
        assert result[0] == "Line 4: 'Subject: Test' does not match 'Subject: Does not match'"

    def test_with_skipped_lines__one_line_in_second_block_does_not_match(self, sut, file_with_actual_content):
        excepted_content = """\
...
To: test@mail-sink.theirdomain.test
Subject: Test
...
Content-Transfer-Encoding: 42bit
...
"""
        is_matching, result = sut.matches(file_with_actual_content, excepted_content)

        assert is_matching == False
        # The line with the wrong "Content-Transfer-Encoding" is not matched because
        # the "..." after the Subject line is greedy.
        assert len(result) == 2
        assert result[0] == "Line 12: EOF does not match '...'"
        assert result[1] == "Line 12: EOF does not match 'Content-Transfer-Encoding: 42bit'"

    def test_with_skipped_lines__multiple_lines_in_different_blocks_does_not_match(self, sut, file_with_actual_content):
        excepted_content = """\
...
To: test@mail-sink.theirdomain.test
Subject: Does not match
...
Content-Transfer-Encoding: 42bit
...
"""
        is_matching, result = sut.matches(file_with_actual_content, excepted_content)

        assert is_matching == False
        # The line with the wrong "Content-Transfer-Encoding" is not matched because
        # the "..." after the Subject line is greedy.
        assert len(result) == 3
        assert result[0] == "Line 4: 'Subject: Test' does not match 'Subject: Does not match'"
        assert result[1] == "Line 12: EOF does not match '...'"
        assert result[2] == "Line 12: EOF does not match 'Content-Transfer-Encoding: 42bit'"

    def test_with_skipped_lines__regex_does_not_match(self, sut, file_with_actual_content):
        excepted_content = r"""
...
To: test@mail-sink.theirdomain.test
Subject: $$ \d+ $$
...
""".strip()
        is_matching, result = sut.matches(file_with_actual_content, excepted_content)

        assert is_matching == False
        assert len(result) == 1
        assert result[0] == r"Line 4: 'Subject: Test' does not match 'Subject: $$ \d+ $$'"
