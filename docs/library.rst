Library
=======

The library provides functions for back translation from amino acids to
nucleotides.

.. code:: python

    >>> from mutalyzer_backtranslate import BackTranslate
    >>>
    >>> # Create a class instance, optionally giving the translation table id.
    >>> bt = BackTranslate()
    >>>
    >>> # Find all substitutions that transform the codon 'TGG' into a stop codon.
    >>> bt.with_dna('TGG', '*')
    {1: {('G', 'A')}, 2: {('G', 'A')}}

Sometimes we do not have access to the DNA sequence so we have to find possible
substitutions from the amino acids directly.

.. code:: python

    >>> # Find all substitutions that transform a Tryptophan into a stop codon.
    >>> bt.without_dna('W', '*')
    {1: {('G', 'A')}, 2: {('G', 'A')}}

To find out which substitution predictions can be improved by adding codon
information, use the following function.

.. code:: python

    >>> bt.improvable()
    {('N', 'K'), ('R', 'W'), ('L', 'F'), ('D', 'E'), ('E', 'D'), ('C', 'W'),
     ('K', 'N'), ('Q', 'H'), ('C', '*'), ('I', 'L'), ('G', 'R'), ('F', 'L'),
     ('S', '*'), ('T', 'S'), ('*', 'S'), ('S', 'R'), ('R', 'S'), ('V', 'L'),
     ('R', 'G'), ('Y', '*'), ('S', 'T'), ('*', 'L'), ('*', 'W'), ('H', 'Q'),
     ('L', 'I'), ('I', 'M'), ('L', 'V'), ('L', 'M'), ('L', '*'), ('R', '*'),
     ('S', 'C'), ('*', 'Y')}

To get substitutions in a readable format, we can use the following:

.. code:: python

    >>> from mutalyzer_backtranslate.util import subst_to_cds
    >>>
    >>> substitutions = bt.without_dna('W', '*')
    >>>
    >>> # Transform the substitutions to CDS coordinates.
    >>> subst_to_cds(substitutions, 12)
    {(14, 'G', 'A'), (15, 'G', 'A')}
