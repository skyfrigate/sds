.. _guide_probabilistic_bayesian_network:

========================
Bayesian Network Guide
========================

.. currentmodule:: sds.probabilistic

Introduction
============

A **Bayesian network** represents a joint probability distribution as a
directed acyclic graph (DAG): each node is a random variable, each edge
represents direct probabilistic dependence, and each node carries a
conditional probability table (CPT) quantifying that dependence given its
parents.

.. mermaid::

   graph TD
       Cloudy((Cloudy)) --> Sprinkler((Sprinkler))
       Cloudy --> Rain((Rain))
       Sprinkler --> WetGrass((WetGrass))
       Rain --> WetGrass

       style Cloudy fill:#3498db,color:#fff
       style WetGrass fill:#e74c3c,color:#fff

Mathematical Model
=====================

Formal Definition
---------------------

A Bayesian network is a pair :math:`(G, \Theta)` where :math:`G = (V, E)` is a
directed acyclic graph and :math:`\Theta` is a set of conditional probability
tables, one per node:

.. math::

   \Theta = \bigl\{ P(X_i \mid \mathrm{parents}(X_i)) : X_i \in V \bigr\}

The DAG encodes a factorization of the joint distribution via the chain rule:

.. math::

   P(X_1, \ldots, X_n) = \prod_{i=1}^{n} P\bigl(X_i \mid \mathrm{parents}(X_i)\bigr)

**Local Markov property**: each variable is conditionally independent of its
non-descendants, given its parents. This is precisely what makes the
factorization above valid — without it, the chain rule would require
conditioning every :math:`X_i` on *all* preceding variables, not just its
parents.

CPT Normalization
----------------------

Each CPT must satisfy, for every configuration of the parents:

.. math::

   \sum_{x \in \mathrm{dom}(X_i)} P(X_i = x \mid \mathrm{parents}(X_i)) = 1

This is enforced at attach-time by :meth:`~sds.probabilistic.bayesian_network.BayesianNetwork.set_cpt`
— an unnormalized table raises ``ValueError`` immediately rather than
producing silently wrong results later.

Building a Network
======================

Step-by-Step
---------------

.. code-block:: python

   from sds.probabilistic import BayesianNetwork, Factor, RandomVariable

   # 1. Define variables
   rain = RandomVariable("Rain", ("true", "false"))
   sprinkler = RandomVariable("Sprinkler", ("true", "false"))
   wet_grass = RandomVariable("WetGrass", ("true", "false"))

   # 2. Register variables and topology
   bn = BayesianNetwork()
   for var in (rain, sprinkler, wet_grass):
       bn.add_variable(var)
   bn.add_edge(rain, sprinkler)
   bn.add_edge(rain, wet_grass)
   bn.add_edge(sprinkler, wet_grass)

   # 3. Attach CPTs (scope: (variable,) + parents, any parent order)
   bn.set_cpt(rain, Factor((rain,), {("true",): 0.2, ("false",): 0.8}))
   bn.set_cpt(sprinkler, Factor(
       (sprinkler, rain),
       {
           ("true", "true"): 0.01, ("false", "true"): 0.99,
           ("true", "false"): 0.4, ("false", "false"): 0.6,
       },
   ))
   bn.set_cpt(wet_grass, Factor(
       (wet_grass, rain, sprinkler),
       {
           ("true", "true", "true"): 0.99, ("false", "true", "true"): 0.01,
           ("true", "true", "false"): 0.9, ("false", "true", "false"): 0.1,
           ("true", "false", "true"): 0.9, ("false", "false", "true"): 0.1,
           ("true", "false", "false"): 0.0, ("false", "false", "false"): 1.0,
       },
   ))

   # 4. Evaluate a full assignment
   bn.joint({rain: "true", sprinkler: "true", wet_grass: "true"})
   # 0.2 * 0.01 * 0.99 == 0.00198

Why Cycles Are Rejected
---------------------------

.. math::

   P(X_1, \ldots, X_n) = \prod_i P(X_i \mid \mathrm{parents}(X_i))

only defines a valid probability distribution when the dependency graph is
**acyclic** — a cycle would make the factorization circular (X depends on Y,
which depends on X). ``add_edge()`` checks this immediately:

.. code-block:: python

   bn.add_edge(wet_grass, rain)  # ValueError: would introduce a cycle

Algorithm: Constructing a Valid Network
==============================================

