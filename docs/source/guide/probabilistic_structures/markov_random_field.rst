.. _guide_probabilistic_markov_random_field:

============================
Markov Random Field Guide
============================

.. currentmodule:: sds.probabilistic

Introduction
============

A **Markov random field** (MRF) represents a joint probability distribution as
an *undirected* graph: nodes are variables, edges represent symmetric
dependence, and potentials (unnormalized, non-negative functions) are attached
over the graph's cliques. Unlike a Bayesian network, there is no notion of
"cause" and "effect" — and cycles are perfectly normal.

.. mermaid::

   graph LR
       A((A)) --- B((B))
       B --- C((C))
       C --- D((D))
       D --- A

       style A fill:#2ecc71,color:#fff
       style B fill:#2ecc71,color:#fff
       style C fill:#2ecc71,color:#fff
       style D fill:#2ecc71,color:#fff

Mathematical Model
=====================

Formal Definition
---------------------

A Markov random field is a pair :math:`(G, \Phi)` where :math:`G = (V, E)` is
an undirected graph and :math:`\Phi` is a set of potential functions, each
defined over a **clique** of :math:`G`:

.. math::

   P(X_1, \ldots, X_n) = \frac{1}{Z} \prod_{c \in \mathcal{C}} \phi_c(\mathbf{X}_c)

where :math:`\mathcal{C}` is the set of cliques with an attached potential, and

.. math::

   Z = \sum_{\mathbf{x}} \prod_{c \in \mathcal{C}} \phi_c(\mathbf{x}_c)

is the **partition function**, summed over every possible joint assignment —
required to turn the unnormalized product into a true probability
distribution.

Hammersley-Clifford Theorem
--------------------------------

The theorem justifying this factorization states (informally) that a strictly
positive distribution satisfies the graph's conditional independence
structure **if and only if** it factorizes over the graph's cliques. This is
why :meth:`~sds.probabilistic.markov_random_field.MarkovRandomField.add_factor`
enforces that a factor's scope be a clique: attaching a potential over
variables that are *not* all pairwise connected would not correspond to any
consistent graph structure.

Building a Field
====================

Step-by-Step
---------------

.. code-block:: python

   from sds.probabilistic import Factor, MarkovRandomField, RandomVariable

   # 1. Define variables
   a = RandomVariable("A", ("0", "1"))
   b = RandomVariable("B", ("0", "1"))
   c = RandomVariable("C", ("0", "1"))

   # 2. Register variables and topology (undirected, cycles allowed)
   mrf = MarkovRandomField()
   for var in (a, b, c):
       mrf.add_variable(var)
   mrf.add_edge(a, b)
   mrf.add_edge(b, c)
   mrf.add_edge(c, a)  # closes the triangle -- perfectly valid

   # 3. Attach potentials over cliques
   mrf.add_factor(Factor(
       (a, b),
       {("0", "0"): 2.0, ("0", "1"): 0.5, ("1", "0"): 0.5, ("1", "1"): 2.0},
   ))

   # 4. Evaluate the unnormalized potential for a full assignment
   mrf.joint({a: "0", b: "0", c: "1"})  # only counts the a-b factor: 2.0

.. warning::

   ``joint()`` returns a value **proportional** to the true probability, not
   the probability itself — computing :math:`Z` requires summing over every
   possible assignment, an inference computation this library deliberately
   does not implement (see :doc:`../../api/probabilistic/interfaces`).

Why This Isn't a Bayesian Network
=======================================

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Aspect
     - BayesianNetwork
     - MarkovRandomField
   * - Edges
     - Directed
     - Undirected
   * - Cycles
     - Forbidden (DAG)
     - Allowed
   * - Factor semantics
     - Normalized (CPT)
     - Unnormalized (potential)
   * - ``joint()``
     - True probability
     - Proportional to probability

A grid of pixels, where each pixel's label depends symmetrically on its
neighbors (no natural "parent" direction), is the textbook example of a
dependency structure that a Bayesian network cannot represent without
arbitrarily picking a direction — but an MRF represents naturally.

Algorithm: Attaching a Valid Potential
==============================================

