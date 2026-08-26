import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sorter2_stage3_header import build_hybrid_header


HIT_PARTS = ["L201", "cl2", "Nitta4483", "ogracilis", "ph0"]


def test_default_omits_specimen_for_backwards_compatibility():
    # Regression guard: the default output shape must stay identical
    # to pre-#16 behavior for existing callers.
    header = build_hybrid_header(HIT_PARTS, "Kato009", "ochinensis", "ph0")
    assert header == ">L201_cl2_Kato009_ochinensis_ogracilis_ph0"


def test_tag_specimen_false_matches_default():
    header = build_hybrid_header(
        HIT_PARTS, "Kato009", "ochinensis", "ph0", tag_specimen=False
    )
    assert header == ">L201_cl2_Kato009_ochinensis_ogracilis_ph0"


def test_tag_specimen_true_inserts_specimen_before_phase_tag():
    # Regression test for joelnitta/sorter2r#16: the matched diploid
    # specimen (splithits2[2]) is discarded by default; opting in
    # should insert it right before the trailing phase tag, without
    # moving any other field.
    header = build_hybrid_header(
        HIT_PARTS, "Kato009", "ochinensis", "ph0", tag_specimen=True
    )
    assert header == ">L201_cl2_Kato009_ochinensis_ogracilis_Nitta4483_ph0"


def test_ph0_and_ph1_are_parallel():
    header0 = build_hybrid_header(
        HIT_PARTS, "Kato009", "ochinensis", "ph0", tag_specimen=True
    )
    header1 = build_hybrid_header(
        HIT_PARTS, "Kato009", "ochinensis", "ph1", tag_specimen=True
    )
    assert header0.replace("ph0", "ph1") == header1
