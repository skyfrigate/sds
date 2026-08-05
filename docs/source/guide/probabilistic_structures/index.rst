.. _guide_probabilistic:

===============================
Probabilistic Structures Guide
===============================

.. currentmodule:: sds.probabilistic

Introduction
============

A **probabilistic graphical model** represents a joint probability distribution
over a set of random variables as a graph: nodes are variables, and edges (or
cliques) encode direct probabilistic dependence. The graph structure is what
makes an otherwise intractable joint distribution over many variables
manageable — it factorizes into a product of small, local terms instead of one
enormous table.

.. mermaid::

   graph TD
       subgraph "Bayesian Network (directed)"
       A1((Cloudy)) --> B1((Sprinkler))
       A1 --> C1((Rain))
       B1 --> D1((WetGrass))
       C1 --> D1
       end

       style A1 fill:#3498db,color:#fff
       style D1 fill:#e74c3c,color:#fff

.. note::

   This guide focuses on *structure* — what the library represents and how to
   build it. It deliberately does not cover *inference* (computing marginal
   probabilities, the most likely explanation, ...): those algorithms belong
   to ``sds.algorithms`` and are not yet implemented. See
   :ref:`what-this-module-does-not-do` below.

Why Three Different Structures?
===================================

.. list-table:: When To Use Which
   :header-rows: 1
   :widths: 25 40 35

   * - Structure
     - Use when...
     - Example domain
   * - :class:`BayesianNetwork`
     - Dependencies have a natural direction (cause → effect,
       parent → child)
     - Medical diagnosis, genetics
   * - :class:`MarkovRandomField`
     - Dependencies are symmetric, or naturally form cycles
     - Image processing (pixel grids), spatial statistics
   * - :class:`HiddenMarkovModel`
     - Data unfolds over discrete time, with a hidden state driving
       observations
     - Speech recognition, part-of-speech tagging, weather modeling

.. mermaid::

   graph TD
       Q{What are you modeling?}
       Q -->|Directional dependency| BN[BayesianNetwork]
       Q -->|Symmetric / cyclic dependency| MRF[MarkovRandomField]
       Q -->|Sequence over time, hidden driver| HMM[HiddenMarkovModel]

       style BN fill:#3498db,color:#fff
       style MRF fill:#2ecc71,color:#fff
       style HMM fill:#9b59b6,color:#fff

The Two Building Blocks
===========================

Every structure in this module is built from the same two pieces:

* A :class:`~sds.probabilistic.variable.RandomVariable` — a named, discrete,
  finite-domain variable (e.g. ``RandomVariable("Rain", ("true", "false"))``).
* A :class:`~sds.probabilistic.factor.Factor` — a table mapping every joint
  state combination over a scope of variables to a non-negative number.

A conditional probability table (CPT), an unnormalized potential, and a
transition matrix are all, mechanically, the *same* :class:`Factor` type —
what differs is how each concrete structure validates and combines them.

.. _what-this-module-does-not-do:

What This Module Does *Not* Do
=====================================

No structure in ``sds.probabilistic`` performs inference. Concretely:

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - You can compute...
     - ...with this module
     - ...but NOT this (yet)
   * - The probability of one, fully known
       assignment
     - ``joint(assignment)`` — yes
     - —
   * - A marginal probability, summing over
       unobserved variables
     - —
     - Variable Elimination / Belief
       Propagation (``sds.algorithms``, planned)
   * - The most likely hidden sequence given
       observations
     - —
     - Viterbi (``sds.algorithms``, planned)
   * - The likelihood of an observation
       sequence, summing over every hidden
       path
     - —
     - The Forward algorithm (``sds.algorithms``,
       planned)

This is a deliberate design boundary (see :doc:`../../api/probabilistic/interfaces`):
structures and algorithms are kept strictly separate throughout this library.

Getting Started
==================

.. toctree::
   :maxdepth: 2

   bayesian_network
   markov_random_field
   hidden_markov_model

Comparing the Three Structures
====================================

.. list-table:: Structural Comparison
   :header-rows: 1
   :widths: 20 25 25 30

   * - Aspect
     - BayesianNetwork
     - MarkovRandomField
     - HiddenMarkovModel
   * - Topology
     - Directed, acyclic
     - Undirected, cycles OK
     - Fixed 2-variable chain
   * - Factor meaning
     - Normalized CPT
     - Unnormalized potential
     - Normalized CPT-shaped
   * - ``joint()`` result
     - True probability
     - Proportional to probability
     - True probability (of one sequence)
   * - Variable count
     - Open (any number)
     - Open (any number)
     - Exactly 2 (+ 1 derived)
   * - Composes
     - ``sds.graph.DirectedGraph``
     - ``sds.graph.Graph``
     - *(nothing — fixed shape)*

Real-World Application Domains
=====================================

Bayesian Networks
---------------------

- **Medical diagnosis**: symptoms conditioned on diseases
- **Genetics**: inheritance patterns (genotype → phenotype)
- **Spam filtering**: word occurrences conditioned on spam/ham
- **Risk assessment**: causal factors in finance, engineering

Markov Random Fields
-------------------------

- **Image segmentation**: pixel labels depend on neighboring pixels
- **Spatial statistics**: temperature/pollution readings across a region
- **Social network influence**: symmetric peer effects

Hidden Markov Models
-------------------------

- **Speech recognition**: phonemes (hidden) → acoustic signal (observed)
- **Part-of-speech tagging**: grammatical role (hidden) → word (observed)
- **Bioinformatics**: gene structure (hidden) → DNA sequence (observed)
- **Weather modeling**: weather regime (hidden) → sensor readings (observed)

References
============

* **[Koller2009]** Koller, D., Friedman, N. "Probabilistic Graphical Models:
  Principles and Techniques", MIT Press, 2009.
* **[Murphy2012]** Murphy, K. P. "Machine Learning: A Probabilistic
  Perspective", MIT Press, 2012.
* **[Rabiner1989]** Rabiner, L. R. "A tutorial on hidden Markov models and
  selected applications in speech recognition", Proceedings of the IEEE,
  77(2), 1989.

Open Educational Resources
==============================

* **[StanfordCS228]** Stanford University. "CS228: Probabilistic Graphical
  Models" — free, comprehensive lecture notes.
  https://ermongroup.github.io/cs228-notes/
* **[Eddy2004]** Eddy, S. R. "What is a hidden Markov model?", Nature
  Biotechnology 22, 1315-1316 (2004) — freely accessible two-page primer.
  https://doi.org/10.1038/nbt1004-1315

See Also
==========

* :doc:`../../api/probabilistic/index` — full API reference
* :doc:`../graph_structures/index` — graph structures, composed here for topology
* :doc:`../advanced_structures/index` — deterministic advanced structures (contrast)
