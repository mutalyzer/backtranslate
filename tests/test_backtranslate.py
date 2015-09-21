"""
Tests for the backtranslate.backtranslate module.
"""


from __future__ import (
    absolute_import, division, print_function, unicode_literals)
from future.builtins import str, zip

from backtranslate.backtranslate import BackTranslate, cmp_subst


class TestParser(object):
    """
    Test the backtranslate.backtranslate module.
    """
    def setup(self):
        self.bt = BackTranslate()


    def test_with_dna_1(self):
        assert cmp_subst(
            self.bt.with_dna('TGG', '*'),
            {1: set([('G', 'A')]), 2: set([('G', 'A')])})


    def test_with_dna_2(self):
        assert cmp_subst(
            self.bt.with_dna('GTA', 'L'),
            {0: set([('G', 'C'), ('G', 'T')])})


    def test_without_dna_1(self):
        assert cmp_subst(
            self.bt.without_dna('R', '*'),
            {0: set([('C', 'T'), ('A', 'T')])})


    def test_without_dna_2(self):
        assert cmp_subst(
            self.bt.without_dna('N', 'K'),
            {2: set([('T', 'G'), ('C', 'A'), ('C', 'G'), ('T', 'A')])})


    def test_without_dna_3(self):
        assert cmp_subst(
            self.bt.without_dna('R', 'S'), {
                0: set([('C', 'A')]),
                2: set([('G', 'C'), ('A', 'T'), ('A', 'C'), ('G', 'T')])})
