.. _api_probabilistic:

============================================
Probabilistic Structures (sds.probabilistic)
============================================

.. currentmodule:: sds.probabilistic

Probabilistic graphical models represent probability distributions over discrete
random variables as a structure: a set of variables, and a set of factors (potential
functions) relating subsets of them. Unlike the deterministic structures in
:doc:`../advanced/index`, every operation here returns or manipulates a probability
(or a quantity proportional to one) rather than an exact value.

Overview
========

The module provides three families of structure:

* **Bayesian Networks** — directed, acyclic dependency graphs with locally
  normalized conditional probability tables (CPTs).
* **Markov Random Fields** — undirected dependency graphs (cycles allowed) with
  generally *unnormalized* potentials.
* **Hidden Markov Models** — a fixed states/observations chain with an initial
  distribution, a transition model and an emission model.

.. important::

   This module holds **no inference logic**. Computing a marginal probability by
   summing over hidden variables (Variable Elimination, Belief Propagation, the
   Forward algorithm), or finding the most likely explanation (Viterbi), is not
   implemented here — these are search/optimization algorithms and belong to
   ``sds.algorithms``, consistent with the library's strict separation between
   structures and algorithms. What *is* provided is the direct, O(n)-or-better
   product of stored factors for a **fully specified** assignment — see
   ``joint()`` on each structure.

Key Features
============

✓ **Two independent design families** — ``AbstractGraphicalModel`` (Bayesian
  Networks, Markov Random Fields) and ``AbstractHiddenMarkovModel`` (deliberately
  separate — see :doc:`interfaces`)

✓ **Composition over reimplementation** — ``BayesianNetwork`` and
  ``MarkovRandomField`` each delegate topology to :doc:`../graph/index`
  (``DirectedGraph`` / ``Graph``) rather than reimplementing adjacency

✓ **Fail-fast validation** — CPTs/potentials are checked at attach-time
  (normalization, scope correctness, clique membership for Markov random
  fields), never silently accepted

✓ **Pure Python** — no numeric dependency; probability tables are plain
  ``dict``-backed :doc:`factor` instances

Module Contents
================

Building Blocks
----------------

Shared by every structure in this module:

.. toctree::
   :maxdepth: 1

   variable
   factor

Abstract Interfaces
--------------------

.. toctree::
   :maxdepth: 1

   interfaces

Concrete Structures
---------------------

.. toctree::
   :maxdepth: 1

   bayesian_network
   markov_random_field
   hidden_markov_model

Structure Comparison
======================

.. list-table:: Probabilistic Structure Comparison
   :header-rows: 1
   :widths: 20 20 20 20 20

   * - Structure
     - Topology
     - Cycles
     - Factor semantics
     - Composes
   * - BayesianNetwork
     - Directed graph
     - Never (DAG)
     - Normalized CPT
     - ``sds.graph.DirectedGraph``
   * - MarkovRandomField
     - Undirected graph
     - Allowed
     - Unnormalized potential
     - ``sds.graph.Graph``
   * - HiddenMarkovModel
     - Fixed 2-variable chain
     - N/A (sequential)
     - Normalized CPT-shaped
     - *(none — fixed shape)*

Why Two Independent Design Families?
========================================

``BayesianNetwork`` and ``MarkovRandomField`` share :class:`AbstractGraphicalModel`:
both manage an *open* set of variables and factors, and both answer "what is the
potential of this full assignment?" the same way (multiply every stored factor).

``HiddenMarkovModel`` does not fit that shape. It has exactly two variables
(states, observations) and exactly three components (initial distribution,
transition model, emission model) — never more, never fewer. Forcing it under
:class:`AbstractGraphicalModel` would require degenerate implementations of
``add_variable()`` (there is no open variable set to add to) and a ``joint()``
signature that cannot represent a time sequence. See :doc:`interfaces` for the
full rationale — the same category of Liskov-substitution concern that already
justified keeping ``AbstractDirectedGraph`` separate from ``AbstractGraph`` in
:doc:`../graph/index`.

.. mermaid::

   classDiagram
       class Collection {
           <<abstract>>
       }
       class AbstractGraphicalModel {
           <<abstract>>
           +add_variable(variable)
           +add_factor(factor)
           +factors_for(variable)
           +joint(assignment)
       }
       class AbstractBayesianNetwork {
           <<abstract>>
           +add_edge(parent, child)
           +set_cpt(variable, factor)
       }
       class AbstractMarkovRandomField {
           <<abstract>>
           +add_edge(a, b)
       }
       class AbstractHiddenMarkovModel {
           <<abstract>>
           +set_states(variable)
           +set_transition_model(factor)
           +joint(states_seq, obs_seq)
       }

       Collection <|-- AbstractGraphicalModel
       AbstractGraphicalModel <|-- AbstractBayesianNetwork
       AbstractGraphicalModel <|-- AbstractMarkovRandomField
       Collection <|-- AbstractHiddenMarkovModel

       AbstractBayesianNetwork <|.. BayesianNetwork
       AbstractMarkovRandomField <|.. MarkovRandomField
       AbstractHiddenMarkovModel <|.. HiddenMarkovModel

       note for AbstractHiddenMarkovModel "Independent from\nAbstractGraphicalModel"

Quick Start
============

.. code-block:: python

   from sds.probabilistic import BayesianNetwork, Factor, RandomVariable

   rain = RandomVariable("Rain", ("true", "false"))
   sprinkler = RandomVariable("Sprinkler", ("true", "false"))

   bn = BayesianNetwork()
   bn.add_variable(rain)
   bn.add_variable(sprinkler)
   bn.add_edge(rain, sprinkler)

   bn.set_cpt(rain, Factor((rain,), {("true",): 0.2, ("false",): 0.8}))
   bn.set_cpt(sprinkler, Factor(
       (sprinkler, rain),
       {
           ("true", "true"): 0.01, ("false", "true"): 0.99,
           ("true", "false"): 0.4, ("false", "false"): 0.6,
       },
   ))

   bn.joint({rain: "true", sprinkler: "false"})  # 0.198

Related Modules
=================

* :doc:`../../guide/probabilistic_structures/index` — user guide for probabilistic structures
* :doc:`../graph/index` — graph structures, composed here for topology
* :doc:`../advanced/index` — deterministic advanced structures (contrast, see DD-011/DD-013)
* :doc:`../core/index` — core abstractions (``Collection``)

References
===========

* **[1]** Koller, D., Friedman, N. "Probabilistic Graphical Models: Principles and
   Techniques", MIT Press, 2009.
* **[2]** Murphy, K. P. "Machine Learning: A Probabilistic Perspective", MIT Press,
   2012, Chapter 10.
* **[3]** Rabiner, L. R. "A tutorial on hidden Markov models and selected
   applications in speech recognition", Proceedings of the IEEE, 77(2), 1989.

Open Educational Resources
============================

* **[StanfordCS228]** Stanford University. "CS228: Probabilistic Graphical Models"
   https://ermongroup.github.io/cs228-notes/

   Free, comprehensive lecture notes covering Bayesian networks, Markov
   random fields and inference.

* **[MITHMM]** Eddy, S. R. "What is a hidden Markov model?", Nature Biotechnology
   22, 1315-1316 (2004). https://doi.org/10.1038/nbt1004-1315

   Short, freely accessible introduction to HMMs with a bioinformatics angle.
