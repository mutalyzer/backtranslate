Usage
=====

Use the command ``backtranslate`` to find substitutions that explain an amino
acid change:

::

    $ backtranslate with_dna -o 210 data/mhv.fa - 1 Leu
    1       A       C
    1       A       T

If no reference is available, use the ``without_dna`` subcommand:

::

    $ backtranslate without_dna - Asp 92 Tyr
    274     G       T

The command ``find_stops`` finds a list of positions and substitutions that
lead to stop codons. This list of destructive substitutions are useful when
analysing a pool of viral transcripts. Counting the appropriate nucleotides at
the given positions gives insight into how many transcripts are active.

::

    $ backtranslate find_stops -o 210 data/mhv.fa -
    216     A       T
    225     A       T
    230     C       A
    230     C       G
    243     A       T
    ...
