=======
License
=======

.. currentmodule:: sds

Overview
========

The SDS-Tools project uses a **dual licensing model** to distinguish between the code
implementation and its documentation:

* **Code**: Apache License 2.0
* **Documentation**: Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)

This dual approach allows us to:

* Keep the code permissive and reusable for all purposes
* Acknowledge the academic and open-access sources that inspired our documentation
* Ensure educational materials remain freely available while respecting attribution

.. mermaid::

   graph LR
       A[SDS-Tools Project] --> B[Source Code]
       A --> C[Documentation]

       B --> D[Apache 2.0<br/>✓ Commercial use<br/>✓ Modification<br/>✓ Distribution]
       C --> E[CC BY-NC 4.0<br/>✓ Educational use<br/>✓ Attribution required<br/>✗ Commercial use]

       style A fill:#e74c3c,color:#fff
       style B fill:#3498db,color:#fff
       style C fill:#2ecc71,color:#fff
       style D fill:#95a5a6,color:#fff
       style E fill:#f39c12,color:#fff

Source Code License (Apache 2.0)
=================================

The **source code** of SDS-Tools is licensed under the **Apache License, Version 2.0**.

Quick Summary
-------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Permission
     - Description
   * - ✓ **Commercial use**
     - You can use this software for commercial purposes
   * - ✓ **Modification**
     - You can modify the source code
   * - ✓ **Distribution**
     - You can distribute the original or modified code
   * - ✓ **Patent use**
     - Express grant of patent rights from contributors
   * - ✓ **Private use**
     - You can use and modify privately
   * - ⚠ **Trademark**
     - Does not grant rights to use trademarks
   * - ⚠ **Liability**
     - Includes limitation of liability
   * - ⚠ **Warranty**
     - Software is provided "as is"

Copyright Notice
----------------

.. code-block:: text

   Copyright 2019-2025, skyfrigate & biface

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       https://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

Full License Text
-----------------

The complete Apache 2.0 license is available at:

* Online: https://www.apache.org/licenses/LICENSE-2.0
* Repository: `LICENSE.md <https://github.com/skyfrigate/sds-tools/blob/master/LICENSE.md>`_

Documentation License (CC BY-NC 4.0)
====================================

The **documentation** (including guides, tutorials, examples, and mathematical descriptions)
is licensed under the **Creative Commons Attribution-NonCommercial 4.0 International License**.

.. image:: https://licensebuttons.net/l/by-nc/4.0/88x31.png
   :alt: CC BY-NC 4.0
   :target: https://creativecommons.org/licenses/by-nc/4.0/

Quick Summary
-------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Permission
     - Description
   * - ✓ **Share**
     - Copy and redistribute the material in any medium or format
   * - ✓ **Adapt**
     - Remix, transform, and build upon the material
   * - ✓ **Attribution**
     - You must give appropriate credit
   * - ✗ **Commercial use**
     - You may not use the material for commercial purposes
   * - ✓ **Educational use**
     - Free to use in educational and research contexts

.. note::

   This license applies to the **documentation content only**, not the source code.
   You are free to use the code (Apache 2.0) in commercial projects, but the
   documentation materials require attribution and cannot be used commercially.

You Are Free To
---------------

✓ **Share** — copy and redistribute the documentation in any medium or format

✓ **Adapt** — remix, transform, and build upon the documentation

✓ **Use for teaching** — use the documentation in educational settings

✓ **Use for research** — cite and reference the documentation in academic work

Under the Following Terms
--------------------------

**Attribution (BY)** — You must give appropriate credit, provide a link to the license,
and indicate if changes were made. You may do so in any reasonable manner, but not in
any way that suggests the licensor endorses you or your use.

**NonCommercial (NC)** — You may not use the documentation for commercial purposes.
This means you cannot:

* Sell the documentation or access to it
* Use it in paid training or courses
* Include it in commercial publications
* Use it for commercial consulting services

However, you CAN:

* Use it in free educational courses
* Reference it in academic papers
* Use it for personal learning
* Share it with students and colleagues

How to Attribute
----------------

When using or adapting this documentation, please provide attribution using one of
these formats:

**Academic Citation (APA Style)**:

.. code-block:: text

   SDS-Tools Documentation. (2025). Tree Structures Guide.
   Retrieved from https://sds-tools.readthedocs.io/
   Licensed under CC BY-NC 4.0.

**Inline Attribution**:

