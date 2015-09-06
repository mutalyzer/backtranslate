#!/usr/bin/env python

"""
"""


from collections import defaultdict

from Bio.Data import CodonTable, IUPACData
from extractor.variant import Allele, DNAVar, ISeq, ISeqList
from Levenshtein import hamming


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


def three_to_one():
    """
    The three letter to one letter table for amino acids including stop.

    :returns dict: Three letter to one letter amino acids table.
    """
    protein_letters_3to1 = dict(IUPACData.protein_letters_3to1_extended)
    protein_letters_3to1.update({'Ter': '*'})

    return protein_letters_3to1


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
                    substitutions[position].add(codon[position])

    return substitutions


def subst_to_var(reference_codon, substitutions, offset=1):
    """
    Translate a set of substitutions to HGVS.

    :arg str reference_codon: Original codon.
    :arg dict substitutions: Set of single nucleotide substitutions indexed by
        position.
    :arg int offset: Codon position in the CDS.

    :returns set: Substitutions in HGVS format.
    """
    variants = set()

    for position in substitutions:
        for substitution in substitutions[position]:
            variants.add(Allele([DNAVar(
                start=position + offset, end=position + offset,
                sample_start=position + offset, sample_end=position + offset,
                type='subst',
                deleted=ISeqList([ISeq(sequence=reference_codon[position])]),
                inserted=ISeqList([ISeq(sequence=substitution)]))]))

    return variants
