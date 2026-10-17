from importlib.metadata import PackageNotFoundError, metadata
from re import split
from typing import Callable

from .backtranslate import BackTranslate


def _extract(key: str, delim: str = r'[^\s\S]', index: int = 0) -> str:
    try:
        value = metadata(__package__).get(key, '')
    except PackageNotFoundError:
        return '<NO DATA>'
    return split(delim, value)[index]


def doc_split(func: Callable) -> str:
    return func.__doc__.split('\n\n')[0]


_email = _extract('Author-email', r'<|>', 1)
_url = _extract('Project-URL', r', ', 1)
_year = '2015-2026'

project = _extract('Name')
release = _extract('Version')
author = _extract('Author-email', r'"', 1)
description = _extract('Summary')
copyright = f'{_year} by {author} <{_email}>'
info = f'''{project} version {release}

Copyright (c) {copyright}
Homepage: {_url}'''
