#!/usr/bin/env python


from __future__ import (
    absolute_import, division, print_function, unicode_literals)
from future.builtins import str, zip

import argparse
import re

from Bio import SeqIO

from . import usage, version, doc_split
from .backtranslate import BackTranslate
from .util import protein_letters_3to1, subst_to_cds


def with_dna(input_handle, output_handle, offset, position, amino_acid):
    """
    Get all variants that result in the observed amino acid change.

    :arg stream input_handle: Open readable handle to a FASTA file.
    :arg stream output_handle: Open writable handle to a file.
    :arg int offset: Position of the CDS start in the reference sequence.
    :arg int position: Position of the amino acid change (in p. coordinates).
    :arg str amino_acid: Observed amino acid.

    :returns set: Variants that lead to the observed amino acid change.
    """
    bt = BackTranslate()
    reference = str(SeqIO.parse(input_handle, 'fasta').next().seq)
    codon_pos = offset - 1 + (position - 1) * 3
    codon = reference[codon_pos:codon_pos + 3]
    substitutions = bt.with_dna(codon, protein_letters_3to1[amino_acid])

    for subst in subst_to_cds(substitutions, (position - 1) * 3):
        output_handle.write('{}\t{}\t{}\n'.format(*subst))


def without_dna(output_handle, position, reference_amino_acid, amino_acid):
    """
    Get all variants that result in the observed amino acid change without
    making use of the transcript.

    :arg stream output_handle: Open writable handle to a file.
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
        output_handle.write(
            'This substitution can be improved by using `with_dna`.\n')

    for subst in subst_to_cds(substitutions, (position - 1) * 3):
        output_handle.write('{}\t{}\t{}\n'.format(*subst))


def find_stops(input_handle, output_handle, offset):
    """
    Almost stop codon finder.

    :arg stream input_handle: Open readable handle to a FASTA file.
    :arg stream output_handle: Open writable handle to a file.
    :arg int offset: Position of the CDS start in the reference sequence.
    """
    bt = BackTranslate()
    sequence = str(SeqIO.parse(input_handle, 'fasta').next().seq)

    for index, codon in enumerate(re.findall('...', sequence[offset - 1:])):
        stop_positions = bt.with_dna(codon, '*')

        for position in stop_positions:
            for subst in stop_positions[position]:
                output_handle.write('{}\t{}\t{}\n'.format(
                    offset + (index * 3) + position, *subst))


def main():
    """
    Main entry point.
    """
    input_parser = argparse.ArgumentParser(add_help=False)
    input_parser.add_argument('input_handle', metavar='INPUT',
        type=argparse.FileType('r'), help='input file in FASTA format')
    input_parser.add_argument('-o', dest='offset', type=int, default=1,
        help='offset in the reference sequence (int default=%(default)s)')

    output_parser = argparse.ArgumentParser(add_help=False)
    output_parser.add_argument('output_handle', metavar='OUTPUT',
        type=argparse.FileType('w'), help='output file')

    reference_aa_parser = argparse.ArgumentParser(add_help=False)
    reference_aa_parser.add_argument(
        'reference_amino_acid', type=str, help='amino acid, e.g., Asp')

    observed_parser = argparse.ArgumentParser(add_help=False)
    observed_parser.add_argument(
        'position', type=int, help='position, e.g., 92')
    observed_parser.add_argument(
        'amino_acid', type=str, help='amino acid, e.g., Tyr')

    parser = argparse.ArgumentParser(
        description=usage[0], epilog=usage[1],
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-v', action='version', version=version(parser.prog))
    subparsers = parser.add_subparsers(dest='subcommand')

    parser_with_dna = subparsers.add_parser(
        'with_dna', parents=[input_parser, output_parser, observed_parser],
        description=doc_split(with_dna))
    parser_with_dna.set_defaults(func=with_dna)

    parser_without_dna = subparsers.add_parser(
        'without_dna',
        parents=[output_parser, reference_aa_parser, observed_parser],
        description=doc_split(without_dna))
    parser_without_dna.set_defaults(func=without_dna)

    parser_find_stops = subparsers.add_parser(
        'find_stops',
        parents=[input_parser, output_parser],
        description=doc_split(find_stops))
    parser_find_stops.set_defaults(func=find_stops)

    args = parser.parse_args()

    try:
        args.func(
            **dict((k, v) for k, v in vars(args).items() if k not in
            ('func', 'subcommand')))
    except IOError as error:
        parser.error(error)


if __name__ == '__main__':
    main()
