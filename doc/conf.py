# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
sys.path.insert(0, os.path.abspath('scr/sustainable_wage_tool_data'))

project = 'sustainable_wage_tool_data'
copyright = '2025, Higher Expectations'
author = 'Angel Febles'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

languages = ['en', 'es']
language = 'en'  # Default language

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode'
]

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

templates_path = ['templates']


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'groundwork'
html_static_path = ['_static']

locale_dirs = ['./locale/']   
gettext_compact = False     
