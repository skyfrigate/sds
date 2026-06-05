============
Contributing
============

Thank you for your interest in contributing to SDS-Tools!

How to Contribute
=================

Reporting Bugs
--------------

* Check if the bug has already been reported in the issue tracker
* Include Python version, OS, and SDS-Tools version
* Provide a minimal reproducible example
* Describe expected vs actual behavior

Suggesting Enhancements
-----------------------

* Check if the feature has already been suggested
* Explain the use case and benefits
* Provide examples of how it would be used

Code Contributions
------------------

1. Fork the repository
2. Create a feature branch
3. Write tests for new functionality
4. Ensure all tests pass
5. Update documentation
6. Submit a pull request

Development Setup
=================

.. code-block:: bash

   # Clone repository
   git clone https://github.com/yourusername/sds-tools.git
   cd sds-tools

   # Install in development mode
   pip install -e ".[dev]"

   # Run tests
   pytest

   # Check coverage
   pytest --cov=sds

   # Build documentation
   cd docs
   make html

Code Style
==========

* Follow PEP 8
* Use Black for formatting
* Use type hints
* Write NumPy-style docstrings
* Maximum line length: 100 characters

Testing Requirements
====================

* Write tests for all new functionality
* Maintain >90% code coverage
* Include edge cases and error conditions
* Use descriptive test names

Documentation Requirements
==========================

* Update API documentation
* Add usage examples
* Update user guide if adding new structures
* Include complexity analysis

Review Process
==============

All contributions will be reviewed for:

* Code quality and style
* Test coverage
* Documentation completeness
* Performance implications
* API consistency

License
=======

By contributing, you agree that your contributions will be licensed
under the same license as the project.