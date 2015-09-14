#!/usr/bin/env python

import argparse

from suds.client import Client

from . import usage, version, doc_split
from .backtranslate import BackTranslate
from .util import protein_letters_3to1, subst_to_hgvs


URL = 'https://mutalyzer.nl/services/?wsdl'


def with_dna(reference, position, amino_acid):
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

    bt = BackTranslate()
    substitutions = bt.with_dna(codon, protein_letters_3to1[amino_acid])

    return subst_to_hgvs(substitutions, offset)


def without_dna(reference, position, reference_amino_acid, amino_acid):
    """
    Get all variants that result in the observed amino acid change without
    making use of the transcript.

    :arg str reference: Accession number.
    :arg int position: Position of the amino acid change (in p. coordinates).
    :arg str reference_amino_acid: Observed amino acid.
    :arg str amino_acid: Observed amino acid.

    :returns set: Variants that lead to the observed amino acid change.
    """
    bt = BackTranslate()
    improvable = bt.improvable()

    substitutions = bt.without_dna(
        protein_letters_3to1[reference_amino_acid],
        protein_letters_3to1[amino_acid])

    if (protein_letters_3to1[reference_amino_acid],
            protein_letters_3to1[amino_acid]) in improvable:
        print 'This substitution can be improved by using `with dna`.'

    return subst_to_hgvs(substitutions, (position - 1) * 3)


def main():
    """
    Main entry point.
    """
    input_parser = argparse.ArgumentParser(add_help=False)
    input_parser.add_argument(
        'reference', type=str,
        help='accession number, e.g., NM_003002.3')
    input_parser.add_argument('position', type=int, help='position, e.g., 92')

    reference_aa_parser = argparse.ArgumentParser(add_help=False)
    reference_aa_parser.add_argument(
        'reference_amino_acid', type=str, help='amino acid, e.g., Asp')

    observed_aa_parser = argparse.ArgumentParser(add_help=False)
    observed_aa_parser.add_argument(
        'amino_acid', type=str, help='amino acid, e.g., Tyr')

    parser = argparse.ArgumentParser(
        description=usage[0], epilog=usage[1],
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-v', action='version', version=version(parser.prog))
    subparsers = parser.add_subparsers(dest='subcommand')

    parser_with_dna = subparsers.add_parser(
        'with_dna', parents=[input_parser, observed_aa_parser],
        description=doc_split(with_dna))
    parser_with_dna.set_defaults(func=with_dna)

    parser_without_dna = subparsers.add_parser(
        'without_dna',
        parents=[input_parser, reference_aa_parser, observed_aa_parser],
        description=doc_split(without_dna))
    parser_without_dna.set_defaults(func=without_dna)

    args = parser.parse_args()

    try:
        print map(lambda x: '{}:c.{}'.format(args.reference, x), args.func(
            **dict((k, v) for k, v in vars(args).items() if k not in
            ('func', 'subcommand'))))
    except IOError as error:
        parser.error(error)


if __name__ == '__main__':
    main()
