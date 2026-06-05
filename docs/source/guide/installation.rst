.. _guide_installation:

============
Installation
============

This guide covers different methods to install SDS-Tools and set up your
development environment.

Requirements
============

* **Python**: 3.10 or higher
* **pip**: Latest version recommended
* **Git**: For installing from source

Quick Installation
==================

For most users, installing from PyPI is the simplest method:

.. code-block:: bash

   pip install sds-tools

This will install the latest stable release of SDS-Tools and its dependencies.

Installing in a Virtual Environment
====================================

It's strongly recommended to install SDS-Tools in a virtual environment to
avoid conflicts with other Python packages.

Using venv (Standard Library)
------------------------------

Python's built-in ``venv`` module provides a simple way to create virtual environments:

**Create a virtual environment:**

.. code-block:: bash

   # Create a new virtual environment
   python -m venv sds-env

   # On Windows
   python -m venv sds-env

**Activate the environment:**

.. code-block:: bash

   # On Linux/macOS
   source sds-env/bin/activate

   # On Windows (Command Prompt)
   sds-env\Scripts\activate.bat

   # On Windows (PowerShell)
   sds-env\Scripts\Activate.ps1

**Install SDS-Tools:**

.. code-block:: bash

   pip install sds-tools

**Deactivate when done:**

.. code-block:: bash

   deactivate

Using virtualenv
----------------

``virtualenv`` is a third-party alternative with additional features:

**Install virtualenv:**

.. code-block:: bash

   pip install virtualenv

**Create and activate environment:**

.. code-block:: bash

   # Create environment
   virtualenv sds-env

   # Activate (Linux/macOS)
   source sds-env/bin/activate

   # Activate (Windows)
   sds-env\Scripts\activate

**Install SDS-Tools:**

.. code-block:: bash

   pip install sds-tools

Using uv (Recommended for Speed)
---------------------------------

``uv`` is a fast Python package installer and resolver written in Rust.
It's significantly faster than pip.

**Install uv:**

.. code-block:: bash

   # On Linux/macOS
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # On Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

   # Or using pip
   pip install uv

**Create a virtual environment with uv:**

.. code-block:: bash

   # Create environment
   uv venv sds-env

   # Activate (Linux/macOS)
   source sds-env/bin/activate

   # Activate (Windows)
   sds-env\Scripts\activate

**Install SDS-Tools with uv:**

.. code-block:: bash

   # Install SDS-Tools
   uv pip install sds-tools

   # Or directly with uv (faster)
   uv pip install sds-tools --resolution highest

**Why use uv?**

* ⚡ **10-100x faster** than pip
* 🔒 **Reliable dependency resolution**
* 💾 **Smart caching**
* 🎯 **Compatible with pip**

Installing from Source
======================

For Development or Latest Features
-----------------------------------

Clone the repository and install in editable mode:

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/skyfrigate/sds.git
   cd sds

   # Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install in editable mode
   pip install -e .

**With uv (faster):**

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/skyfrigate/sds.git
   cd sds

   # Create environment and install with uv
   uv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   uv pip install -e .

Installing Development Dependencies
------------------------------------

To contribute to SDS-Tools, install development dependencies:

**Using pip:**

.. code-block:: bash

   # Install with dev dependencies (if using optional-dependencies)
   pip install -e ".[dev]"

**Using uv with dependency groups (PEP 735):**

.. code-block:: bash

   # Install development tools
   uv pip install --group dev

   # Install documentation tools
   uv pip install --group docs

   # Or both
   uv pip install --group dev --group docs

This installs additional tools:

* **Testing**: pytest, pytest-cov
* **Linting**: black, isort, ruff, mypy
* **Security**: bandit
* **Build tools**: tox

Installing Documentation Dependencies
--------------------------------------

To build the documentation locally:

**Using pip:**

.. code-block:: bash

   pip install -e ".[docs]"

**Using uv:**

.. code-block:: bash

   uv pip install --group docs

Then build the documentation:

.. code-block:: bash

   cd docs
   make html

   # Open in browser (Linux/macOS)
   open build/html/index.html

   # Open in browser (Windows)
   start build/html/index.html

