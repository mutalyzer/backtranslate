# Back translation
This library provides functions for back translation from amino acids to
nucleotides.

    from __future__ import unicode_literals

    from backtranslate.backtranslate import BackTranslate

    # Create a class instance, optionally giving the translation table id.
    bt = BackTranslate()
    # Find all substitutions that transform the codon 'TTG' into a stop codon.
    substitutions = bt.with_dna('TGG', '*')


Sometimes we do not have access to the DNA sequence so we have to find
possible substitutions from the amino acids directly.

    # Find all substitutions that transform a Tryptophan into a stop codon.
    substitutions = bt.without_dna('W', '*')

To find out which substitution predictions can be improved by adding codon
information, use the following function.

    bt.improvable()

To get substitutions in a readable format, we can use the following:

    from backtranslate.util import subst_to_cds

    # Transform the substitutions to CDS coordinates.
    variants = subst_to_cds(substitutions, 12)

## Command line interface
Use the command `back_translate` to find substitutions that explain an amino
acid change:

    $ back_translate with_dna -o 210 data/mhv.fa - 1 Leu
    1       A       C
    1       A       T


If no reference is available, use the `without_dna` subcommand:

    $ back_translate without_dna - Asp 92 Tyr
    274     G       T


The command `find_stops` finds a list of positions and substitutions that lead
to stop codons. This list of destructive substitutions are useful when
analysing a pool of viral transcripts. Counting the appropriate nucleotides at
the given positions gives insight into how many transcripts are active.

    $ back_translate find_stops -o 210 data/mhv.fa -
    216     A       T
    225     A       T
    230     C       A
    230     C       G
    243     A       T
    ...
