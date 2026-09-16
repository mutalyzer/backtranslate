from mutalyzer_backtranslate import _authors, _project, _version, _info


author = _authors
project = _project
release = _version
info = _info

autoclass_content = 'both'
extensions = ['sphinx.ext.autodoc', 'sphinx_autodoc_typehints', 'sphinxarg.ext']
master_doc = 'index'
