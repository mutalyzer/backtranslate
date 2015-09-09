# Back translation
This library provides functions for back translation from amino acids to
nucleotides.

    from backtranslate.backtranslate import (
        reverse_translation_table, one_subst)

    # First create the reverse translation table for the organism of interest.
    back_table = reverse_translation_table(1)
    # Find all substitutions that transform the codon 'TTG' into a stop codon.
    substitutions = one_subst(back_table, 'TGG', '*')


Sometimes we do not have access to the DNA sequence so we have to find
possible substitutions from the amino acids directly.

    from backtranslate.backtranslate import (
        reverse_translation_table, one_subst_without_dna)

    # Find all substitutions that transform a Tryptophan into a stop codon.
    substitutions = one_subst_without_dna(back_table, 'W', '*')

To find out which substitution predictions can be improved by adding codon
information, use the following function.

    from backtranslate.backtranslate import improvable_substitutions

    improvable_substitutions(back_table)

To get substitutions in a readable format, we can use the following:

    from backtranslate.backtranslate import subst_to_var

    # Transform the substitutions to HGVS.
    variants = subst_to_var('TGG', substitutions, 12)
    # Print the variants in human readable format.
    print map(str, variants)

## Command line interface
Use the command `back_translate` to find substitutions that explain an amino
acid change:

    > back_translate NM_003002.2 92 Glu
    ['NM_003002.2:c.276C>A', 'NM_003002.2:c.276C>G']

When using a genomic reference sequence, make sure to mention the gene name and
the transcript variant:

    > back_translate 'AB026906.1(SDHD_v001)' 92 Tyr
    ['AB026906.1(SDHD_v001):c.274G>T']

## Potential stop codon finder
The command `find_stops` finds a list of positions and substitutions that lead
to stop codons. This list of destructive substitutions are useful when
analysing a pool of viral transcripts. Counting the appropriate nucleotides at
the given positions gives insight into how many transcripts are active.

    > find_stops -o 210 data/mhv.fa -
    (216, set(['T']))
    (225, set(['T']))
    (230, set(['A', 'G']))
    (243, set(['T']))
    ...
