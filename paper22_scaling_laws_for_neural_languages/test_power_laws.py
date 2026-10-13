"""
Tests for paper22 scaling laws (Kaplan et al., 2001.08361).

The implementation under test lives in scaling_laws.py.
"""

from scaling_laws import power_law


def test_power_law():
    assert power_law(1, 2, 2, 2) == 4