Verifying Installation
======================

Test Basic Import
-----------------

Verify that SDS-Tools is installed correctly:

.. code-block:: python

   import sds
   print(sds.__version__)  # Should print version number

Test with Examples
------------------

Try a simple example:

.. code-block:: python

   from sds.linear import LinkedList

   # Create a list
   lst = LinkedList()
   lst.append(1)
   lst.append(2)
   lst.append(3)

   # Print elements
   print(list(lst))  # [1, 2, 3]

   # Access by index
   print(lst[0])     # 1
   print(lst[-1])    # 3

Run Tests
---------

If you installed from source, run the test suite:

.. code-block:: bash

   # Install pytest if not already installed
   pip install pytest

   # Run tests
   pytest tests/

   # Run with coverage
   pytest --cov=sds tests/

Upgrading
=========

Upgrade to the Latest Version
------------------------------

.. code-block:: bash

   # Using pip
   pip install --upgrade sds-tools

   # Using uv
   uv pip install --upgrade sds-tools

Upgrade from Source
-------------------

.. code-block:: bash

   cd sds
   git pull origin main
   pip install -e .

Uninstallation
==============

Remove SDS-Tools
----------------

.. code-block:: bash

   # Using pip
   pip uninstall sds-tools

   # Using uv
   uv pip uninstall sds-tools

Remove Virtual Environment
---------------------------

Simply delete the environment directory:

.. code-block:: bash

   # Deactivate first
   deactivate

   # Remove directory
   rm -rf sds-env  # Linux/macOS
   rmdir /s sds-env  # Windows

Platform-Specific Notes
=======================

Windows
-------

**PowerShell Execution Policy:**

If you get an error activating the virtual environment in PowerShell:

.. code-block:: powershell

   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

**Long Path Support:**

Enable long path support in Windows if you encounter path length issues:

1. Open Registry Editor (regedit)
2. Navigate to ``HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem``
3. Set ``LongPathsEnabled`` to 1

macOS
-----

**Using Homebrew Python:**

If using Python from Homebrew:

.. code-block:: bash

   brew install python@3.10
   python3.10 -m venv sds-env

Linux
-----

**Install Python Development Headers:**

Some Linux distributions require development packages:

.. code-block:: bash

   # Debian/Ubuntu
   sudo apt-get install python3-dev python3-venv

   # Fedora/RHEL
   sudo dnf install python3-devel

   # Arch Linux
   sudo pacman -S python

Troubleshooting
===============

Import Errors
-------------

**Problem:** ``ModuleNotFoundError: No module named 'sds'``

**Solution:**

1. Ensure you're in the correct virtual environment
2. Verify installation: ``pip list | grep sds-tools``
3. Reinstall: ``pip install --force-reinstall sds-tools``

Permission Errors
-----------------

**Problem:** Permission denied during installation

**Solution:**

1. Use a virtual environment (recommended)
2. Or install for user only: ``pip install --user sds-tools``

SSL Certificate Errors
----------------------

**Problem:** SSL errors when installing

**Solution:**

.. code-block:: bash

   # Upgrade pip
   pip install --upgrade pip

   # Use trusted host (temporary solution)
   pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org sds-tools

Dependency Conflicts
--------------------

**Problem:** Conflicting dependencies

**Solution:**

1. Create a fresh virtual environment
2. Use ``uv`` for better dependency resolution
3. Check for conflicting packages: ``pip check``

Getting Help
============

If you encounter issues:

* **Documentation**: https://sds-tools.readthedocs.io
* **Issue Tracker**: https://github.com/skyfrigate/sds/issues
* **Discussions**: https://github.com/skyfrigate/sds/discussions

Next Steps
==========

Now that SDS-Tools is installed, continue with:

* :doc:`getting_started` - Learn the basics
* :doc:`linear_structures/index` - Explore linear data structures
* :ref:`api-reference` - Browse the API documentation

.. note::

   We recommend using ``uv`` for package management due to its speed and
   reliability. It's fully compatible with pip and significantly faster
   for large projects.