from collections import defaultdict

from Bio.Data import CodonTable, IUPACData
from extractor.variant import Allele, DNAVar, ISeq, ISeqList
from Levenshtein import hamming


def _three_to_one():
    """
    The three letter to one letter table for amino acids including stop.

    :returns dict: Three letter to one letter amino acids table.
    """
    protein_letters_3to1 = dict(IUPACData.protein_letters_3to1_extended)
    protein_letters_3to1.update({'Ter': '*'})

    return protein_letters_3to1


def _compare_dict(d1, d2):
    """
    """
    if len(d1) != len(d2):
        return False

    for item in d1:
        if d1[item] != d2[item]:
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


def one_subst(back_table, reference_codon, amino_acid):
    """
    Find single nucleotide substitutions that given a reference codon explains
    an observed amino acid.

    :arg dict back_table: Reverse translation table.
    :arg str reference_codon: Original codon.
    :arg str amino_acid: Observed amino acid.

    :returns dict: Set of single nucleotide substitutions indexed by position.
    """
    substitutions = defaultdict(set)

    for codon in back_table[amino_acid]:
        if hamming(codon, reference_codon) == 1:
            for position in range(3):
                if codon[position] != reference_codon[position]:
                    substitutions[position].add(
                        (reference_codon[position], codon[position]))

    return substitutions


def one_subst_without_dna(back_table, reference_amino_acid, amino_acid):
    """
    Find single nucleotide substitutions that given a reference amino acid
    explains an observed amino acid.

    :arg dict back_table: Reverse translation table.
    :arg str reference_amino_acid: Original amino acid.
    :arg str amino_acid: Observed amino acid.

    :returns dict: Set of single nucleotide substitutions indexed by position.
    """
    substitutions = defaultdict(set)

    for codon in back_table[amino_acid]:
        for reference_codon in back_table[reference_amino_acid]:
            if hamming(codon, reference_codon) == 1:
                for position in range(3):
                    if codon[position] != reference_codon[position]:
                        substitutions[position].add(
                            (reference_codon[position], codon[position]))

    return substitutions


def subst_to_hgvs(substitutions, offset=0):
    """
    Translate a set of substitutions to HGVS.

    :arg dict substitutions: Set of single nucleotide substitutions indexed by
        position.
    :arg int offset: Codon position in the CDS.

    :returns set: Substitutions in HGVS format.
    """
    variants = set()

    for position in substitutions:
        for substitution in substitutions[position]:
            variants.add(Allele([DNAVar(
                start=position + offset + 1,
                end=position + offset + 1,
                sample_start=position + offset + 1,
                sample_end=position + offset + 1,
                type='subst',
                deleted=ISeqList([ISeq(sequence=substitution[0])]),
                inserted=ISeqList([ISeq(sequence=substitution[1])]))]))

    return variants


def improvable_substitutions(back_table):
    """
    Calculate all pairs of amino acid substututions that can be improved by
    looking at the underlying codon.

    :arg dict back_table: Reverse translation table.

    :returns list: List of improvable substitutions.
    """
    substitutions = set()

    for reference_amino_acid in back_table:
        for sample_amino_acid in back_table:
            substitutions_without_dna = one_subst_without_dna(
                back_table, reference_amino_acid, sample_amino_acid)
            for codon in back_table[reference_amino_acid]:
                substitutions_with_dna = one_subst(
                    back_table, codon, sample_amino_acid)
                if (substitutions_with_dna and not _compare_dict(
                        substitutions_without_dna, substitutions_with_dna) and
                        reference_amino_acid != sample_amino_acid):
                    substitutions.add(
                        (reference_amino_acid, sample_amino_acid))

    return substitutions


protein_letters_3to1 = _three_to_one()
