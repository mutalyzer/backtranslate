"""
Tests for the backtranslate CLI.
"""
from __future__ import (
    absolute_import, division, print_function, unicode_literals)
from future.builtins import str, zip

import sys

from hashlib import md5
from io import StringIO

from backtranslate import cli


def md5_check(data, md5sum):
    return md5(data).hexdigest() == md5sum


class TestParser(object):
    """
    Test the backtranslate.backtranslate module.
    """
    def setup(self):
        self._input = open('data/mhv.fa')
        self._output = StringIO()

    def test_with_dna(self):
        cli.with_dna(self._input, self._output, 210, 1, 'Leu')
        assert md5_check(
            self._output.getvalue(), 'efd57489b71583751f3a7efdd70df840')

    def test_without_dna(self):
        cli.without_dna(self._output, 92, 'Asp', 'Tyr')
        assert md5_check(
            self._output.getvalue(), '35e17a7e874f11abccb3bd3054c53993')

    def test_find_stops(self):
        cli.find_stops(self._input, self._output, 210, False)
        assert md5_check(
            self._output.getvalue(), '41c105e384651201970c0b2efd3afa3e')

    def test_find_stops_compact(self):
        cli.find_stops(self._input, self._output, 210, True)
        assert md5_check(
            self._output.getvalue(), '67c62854f4c0972e3fbf3dcec81b6a94')