.. code-block:: text

   procedure ADD_FACTOR(field, factor):
       for v in factor.scope:
           if not field.has_variable(v):
               raise ValueError
       for (v_i, v_j) in pairs(factor.scope):        # O(k^2), k = scope size
           if not field.graph.has_edge(v_i, v_j):
               raise ValueError("not a clique")
       field.factors.append(factor)

Complexity Summary
======================

.. list-table::
   :header-rows: 1
   :widths: 30 25 45

   * - Operation
     - Complexity
     - Notes
   * - ``add_edge``
     - :math:`O(1)`
     - no acyclicity check
   * - ``add_factor``
     - :math:`O(k^2)`
     - k = scope size, pairwise clique validation
   * - ``joint(assignment)``
     - :math:`O(\text{number of factors})`
     - direct product, no partition function

Real-World Example: Image Denoising (Ising-style Model)
===============================================================

A classic MRF application: each pixel is a binary variable, and neighboring
pixels are encouraged to agree (a simple prior for removing noise).

.. code-block:: python

   from sds.probabilistic import Factor, MarkovRandomField, RandomVariable

   # A 2x2 pixel grid
   pixels = {
       (i, j): RandomVariable(f"P{i}{j}", ("0", "1"))
       for i in range(2) for j in range(2)
   }

   grid = MarkovRandomField()
   for var in pixels.values():
       grid.add_variable(var)

   # Horizontal and vertical neighbor edges
   grid.add_edge(pixels[(0, 0)], pixels[(0, 1)])
   grid.add_edge(pixels[(1, 0)], pixels[(1, 1)])
   grid.add_edge(pixels[(0, 0)], pixels[(1, 0)])
   grid.add_edge(pixels[(0, 1)], pixels[(1, 1)])

   # "Smoothness" potential: agreement is favored (higher value)
   smooth = {("0", "0"): 2.0, ("1", "1"): 2.0, ("0", "1"): 0.5, ("1", "0"): 0.5}
   grid.add_factor(Factor((pixels[(0, 0)], pixels[(0, 1)]), smooth))
   grid.add_factor(Factor((pixels[(1, 0)], pixels[(1, 1)]), smooth))
   grid.add_factor(Factor((pixels[(0, 0)], pixels[(1, 0)]), smooth))
   grid.add_factor(Factor((pixels[(0, 1)], pixels[(1, 1)]), smooth))

Best Practices
================

✅ **Add all relevant edges before attaching a multi-variable potential**

.. code-block:: python

   mrf.add_edge(a, b); mrf.add_edge(b, c); mrf.add_edge(c, a)
   mrf.add_factor(Factor((a, b, c), table))  # valid: {a,b,c} is a full triangle

✗ **Don't expect ``joint()`` to sum to 1 over all assignments**

.. code-block:: python

   # This is a common beginner mistake: MRF potentials are NOT probabilities
   total = sum(mrf.joint(a) for a in all_assignments)  # != 1.0 in general

Common Pitfalls
==================

1. **Forgetting the clique requirement** — a potential over
   non-fully-connected variables raises ``ValueError``, by design.
2. **Confusing potential magnitude with probability** — a higher ``joint()``
   value only means "more likely relative to other assignments *for this
   unnormalized model*", not an actual probability.
3. **Assuming completeness like a Bayesian network** — unlike
   :class:`~sds.probabilistic.bayesian_network.BayesianNetwork`, a variable
   with zero attached factors is perfectly valid here.

See Also
==========

* :doc:`../../api/probabilistic/markov_random_field` — full API reference
* :doc:`bayesian_network` — the directed counterpart
* :doc:`../graph_structures/general` — the composed ``Graph``

References
============

* **[Koller2009]** Koller, D., Friedman, N. "Probabilistic Graphical Models",
  MIT Press, 2009, Chapter 4.
* **[HammersleyClifford1971]** Hammersley, J. M., Clifford, P. "Markov fields
  on finite graphs and lattices" (unpublished manuscript, 1971).

Open Educational Resources
==============================

* **[StanfordCS228MRF]** Stanford University. "CS228 Notes: Markov random
  fields" https://ermongroup.github.io/cs228-notes/representation/undirected/