.. code-block:: text

   procedure BUILD_NETWORK(variables, edges, cpts):
       network <- new BayesianNetwork
       for v in variables:
           network.add_variable(v)
       for (parent, child) in edges:
           network.add_edge(parent, child)      # O(V+E) acyclicity check
       for (variable, factor) in cpts:
           network.set_cpt(variable, factor)     # validates scope + normalization
       return network

Complexity Summary
======================

.. list-table::
   :header-rows: 1
   :widths: 30 25 45

   * - Operation
     - Complexity
     - Notes
   * - Build (n variables, e edges)
     - :math:`O(n + e^2)`
     - dominated by e acyclicity checks, each O(V+E)
   * - ``joint(assignment)``
     - :math:`O(n)`
     - one lookup per CPT
   * - Query parents/children
     - :math:`O(\mathrm{deg})`
     - delegates to the composed ``DirectedGraph``

Real-World Example: Medical Diagnosis
============================================

.. code-block:: python

   from sds.probabilistic import BayesianNetwork, Factor, RandomVariable

   flu = RandomVariable("Flu", ("true", "false"))
   fever = RandomVariable("Fever", ("true", "false"))
   cough = RandomVariable("Cough", ("true", "false"))

   diagnosis = BayesianNetwork()
   for var in (flu, fever, cough):
       diagnosis.add_variable(var)
   diagnosis.add_edge(flu, fever)
   diagnosis.add_edge(flu, cough)

   diagnosis.set_cpt(flu, Factor((flu,), {("true",): 0.05, ("false",): 0.95}))
   diagnosis.set_cpt(fever, Factor(
       (fever, flu),
       {
           ("true", "true"): 0.9, ("false", "true"): 0.1,
           ("true", "false"): 0.05, ("false", "false"): 0.95,
       },
   ))
   diagnosis.set_cpt(cough, Factor(
       (cough, flu),
       {
           ("true", "true"): 0.8, ("false", "true"): 0.2,
           ("true", "false"): 0.1, ("false", "false"): 0.9,
       },
   ))

   # Probability of having flu, fever AND cough simultaneously
   diagnosis.joint({flu: "true", fever: "true", cough: "true"})
   # 0.05 * 0.9 * 0.8 == 0.036

.. note::

   Querying "given fever and cough, what's P(flu)?" — the actually useful
   diagnostic question — requires Bayes' rule and marginalization, i.e.
   *inference*. This library's ``joint()`` only evaluates one fully specified
   assignment; the diagnostic query itself belongs to the future
   ``sds.algorithms`` inference module.

Best Practices
================

✅ **Build topology completely before attaching CPTs**

.. code-block:: python

   # Good: set_cpt validates against the network's ACTUAL parent set
   bn.add_edge(rain, sprinkler)
   bn.set_cpt(sprinkler, cpt)  # validated against {sprinkler} ∪ {rain}

✗ **Don't forget non-root variables need every parent in scope**

.. code-block:: python

   # Wrong: wet_grass has two parents (rain, sprinkler) but this factor
   # only conditions on one of them
   bn.set_cpt(wet_grass, Factor((wet_grass, rain), table))  # ValueError

Common Pitfalls
==================

1. **Assuming ``joint()`` answers diagnostic queries** — it evaluates one
   fixed assignment, not "P(cause | effect)".
2. **Forgetting a CPT** — ``joint()`` raises rather than silently omitting a
   variable's contribution; this is deliberate (see
   :doc:`../../api/probabilistic/bayesian_network`).
3. **Assuming a fixed parent order in the CPT scope** — any order is valid as
   long as it is internally consistent with the table's own keys.

See Also
==========

* :doc:`../../api/probabilistic/bayesian_network` — full API reference
* :doc:`markov_random_field` — the undirected counterpart
* :doc:`../graph_structures/directed` — the composed ``DirectedGraph``

References
============

* **[Pearl1988]** Pearl, J. "Probabilistic Reasoning in Intelligent Systems",
  Morgan Kaufmann, 1988.
* **[Koller2009]** Koller, D., Friedman, N. "Probabilistic Graphical Models",
  MIT Press, 2009, Chapter 3.

Open Educational Resources
==============================

* **[StanfordCS228BN]** Stanford University. "CS228 Notes: Bayesian networks"
  https://ermongroup.github.io/cs228-notes/representation/directed/
