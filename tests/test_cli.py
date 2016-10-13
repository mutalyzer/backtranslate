"""
Tests for the backtranslate CLI.
"""
from __future__ import (
    absolute_import, division, print_function, unicode_literals)
from future.builtins import str, zip

import StringIO
import md5

from backtranslate import cli


def md5_check(data, md5sum):
    return md5.md5(data).hexdigest() == md5sum


class TestParser(object):
    """
    Test the backtranslate.backtranslate module.
    """
    def setup(self):
        self._input = open('data/mhv.fa')
        self._output = StringIO.StringIO()

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
            self._output.getvalue(), 'b3dbcc94594ab61e36dbb2256d4b4561')

    def test_find_stops_compact(self):
        cli.find_stops(self._input, self._output, 210, True)
        assert md5_check(
            self._output.getvalue(), '34aa553f2ea72ca992b2568a963c27ee')
