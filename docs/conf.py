import os
import sys
sys.path.insert(0, os.path.abspath('../'))
from PLASMAG import version

# Add path to the src directory
sys.path.insert(0, os.path.abspath('../src'))

project = 'PLASMAG'
copyright = '2024, Maxime RONCERAY, Claire REVILLET'
author = 'Maxime RONCERAY, Claire REVILLET'
release = version

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.autosectionlabel']
autoclass_content = 'class'

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
