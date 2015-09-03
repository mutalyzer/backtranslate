#!/usr/bin/env python

"""
Almost stop codon finder.


(C) 2015 Jeroen F.J. Laros <J.F.J.Laros@lumc.nl>
"""

import argparse

import Levenshtein
from Bio import SeqIO
from Bio.Data import CodonTable


def one_stop_mutations(codon):
    """
    """
    positions = set()

    for stop_codon in CodonTable.unambiguous_dna_by_id[1].stop_codons:
        if Levenshtein.hamming(codon, stop_codon) == 1:
            for i in range(3):
                if codon[i] != stop_codon[i]:
                    positions.add(i)
    return positions


def find_positions(sequence, offset):
    """
    """
    result = []

    for i in range(offset, len(sequence) - ((len(sequence) - offset) % 3), 3):
        stop_positions = one_stop_mutations(sequence[i:i + 3])

        for position in stop_positions:
            result.append(i + position + 1)

    return result


def stop(input_handle, output_handle, offset):
    """
    """
    sequence = str(SeqIO.parse(input_handle, 'fasta').next().seq)

    for i in find_positions(sequence, offset):
        output_handle.write('{}\n'.format(i))


def main():
    usage = __doc__.split('\n\n\n')
    parser = argparse.ArgumentParser(description=usage[0], epilog=usage[1],
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('input_handle', type=argparse.FileType('r'),
        help='input file in FASTA format')
    parser.add_argument('output_handle', type=argparse.FileType('w'),
        help='output file')
    parser.add_argument('-o', dest='offset', type=int, default=0,
        help='offset in the reference sequence (int default=%(default)s)')

    try:
        args = parser.parse_args()
    except IOError as error:
        parser.error(error)

    stop(args.input_handle, args.output_handle, args.offset - 1)


if __name__ == '__main__':
    main()
