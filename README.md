# Back translation
This library provides functions for back translation from amino acids to
nucleotides.

    from backtranslate import backtranslate

    # First create the reverse translation table for the organism of interest.
    back_table = backtranslate.reverse_translation_table()
    # Find all substitutions that transform the codon 'TTG' into a stop codon.
    substitutions = backtranslate.one_subst(back_table, 'TGG', '*')


Sometimes we do not have access to the DNA sequence so we have to find
possible substitutions from the amino acids directly.

    # Find all substitutions that transform a Tryptophan into a stop codon.
    substitutions = backtranslate.one_subst_without_dna(back_table, 'W', '*')

To find out which substitution predictions can be improved by adding codon
information, use the following function.

    backtranslate.improvable_substitutions(back_table)

To get substitutions in a readable format, we can use the following:

    # Transform the substitutions to HGVS.
    variants = backtranslate.subst_to_hgvs(substitutions, 12)
    # Print the variants in human readable format.
    print map(str, variants)

## Command line interface
Use the command `back_translate` to find substitutions that explain an amino
acid change:

    $ back_translate with_dna NM_003002.2 69 Asp
    ['NM_003002.2:c.207G>T', 'NM_003002.2:c.207G>C']

When using a genomic reference sequence, make sure to mention the gene name and
the transcript variant:

    $ back_translate with_dna 'AB026906.1(SDHD_v001)' 92 Tyr
    ['AB026906.1(SDHD_v001):c.274G>T']

If no reference is available, use the `without_dna` subcommand:

    $ back_translate without_dna NM_003002.2 66 Trp Ter
    ['NM_003002.2:c.197G>A', 'NM_003002.2:c.198G>A']


## Potential stop codon finder
The command `find_stops` finds a list of positions and substitutions that lead
to stop codons. This list of destructive substitutions are useful when
analysing a pool of viral transcripts. Counting the appropriate nucleotides at
the given positions gives insight into how many transcripts are active.

    $ find_stops -o 210 data/mhv.fa -
    (216, set([('A', 'T')]))
    (225, set([('A', 'T')]))
    (230, set([('C', 'A'), ('C', 'G')]))
    (243, set([('A', 'T')]))
    ...
