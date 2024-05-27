import os
import sys
sys.path.insert(0, os.path.abspath('../'))

# Add path to the src directory
sys.path.insert(0, os.path.abspath('../src'))

project = 'PLASMAG'
copyright = '2024, Maxime RONCERAY'
author = 'Maxime RONCERAY'
release = 'v1.1.1'

extensions = ['sphinx.ext.autodoc']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'classic'
html_static_path = ['_static']
