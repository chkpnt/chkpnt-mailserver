import pytest
from compare import compare

@pytest.fixture
def file_with_actual_content(tmp_path):
    actual_content = u"""\
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

def test_exact_match(file_with_actual_content):
    excepted_content = u"""\
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
    is_matching, result = compare(file_with_actual_content, excepted_content, "$$ ", " $$")

    assert is_matching == True
    assert result == []

def test_does_not_match(file_with_actual_content):
    excepted_content = u"""\
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
    
    is_matching, result = compare(file_with_actual_content, excepted_content, "$$ ", " $$")

    assert is_matching == False
    assert result[0] == "Line 1: 'Date: Wed, 24 Apr 2019 00:01:35 +0200' does not match 'Date: Wed, 24 Apr 1999 00:01:35 +0200'"
    assert result[1] == "Line 5: 'Message-ID: <5cbf8b3f.KRE6KgzO9+saDxMn%vagrant@client.localdomain>' does not match 'Message-ID: <id@client.localdomain>'"

def test_match_regex(file_with_actual_content):
    excepted_content = u"""\
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
    
    is_matching, result = compare(file_with_actual_content, excepted_content, "$$ ", " $$")

    assert is_matching == True
    assert result == []

def test_regex_does_not_match(file_with_actual_content):
    excepted_content = u"""\
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
"""
    
    is_matching, result = compare(file_with_actual_content, excepted_content, "$$ ", " $$")

    assert is_matching == False
    assert result[0] == r"Line 1: 'Date: Wed, 24 Apr 2019 00:01:35 +0200' does not match 'Date: Wed, $$ \d{1,2} Jan \d{4} \d\d:\d\d:\d\d $$ +0200'"

@pytest.fixture
def file_with_only_date_header(tmp_path):
    actual_content = u"""\
Date: Wed, 24 Apr 2019 00:01:35 +0200
"""
    file = tmp_path / "file.txt"
    file.write_text(actual_content)
    return str(file)

def test_multiple_regex_in_one_line(file_with_only_date_header):
    excepted_content = u"""\
Date: $$ \w{3} $$, 24 Apr 2019 $$ \d\d:\d\d:\d\d $$ +0200$$ .* $$
"""
    
    is_matching, result = compare(file_with_only_date_header, excepted_content, "$$ ", " $$")

    assert is_matching == True
    assert result == []

def test_regex_needs_an_end_delimiter_to_be_recognized_as_such(file_with_only_date_header):
    excepted_content = u"""\
Date: $$ .* $$, 24 Apr 2019 $$ .* $$ +0200$$ .*
"""
    
    is_matching, result = compare(file_with_only_date_header, excepted_content, "$$ ", " $$")

    assert is_matching == False
    assert result[0] == r"Line 1: 'Date: Wed, 24 Apr 2019 00:01:35 +0200' does not match 'Date: $$ .* $$, 24 Apr 2019 $$ .* $$ +0200$$ .*'"
    
def test_other_delimiters(file_with_only_date_header):
    excepted_content = u"""\
Date: AUF \w{3} ZU, 24 Apr 2019 AUF \d\d:\d\d:\d\d ZU +0200
"""
    
    is_matching, result = compare(file_with_only_date_header, excepted_content, "AUF ", " ZU")

    assert is_matching == True
    assert result == []

