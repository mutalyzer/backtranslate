from argparse import FileType
from importlib.metadata import PackageNotFoundError, metadata
from os.path import exists
from re import split
from typing import Callable


class ProtectedFileType(FileType):
    def __call__(self, string):
        if 'w' in self._mode and exists(string):
            raise IOError('failed to create "{}": file exists.'.format(string))
        return super(ProtectedFileType, self).__call__(string)


def _extract(key: str, delim: str = r'[^\s\S]', index: int = 0) -> str:
    try:
        value = metadata(__package__).get(key, '')
    except PackageNotFoundError:
        return '<NO DATA>'
    return split(delim, value)[index]


def doc_split(func: Callable) -> str:
    return func.__doc__.split('\n\n')[0]


_project = _extract('Name')
_version = _extract('Version')
_author = _extract('Author-email', r'"', 1)
_email = _extract('Author-email', r'<|>', 1)
_description = _extract('Summary')
_url = _extract('Project-URL', r', ', 1)
_info = f'Homepage: {_url}'
_copyright = f'Copyright © {_author} {_email}'
