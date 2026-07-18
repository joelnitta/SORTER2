import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sorter2_readstats import parse_readstats

FIXTURE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")


def _load(name):
    with open(os.path.join(FIXTURE_DIR, name)) as f:
        return list(f)


def test_16line_flagstat_readdepth_and_coverage():
    # Regression test for joelnitta/sorter2r#13: this samtools build
    # emits an extra flagstat "+"-line, which used to shift the two
    # appended depth lines and drop readdepth entirely.
    stats = parse_readstats(_load("readstats_16line.txt"))
    assert stats["readdepth"] == [12]
    assert stats["coverage"] == [100]


def test_15line_flagstat_readdepth_and_coverage():
    # Same depth/coverage values, one fewer flagstat line -- content
    # matching must find them regardless of position.
    stats = parse_readstats(_load("readstats_15line.txt"))
    assert stats["readdepth"] == [12]
    assert stats["coverage"] == [100]


def test_flagstat_lines_parsed_by_label():
    stats = parse_readstats(_load("readstats_16line.txt"))
    assert stats["supplementary"] == [5]
    assert stats["mapped"] == [1662]


def test_header_line_ignored():
    stats = parse_readstats(_load("readstats_16line.txt"))
    assert "Read" not in stats
    assert "Statistics" not in stats
