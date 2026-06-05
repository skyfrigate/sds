# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "SDS Tools - Simple Data Structures Toolbox"
copyright = "2019-2024, skyfrigate & biface"
author = "skyfrigate & biface"

# The short X.Y version
version = "0.1"
# The full version, including alpha/beta/rc tags
release = "0.1.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# sys.path.append(os.path.abspath('..'))
# sys.path.append(os.path.abspath('../..'))
# sys.path.append(os.path.abspath('../../src'))
sys.path.insert(0, os.path.abspath("../../src"))

# -- General configuration ---------------------------------------------------

extensions = [
    # Sphinx core extensions
    "sphinx.ext.autodoc",  # Autodoc from docstring
    "sphinx.ext.napoleon",  # NumPy/Google docstrings format support
    "sphinx.ext.viewcode",  # Code block links
    "sphinx.ext.intersphinx",  # Links to other documentation
    "sphinx.ext.autosummary",  # Autosummary
    "sphinx.ext.todo",  # Notes TODO
    "sphinx.ext.coverage",  # Documentation coverage
    "sphinx.ext.githubpages",  # GitHub Pages support
    # Math support
    "sphinx.ext.mathjax",  # Mathematical formulas
    # External extensions
    "sphinxcontrib.mermaid",  # Mermaid draws
    # Additional extensions from your setup
    "sphinx_copybutton",  # Copy/Paste button
    "sphinx_tabs.tabs",  # Tabs support
    "sphinx_design",  # Design components
    "myst_parser",  # Markdown support
]


# Napoleon settings pour NumPy style
napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_type_aliases = None
napoleon_attr_annotations = True

# Autodoc settings
autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "exclude-members": "__weakref__",
}

# Don't show type hints in signatures (they're in the description)
autodoc_typehints = "description"
autodoc_typehints_description_target = "documented"

# Autosummary
autosummary_generate = True
autosummary_imported_members = True

# Templates path
templates_path = ["_templates"]
html_static_path = ["_static"]
html_css_files = ["css/enhanced.css"]

# Locale pour internationalisation
locale_dirs = ["locales/"]
gettext_compact = False
gettext_uuid = True

# Language
language = "en"  # Défaut anglais, peut être surchargé

# Source suffix
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",  # Si myst_parser est activé
}

# Master doc
master_doc = "index"

# Exclude patterns
exclude_patterns = [
    "_examples",  # Templates RST
    "_templates",  # Templates Jinja2
]

# Pygments style
pygments_style = "sphinx"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# -- Options for HTML output -------------------------------------------------
html_theme = "furo"

html_theme_options = {
    # Light / dark mode
    "light_css_variables": {
        "color-brand-primary": "#2980b9",
        "color-brand-content": "#2980b9",
    },
    "dark_css_variables": {
        "color-brand-primary": "5dade2",
        "color-brand-content": "#5dade2",
    },
    # Top-of-page buttons: valid values are "view" and/or "edit"
    "top_of_page_buttons": ["view", "edit"],
    # Footer icons (GitHub + GitLab)
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/skyfrigate/sds",
            "html": """
                <svg stroke="currentColor" fill="currentColor" stroke-width="0"
                    viewBox="0 0 16 16" height="1em" width="1em"
                    xmlns="http://www.w3.org/2000/svg">
                    <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54
                    2.29 6.53 5.47 7.59.4.07.55-.17.55-.38
                    0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01
                    1.08.58 1.23.82.72 1.21 1.87.87
                    2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95
                    0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0
                    .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09
                    2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08
                    2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65
                    3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01
                    2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z">
                    </path>
                </svg>
            """,
            "class": "",
        },
    ],
    # Navigation
    "navigation_with_keys": True,
}

# Logo et favicon
html_logo = '_static/images/logo.svg'
html_favicon = '_static/images/logo.svg'

