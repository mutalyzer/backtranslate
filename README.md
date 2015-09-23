# Back translation
This library provides functions for back translation from amino acids to
nucleotides.

    >>> from __future__ import unicode_literals
    >>>
    >>> from backtranslate.backtranslate import BackTranslate
    >>>
    >>> # Create a class instance, optionally giving the translation table id.
    >>> bt = BackTranslate()
    >>>
    >>> # Find all substitutions that transform the codon 'TTG' into a stop
    >>> # codon.
    >>> bt.with_dna('TGG', '*')
    {1: set([('G', 'A')]), 2: set([('G', 'A')])}


Sometimes we do not have access to the DNA sequence so we have to find
possible substitutions from the amino acids directly.

    >>> # Find all substitutions that transform a Tryptophan into a stop codon.
    >>> bt.without_dna('W', '*')
    {1: set([('G', 'A')]), 2: set([('G', 'A')])}

To find out which substitution predictions can be improved by adding codon
information, use the following function.

    >>> bt.improvable()
    set([('I', 'L'), ('R', 'W'), ('Q', 'H'), ('C', '*'), ('*', 'W'),
        ('K', 'N'), ('C', 'W'), ('S', 'R'), ('L', 'I'), ('*', 'S'), ('S', '*'),
        ('L', '*'), ('L', 'M'), ('L', 'F'), ('*', 'L'), ('D', 'E'), ('R', 'G'),
        ('S', 'C'), ('E', 'D'), ('R', 'S'), ('N', 'K'), ('H', 'Q'), ('S', 'T'),
        ('T', 'S'), ('G', 'R'), ('L', 'V'), ('I', 'M'), ('F', 'L'), ('*', 'Y'),
        ('Y', '*'), ('V', 'L'), ('R', '*')])

To get substitutions in a readable format, we can use the following:

    >>> from backtranslate.util import subst_to_cds
    >>>
    >>> substitutions = bt.without_dna('W', '*')
    >>>
    >>> # Transform the substitutions to CDS coordinates.
    >>> subst_to_cds(substitutions, 12)
    set([(15, 'G', 'A'), (14, 'G', 'A')])

## Command line interface
Use the command `backtranslate` to find substitutions that explain an amino
acid change:

    $ backtranslate with_dna -o 210 data/mhv.fa - 1 Leu
    1       A       C
    1       A       T


If no reference is available, use the `without_dna` subcommand:

    $ backtranslate without_dna - Asp 92 Tyr
    274     G       T


The command `find_stops` finds a list of positions and substitutions that lead
to stop codons. This list of destructive substitutions are useful when
analysing a pool of viral transcripts. Counting the appropriate nucleotides at
the given positions gives insight into how many transcripts are active.

    $ backtranslate find_stops -o 210 data/mhv.fa -
    216     A       T
    225     A       T
    230     C       A
    230     C       G
    243     A       T
    ...
