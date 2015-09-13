"""
Tests for the backtranslate.backtranslate module.
"""


from backtranslate.backtranslate import (
    reverse_translation_table, one_subst, one_subst_without_dna, _compare_dict)


class TestParser(object):
    """
    Test the backtranslate.backtranslate module.
    """
    def setup(self):
        self.back_table = reverse_translation_table()


    def test_with_dna_1(self):
        assert _compare_dict(
            one_subst(self.back_table, 'TGG', '*'),
            {1: set([('G', 'A')]), 2: set([('G', 'A')])})


    def test_with_dna_2(self):
        assert _compare_dict(
            one_subst(self.back_table, 'GTA', 'L'),
            {0: set([('G', 'C'), ('G', 'T')])})


    def test_without_dna_1(self):
        assert _compare_dict(
            one_subst_without_dna(self.back_table, 'R', '*'),
            {0: set([('C', 'T'), ('A', 'T')])})


    def test_without_dna_2(self):
        assert _compare_dict(
            one_subst_without_dna(self.back_table, 'N', 'K'),
            {2: set([('T', 'G'), ('C', 'A'), ('C', 'G'), ('T', 'A')])})


    def test_without_dna_3(self):
        assert _compare_dict(
            one_subst_without_dna(self.back_table, 'R', 'S'), {
                0: set([('C', 'A')]),
                2: set([('G', 'C'), ('A', 'T'), ('A', 'C'), ('G', 'T')])})
