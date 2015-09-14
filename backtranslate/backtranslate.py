from collections import defaultdict

from Bio.Data import CodonTable
from Levenshtein import hamming


def cmp_subst(subst_1, subst_2):
    """
    Compare two substitution sets.

    :arg dict subst_1: Substitution set.
    :arg dict subst_2: Substitution set.

    :returns bool: True if `subst_1` equals `subst2`, False otherwise.
    """
    if len(subst_1) != len(subst_2):
        return False

    for item in subst_1:
        if subst_1[item] != subst_2[item]:
            return False

    return True


def reverse_translation_table(table_id=1):
    """
    Calculate a reverse translation table.

    :arg int table_id: Translation table id.

    :returns dict: Set of possible codons indexed by amino acid.
    """
    forward_table = CodonTable.unambiguous_dna_by_id[table_id]
    back_table = defaultdict(set)

    back_table['*'] = set(forward_table.stop_codons)

    for codon in forward_table.forward_table:
        back_table[forward_table.forward_table[codon]].add(codon)

    return back_table


class BackTranslate(object):
    """
    Back translation.
    """
    def __init__(self, table_id=1):
        """
        Initialise the class.

        :arg int table_id: Translation table id.
        """
        self._back_table = reverse_translation_table(table_id)


    def _one_subst(self, substitutions, reference_codon, amino_acid):
        """
        Find single nucleotide substitutions that given a reference codon
        explains an observed amino acid.

        :arg dictsubstitutions: Set of single nucleotide substitutions indexed
            by position.
        :arg str reference_codon: Original codon.
        :arg str amino_acid: Observed amino acid.
        """
        for codon in self._back_table[amino_acid]:
            if hamming(codon, reference_codon) == 1:
                for position in range(3):
                    if codon[position] != reference_codon[position]:
                        substitutions[position].add(
                            (reference_codon[position], codon[position]))


    def with_dna(self, reference_codon, amino_acid):
        """
        Find single nucleotide substitutions that given a reference codon
        explains an observed amino acid.

        :arg str reference_codon: Original codon.
        :arg str amino_acid: Observed amino acid.

        :returns dict: Set of single nucleotide substitutions indexed by
            position.
        """
        substitutions = defaultdict(set)

        self._one_subst(substitutions, reference_codon, amino_acid)

        return substitutions


    def without_dna(self, reference_amino_acid, amino_acid):
        """
        Find single nucleotide substitutions that given a reference amino acid
        explains an observed amino acid.

        :arg str reference_amino_acid: Original amino acid.
        :arg str amino_acid: Observed amino acid.

        :returns dict: Set of single nucleotide substitutions indexed by
            position.
        """
        substitutions = defaultdict(set)

        for reference_codon in self._back_table[reference_amino_acid]:
            self._one_subst(substitutions, reference_codon, amino_acid)

        return substitutions


    def improvable(self):
        """
        Calculate all pairs of amino acid substututions that can be improved by
        looking at the underlying codon.

        :returns list: List of improvable substitutions.
        """
        substitutions = set()

        for reference_amino_acid in self._back_table:
            for sample_amino_acid in self._back_table:
                substitutions_without_dna = self.without_dna(
                    reference_amino_acid, sample_amino_acid)
                for codon in self._back_table[reference_amino_acid]:
                    substitutions_with_dna = self.with_dna(
                        codon, sample_amino_acid)
                    if (substitutions_with_dna and not
                            cmp_subst(substitutions_without_dna,
                            substitutions_with_dna) and
                            reference_amino_acid != sample_amino_acid):
                        substitutions.add(
                            (reference_amino_acid, sample_amino_acid))

        return substitutions
