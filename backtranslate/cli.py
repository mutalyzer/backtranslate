#!/usr/bin/env python

import argparse

from suds.client import Client

from . import usage, version
from .backtranslate import (
    reverse_translation_table, protein_letters_3to1, one_subst, subst_to_var)


URL = 'https://mutalyzer.nl/services/?wsdl'


def possible_variants(reference, position, amino_acid):
    """
    Get all variants that result in the observed amino acid change.

    :arg str reference: Accession number.
    :arg int position: Position of the amino acid change (in p. coordinates).
    :arg str amino_acid: Observed amino acid.

    :returns set: Variants that lead to the observed amino acid change.
    """
    offset = (position - 1) * 3

    # Trick to get the reference sequence.
    service = Client(URL, cache=None).service
    cds = str(service.runMutalyzer('{}:c.1del'.format(reference)).origCDS)
    codon = cds[offset:offset + 3]

    back_table = reverse_translation_table(1)
    substitutions = one_subst(
        back_table, codon, protein_letters_3to1[amino_acid])

    return subst_to_var(codon, substitutions, offset)


def main():
    """
    Main entry point.
    """
    parser = argparse.ArgumentParser(description=usage[0], epilog=usage[1],
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('reference', type=str,
        help='accession number, e.g., AB026906.1(SDHD_i001)')
    parser.add_argument('position', type=int, help='position, e.g., 92')
    parser.add_argument('amino_acid', type=str, help='amino acid, e.g., Tyr')
    parser.add_argument('-v', action="version", version=version(parser.prog))

    try:
        args = parser.parse_args()
    except IOError as error:
        parser.error(error)

    print map(lambda x: '{}:c.{}'.format(args.reference, x), possible_variants(
        args.reference, args.position, args.amino_acid))


if __name__ == '__main__':
    main()
