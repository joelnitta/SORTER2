import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sorter2_progenitor_match import match_progenitor_row


def test_compound_match_wins_over_species_level():
    # Regression test for joelnitta/sorter2r#14: a compound
    # voucher_species row must take precedence over a species-level
    # row for the same progenitor value, so non-monophyletic species
    # can be given per-voucher progenitor clades.
    csv_data = [
        {"hybrid": "cthysanostomum", "progenitor": "ph0", "clade": "prog1"},
        {"hybrid": "Iimura18_cthysanostomum", "progenitor": "ph0", "clade": "prog3"},
    ]
    clade, warn = match_progenitor_row(
        ["Iimura18", "cthysanostomum", "ph0"], csv_data
    )
    assert clade == "prog3"
    assert warn is None


def test_species_level_match_used_when_no_compound_row():
    csv_data = [
        {"hybrid": "cthysanostomum", "progenitor": "ph0", "clade": "prog1"},
        {"hybrid": "Iimura18_cthysanostomum", "progenitor": "ph0", "clade": "prog3"},
    ]
    clade, warn = match_progenitor_row(
        ["Liu18", "cthysanostomum", "ph0"], csv_data
    )
    assert clade == "prog1"
    assert warn == "cthysanostomum"


def test_no_matching_row_returns_none():
    csv_data = [
        {"hybrid": "cthysanostomum", "progenitor": "ph0", "clade": "prog1"},
    ]
    clade, warn = match_progenitor_row(
        ["Iimura46", "cgrande", "ph0"], csv_data
    )
    assert clade is None
    assert warn is None


def test_compound_match_found_regardless_of_row_order():
    csv_data = [
        {"hybrid": "Iimura18_cthysanostomum", "progenitor": "ph0", "clade": "prog3"},
        {"hybrid": "cthysanostomum", "progenitor": "ph0", "clade": "prog1"},
    ]
    clade, warn = match_progenitor_row(
        ["Iimura18", "cthysanostomum", "ph0"], csv_data
    )
    assert clade == "prog3"
    assert warn is None
