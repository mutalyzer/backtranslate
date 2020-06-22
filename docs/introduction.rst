Introduction
============

Back translation or Reverse translation is the conversion of a protein sequence
into a nuclear sequence. In general, there are multiple nuclear sequences that
can be translated into the same protein sequence, so the reverse of this
operation usually results in a large number of candidate nuclear sequences.

A related problem is the back translation of an amino acid *change* to a
nuclear *change*. In this case, we know a reference amino acid and an observed
amino acid and we are interested in the nuclear variant that gave rise to this
change. Since there are infinitely many ways of making such a transformation,
we restrict ourselves to substitutions of one nucleotide that may explain the
observed amino acid change.

For example, we might be interested in which nucleotide substitutions will
transform a Tryptophan into a stop codon. It turns out that there are two
possible one nucleotide substitutions that have this effect; replace either
``G`` with an ``A``.

This form of back translation can be done by making use of reference
information. This information can be provided in the form of a reference amino
acid, or a reference codon. In general, using a reference codon will yield
fewer possibilities when compared to using a reference amino acid.

For example, there are five one nucleotide substitutions that can transform a
Leucine to a Phenylalanine. If we happen to know that the reference codon was
``CTT`` though, then there is only one substitution that can explain this
transformation.

This library provides functionality to back translate amino acid changes using
either a reference amino acid or a reference codon. Furthermore, it provides a
function that, given a codon table, will list all amino acid substitutions of
which the back translation can be improved by adding codon information.