.. code-block:: text

   This material is adapted from the SDS-Tools Documentation
   (https://sds-tools.readthedocs.io/), licensed under CC BY-NC 4.0.

**Code Comment Attribution**:

.. code-block:: python

   # Mathematical model adapted from SDS-Tools Documentation
   # Source: https://sds-tools.readthedocs.io/
   # License: CC BY-NC 4.0

**Markdown Attribution**:

.. code-block:: markdown

   > Mathematical definitions and algorithms adapted from
   > [SDS-Tools Documentation](https://sds-tools.readthedocs.io/),
   > licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/).

Full License Text
-----------------

The complete CC BY-NC 4.0 license is available at:

* Online: https://creativecommons.org/licenses/by-nc/4.0/legalcode
* Summary: https://creativecommons.org/licenses/by-nc/4.0/

Rationale for Dual Licensing
=============================

Why Apache 2.0 for Code?
-------------------------

We chose the Apache License 2.0 for the source code because:

1. **Permissive**: Allows commercial and private use
2. **Patent protection**: Explicit grant of patent rights
3. **Compatibility**: Compatible with many other licenses (GPL, MIT, BSD)
4. **Industry standard**: Widely used and understood in the software industry
5. **Professional use**: Suitable for enterprise and commercial adoption

Why CC BY-NC 4.0 for Documentation?
------------------------------------

We chose CC BY-NC 4.0 for the documentation because:

1. **Academic respect**: Many of our sources are open-access academic materials
2. **Attribution requirement**: Ensures proper credit to original sources
3. **Educational focus**: Keeps educational materials freely available
4. **Non-commercial protection**: Prevents commercial exploitation of educational content
5. **Adaptation allowed**: Permits translation and adaptation for educational purposes

Acknowledgments
===============

This documentation draws inspiration from several open-access academic sources:

Educational Resources
---------------------

* **MIT OpenCourseWare** - Introduction to Algorithms (6.006)

  https://ocw.mit.edu/

* **OpenDSA** - Data Structures and Algorithms Modules

  https://opendsa-server.cs.vt.edu/

* **VisuAlgo** - Visualizing Data Structures and Algorithms

  https://visualgo.net/

* **Stanford CS Education Library** - Binary Trees and other structures

  http://cslibrary.stanford.edu/

* **USFCA Visualization** - David Galles' Algorithm Visualizations

  https://www.cs.usfca.edu/~galles/visualization/

Academic Papers (Open Access)
------------------------------

* Adelson-Velsky & Landis (1962) - AVL Trees
* Bayer & McCreight (1972) - B-Trees
* Guibas & Sedgewick (1978) - Red-Black Trees

See individual guide pages for complete citations and references.

Textbook References
-------------------

While we reference classic textbooks for completeness, our documentation is based
primarily on open-access materials. Cited textbooks include:

* Cormen et al., "Introduction to Algorithms" (CLRS)
* Knuth, "The Art of Computer Programming"
* Sedgewick & Wayne, "Algorithms"

These references are for completeness and further reading; they are not required
to understand or use this documentation.

Frequently Asked Questions
==========================

Can I use the code in my commercial product?
---------------------------------------------

**Yes!** The source code is licensed under Apache 2.0, which explicitly allows
commercial use. You can:

* Use it in commercial software
* Modify it for your needs
* Distribute it as part of your product

You must include the Apache 2.0 license notice, but you don't need to open-source
your modifications.

Can I use the documentation in my paid course?
-----------------------------------------------

**No.** The documentation is licensed under CC BY-NC 4.0, which prohibits commercial
use. However, you can:

* Reference and cite the documentation
* Use it as a recommended resource
* Adapt concepts for your own original materials (with attribution)

You cannot directly use or redistribute the documentation in a commercial context.

Can I translate the documentation?
-----------------------------------

**Yes!** Translation is considered an adaptation, which is allowed under CC BY-NC 4.0.
You must:

* Provide attribution to the original
* Indicate that you made changes (translation)
* Share your translation under the same CC BY-NC 4.0 license
* Not use the translation commercially

We welcome community translations and can help coordinate them.

Can I use code examples in my blog post?
-----------------------------------------

**Yes!** Code examples are part of the documentation, but since they demonstrate
the code (which is Apache 2.0), you can freely use them. Just provide appropriate
attribution and a link back to the documentation.

Can I fork the documentation on GitHub?
----------------------------------------

**Yes!** You can fork the documentation repository. GitHub forks are not considered
distribution, and they facilitate collaboration. However, any use of your fork must
still comply with CC BY-NC 4.0 terms.

Can I use the mathematical definitions in my research paper?
-------------------------------------------------------------

**Yes!** Academic research is not commercial use. You can:

* Cite the documentation as a reference
* Use the mathematical models (with citation)
* Adapt algorithms for your research (with attribution)

This is exactly the kind of use CC BY-NC 4.0 is designed to support.
