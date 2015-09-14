from Bio.Data import IUPACData
from extractor.variant import Allele, DNAVar, ISeq, ISeqList


def _three_to_one():
    """
    The three letter to one letter table for amino acids including stop.

    :returns dict: Three letter to one letter amino acids table.
    """
    protein_letters_3to1 = dict(IUPACData.protein_letters_3to1_extended)
    protein_letters_3to1.update({'Ter': '*'})

    return protein_letters_3to1


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


protein_letters_3to1 = _three_to_one()
