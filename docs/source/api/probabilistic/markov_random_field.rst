.. _api_probabilistic_markov_random_field:

=========================
MarkovRandomField Class
=========================

.. currentmodule:: sds.probabilistic.markov_random_field

Overview
========

:class:`MarkovRandomField` is a concrete
:class:`~sds.probabilistic.interfaces.AbstractMarkovRandomField`. It composes a
``sds.graph.Graph`` internally to carry undirected dependency edges, mirroring
:class:`~sds.probabilistic.bayesian_network.BayesianNetwork`'s approach with
``DirectedGraph``.

Mathematical Foundation
=========================

A Markov random field factorizes an (unnormalized) joint distribution over its
graph's maximal cliques:

.. math::

   P(X_1, \ldots, X_n) = \frac{1}{Z} \prod_{c \in \mathcal{C}} \phi_c(\mathbf{X}_c)

where :math:`\mathcal{C}` is the set of cliques the model's factors are
attached over, :math:`\phi_c` is the potential for clique :math:`c`, and

.. math::

   Z = \sum_{\mathbf{x}} \prod_{c \in \mathcal{C}} \phi_c(\mathbf{x}_c)

is the **partition function** — a normalizing constant summed over every
possible joint assignment. Computing :math:`Z` is an inference problem
(exponential in general), deliberately left to ``sds.algorithms``:
``joint()`` on this class returns :math:`\prod_c \phi_c(\mathbf{x}_c)`, which
is only *proportional* to the true probability.

.. mermaid::

   graph LR
       A((A)) --- B((B))
       B --- C((C))
       C --- A

       style A fill:#2ecc71,color:#fff
       style B fill:#2ecc71,color:#fff
       style C fill:#2ecc71,color:#fff

   %% Unlike a Bayesian network, this 3-cycle is a perfectly valid
   %% Markov random field topology.

Detailed Documentation
========================

.. autoclass:: MarkovRandomField
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __repr__

Design Notes
==============

Cycles Are Permitted
------------------------

Unlike :class:`~sds.probabilistic.bayesian_network.BayesianNetwork`, there is
no acyclicity check — ``Graph`` is undirected, and cycles are a normal,
expected part of Markov random field topology (e.g. a grid, or any model with
mutual dependencies).

Clique Validation on ``add_factor``
------------------------------------------

Per the Hammersley-Clifford correspondence, a factor's scope is expected to
form a **clique** of the underlying graph: every pair of variables in the
scope must be connected by an edge. ``add_factor()`` enforces this fail-fast,
checking every pair:

.. code-block:: python

   from sds.probabilistic import Factor, MarkovRandomField, RandomVariable

   a = RandomVariable("A", ("0", "1"))
   b = RandomVariable("B", ("0", "1"))

   mrf = MarkovRandomField()
   mrf.add_variable(a)
   mrf.add_variable(b)
   # No edge added between a and b yet.

   potential = Factor((a, b), {("0", "0"): 1.0, ("0", "1"): 1.0,
                                ("1", "0"): 1.0, ("1", "1"): 1.0})
   mrf.add_factor(potential)  # ValueError: not a clique

A single-variable factor needs no edge at all — there is no pair to check.

No Completeness Requirement on ``joint()``
------------------------------------------------

Unlike :class:`~sds.probabilistic.bayesian_network.BayesianNetwork`,
``joint()`` does **not** require every variable to have an attached factor: an
unnormalized potential over a subset of variables is still well-defined even
if some registered variables are unconstrained by any factor. With zero
factors attached, ``joint()`` returns ``1.0`` (the empty product).

Usage Examples
================

A Simple Pairwise Potential
---------------------------------

.. code-block:: python

   from sds.probabilistic import Factor, MarkovRandomField, RandomVariable

   rain = RandomVariable("Rain", ("true", "false"))
   sprinkler = RandomVariable("Sprinkler", ("true", "false"))

   mrf = MarkovRandomField()
   mrf.add_variable(rain)
   mrf.add_variable(sprinkler)
   mrf.add_edge(rain, sprinkler)

   mrf.add_factor(Factor(
       (rain, sprinkler),
       {
           ("true", "true"): 0.01, ("true", "false"): 0.99,
           ("false", "true"): 0.4, ("false", "false"): 0.6,
       },
   ))

   mrf.joint({rain: "true", sprinkler: "false"})  # 0.99 (unnormalized)

A Triangle Clique (Cycle Allowed)
---------------------------------------

.. code-block:: python

   cloudy = RandomVariable("Cloudy", ("true", "false"))

   mrf.add_variable(cloudy)
   mrf.add_edge(sprinkler, cloudy)
   mrf.add_edge(cloudy, rain)  # closes the triangle -- no error

   # A 3-variable potential is now valid, since {rain, sprinkler, cloudy}
   # forms a complete triangle in the graph.

Complexity
============

.. list-table::
   :header-rows: 1
   :widths: 35 20 45

   * - Operation
     - Complexity
     - Notes
   * - ``add_variable``
     - O(1)
     - amortized dict insertion
   * - ``add_edge``
     - O(1)
     - no acyclicity check (cycles allowed)
   * - ``add_factor``
     - :math:`O(k^2)`
     - k = scope size, pairwise clique check via ``Graph.has_edge``
   * - ``neighbors``
     - O(deg)
     - delegates to ``Graph``
   * - ``joint``
     - O(number of factors)
     - one ``Factor.value`` lookup per stored potential
   * - ``factors_for``
     - O(number of factors × scope size)
     - linear scan of stored potentials

Best Practices
================

✅ **Add all edges before attaching factors over multi-variable cliques**

.. code-block:: python

   # Good: the clique exists in the graph before the factor references it
   mrf.add_edge(a, b); mrf.add_edge(b, c); mrf.add_edge(c, a)
   mrf.add_factor(Factor((a, b, c), table))  # valid: full triangle

✗ **Don't expect ``joint()`` to return a true probability**

.. code-block:: python

   # This is proportional to P(x), not equal to it -- there is no
   # partition function Z applied here (see Mathematical Foundation above)
   unnormalized = mrf.joint(assignment)

See Also
==========

* :doc:`interfaces` — the ``AbstractMarkovRandomField`` contract
* :doc:`bayesian_network` — the directed counterpart
* :doc:`../graph/graph` — ``Graph``, composed here for topology
* :doc:`../../guide/probabilistic_structures/markov_random_field` — user guide

References
============

* **[1]** Koller, D., Friedman, N. "Probabilistic Graphical Models", MIT Press,
   2009, Chapter 4 (Undirected Graphical Models).
* **[2]** Hammersley, J. M., Clifford, P. "Markov fields on finite graphs and
   lattices" (unpublished manuscript, 1971) — the theorem connecting graph
   cliques to factorization.

Open Educational Resources
============================

* **[StanfordCS228MRF]** Stanford University. "CS228 Notes: Markov random fields"
   https://ermongroup.github.io/cs228-notes/representation/undirected/