# Sidebar
#html_sidebars = {
#    "**": [
#        "globaltoc.html",
#        "relations.html",
#        "sourcelink.html",
#        "searchbox.html",
#    ]
#}

# -- Options for LaTeX output ------------------------------------------------
latex_engine = 'pdflatex'  # ou 'xelatex' pour un meilleur support Unicode

latex_elements = {
    'papersize': 'a4paper',
    'pointsize': '10pt',
    
    # Packages LaTeX additionnels
    'preamble': r'''
        \usepackage{charter}
        \usepackage[defaultsans]{lato}
        \usepackage{inconsolata}
        \usepackage{fancyhdr}
        \pagestyle{fancy}
        \fancyhf{}
        \fancyhead[LE,RO]{\thepage}
        \fancyhead[RE]{\textit{\nouppercase{\leftmark}}}
        \fancyhead[LO]{\textit{\nouppercase{\rightmark}}}
        \renewcommand{\headrulewidth}{0.4pt}
        \renewcommand{\footrulewidth}{0pt}
        \setcounter{tocdepth}{2}
        \setcounter{secnumdepth}{3}
    ''',
    
    # Marges
    'sphinxsetup': '''
        verbatimwithframe=true,
        VerbatimColor={RGB}{242,242,242},
        verbatimhintsturnover=false,
        hmargin={1.5cm,1.5cm},
        vmargin={2cm,2cm},
    ''',
    
    # Page de titre personnalisée
    'maketitle': r'''
        \begin{titlepage}
        \centering
        \vspace*{2cm}
        {\Huge\bfseries ''' + project + r'''\par}
        \vspace{1cm}
        {\Large Documentation Technique\par}
        \vspace{2cm}
        {\large Version ''' + release + r'''\par}
        \vspace{1cm}
        {\large\itshape ''' + author + r'''\par}
        \vfill
        {\large \today\par}
        \end{titlepage}
    ''',
    
    # Position des figures
    'figure_align': 'htbp',
    
    # Table des matières
    'tableofcontents': r'\tableofcontents\clearpage',
}

# Grouping the document tree into LaTeX files
latex_documents = [
    (
        master_doc,
        'SDS-Tools.tex',
        'SDS-Tools Documentation',
        'skyfrigate \\& biface',
        'manual',
    ),
]

# Configuration LaTeX supplémentaire
latex_logo = None  # '_static/images/logo.png' si vous avez un logo
latex_use_parts = False
latex_show_pagerefs = True
latex_show_urls = 'footnote'
latex_domain_indices = True

# -- Options for EPUB output -------------------------------------------------
epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright
epub_exclude_files = ['search.html']
epub_tocdepth = 3
epub_tocdup = True
epub_show_urls = 'inline'
epub_use_index = True

# -- Options pour Intersphinx ------------------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
}

# -- MathJax configuration ---------------------------------------------------

mathjax_path = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"

mathjax3_config = {
    "tex": {
        "inlineMath": [["$", "$"], ["\\(", "\\)"]],
        "displayMath": [["$$", "$$"], ["\\[", "\\]"]],
    },
    "chtml": {
        "displayAlign": "left",
        "displayIndent": "2em"
    }
}

# -- Mermaid configuration ---------------------------------------------------

mermaid_output_format = "raw"
mermaid_params = [
    "--theme",
    "default",
    "--width",
    "800",
    "--backgroundColor",
    "transparent",
]
mermaid_version = "11.12.1"
mermaid_init_js = ""

# -- MyST Parser configuration (Markdown support) ----------------------------

myst_enable_extensions = [
    "colon_fence",  # ::: pour les directives
    "deflist",  # Listes de définitions
    "substitution",  # Substitutions de variables
    "tasklist",  # Listes de tâches
]

# -- Todo extension configuration --------------------------------------------

todo_include_todos = True

# -- Additional settings -----------------------------------------------------

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_emit_warnings = True

# If true, keep warnings as "system message" paragraphs in the built documents.
keep_warnings = False