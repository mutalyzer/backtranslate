Back translation
================

.. image:: https://img.shields.io/github/last-commit/mutalyzer/backtranslate.svg
   :target: https://github.com/mutalyzer/backtranslate/graphs/commit-activity
.. image:: https://travis-ci.org/mutalyzer/backtranslate.svg?branch=master
   :target: https://travis-ci.org/mutalyzer/backtranslate
.. image:: https://readthedocs.org/projects/mutalyzer-backtranslate/badge/?version=latest
   :target: https://mutalyzer-backtranslate.readthedocs.io/en/latest
.. image:: https://img.shields.io/github/release-date/mutalyzer/backtranslate.svg
   :target: https://github.com/mutalyzer/backtranslate/releases
.. image:: https://img.shields.io/github/release/mutalyzer/backtranslate.svg
   :target: https://github.com/mutalyzer/backtranslate/releases
.. image:: https://img.shields.io/pypi/v/mutalyzer-backtranslate.svg
   :target: https://pypi.org/project/mutalyzer-backtranslate/
.. image:: https://img.shields.io/github/languages/code-size/mutalyzer/backtranslate.svg
   :target: https://github.com/mutalyzer/backtranslate
.. image:: https://img.shields.io/github/languages/count/mutalyzer/backtranslate.svg
   :target: https://github.com/mutalyzer/backtranslate
.. image:: https://img.shields.io/github/languages/top/mutalyzer/backtranslate.svg
   :target: https://github.com/mutalyzer/backtranslate
.. image:: https://img.shields.io/github/license/mutalyzer/backtranslate.svg
   :target: https://raw.githubusercontent.com/mutalyzer/backtranslate/master/LICENSE.md

----

This library provides functions for back translation of amino acid changes to
nucleotide changes.

**Features:**

- Support for all known codon tables.
- Back translation of amino acid changes using codon reference information.
- Back translation of amino acid changes using amino acid reference
  information.
- Function to determine all amino acid substitutions of which the back
  translation can be improved by adding codon information.

Please see ReadTheDocs_ for the latest documentation.


Quick start
-----------

The ``BackTranslate`` class provides functionality for back translation.

.. code:: python

    >>> from mutalyzer_backtranslate import BackTranslate
    >>> bt = BackTranslate()

An amino acid change from a Leucine to a Phenylalanine can be explained by five
substitutions.

.. code:: python
    >>> bt.without_dna('L', 'F')
    {2: {('A', 'T'), ('A', 'C'), ('G', 'C'), ('G', 'T')}, 0: {('C', 'T')}}

If codon information is present, the same substitution can only be explained by
one substitution.

.. code:: python

    >>> bt.with_dna('CTT', 'F')
    {0: {('C', 'T')}}


.. _ReadTheDocs: https://mutalyzer-backtranslate.readthedocs.io
