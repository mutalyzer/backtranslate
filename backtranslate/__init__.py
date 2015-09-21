"""
backtranslate: Functions for reverse translation.


Copyright (c) 2015 Leiden University Medical Center <humgen@lumc.nl>
Copyright (c) 2015 Jeroen F.J. Laros <j.f.j.laros@lumc.nl>

Licensed under the MIT license, see the LICENSE file.
"""


from __future__ import (
    absolute_import, division, print_function, unicode_literals)
from future.builtins import str, zip


__version_info__ = ('0', '0', '5')


__version__ = '.'.join(__version_info__)
__author__ = 'LUMC, Jeroen F.J. Laros'
__contact__ = 'J.F.J.Laros@lumc.nl'
__homepage__ = 'https://github.com/mutalyzer/backtranslate'


usage = __doc__.split("\n\n\n")


def doc_split(func):
    return func.__doc__.split("\n\n")[0]


def version(name):
    return "%s version %s\n\nAuthor   : %s <%s>\nHomepage : %s" % (name,
        __version__, __author__, __contact__, __homepage__)
