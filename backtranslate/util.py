from __future__ import unicode_literals

from Bio.Data import IUPACData


def _three_to_one():
    """
    The three letter to one letter table for amino acids including stop.

    :returns dict: Three letter to one letter amino acids table.
    """
    return dict(map(lambda x: (unicode(x[0]), unicode(x[1])),
        IUPACData.protein_letters_3to1_extended.items()) + [('Ter', '*')])


def subst_to_cds(substitutions, offset):
    """
    Convert a set of substitutions to CDS coordinates.

    :arg dict substitutions: Set of single nucleotide substitutions indexed by
        position.
    :arg int offset: Codon position in the CDS.

    :returns set: Substitutions in CDS coordinates.
    """
    variants = set()

    for position in substitutions:
        for substitution in substitutions[position]:
            variants.add(
                (position + offset + 1, substitution[0], substitution[1]))

    return variants


protein_letters = IUPACData.protein_letters + '*'
protein_letters_3to1 = _three_to_one()
