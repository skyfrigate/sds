.. _api_probabilistic_bayesian_network:

======================
BayesianNetwork Class
======================

.. currentmodule:: sds.probabilistic.bayesian_network

Overview
========

:class:`BayesianNetwork` is a concrete
:class:`~sds.probabilistic.interfaces.AbstractBayesianNetwork`. It composes a
``sds.graph.DirectedGraph`` internally to carry parent/child topology, rather
than reimplementing adjacency — each :class:`~sds.probabilistic.variable.RandomVariable`
is wrapped in a ``GraphNode`` (using the variable's ``name`` as the node id) so
the graph's own DAG check (``is_acyclic``) can be reused directly.

Mathematical Foundation
=========================

A Bayesian network factorizes a joint distribution over :math:`n` variables
using the chain rule, exploiting conditional independence encoded by the
directed acyclic graph:

.. math::

   P(X_1, \ldots, X_n) = \prod_{i=1}^{n} P\bigl(X_i \mid \mathrm{parents}(X_i)\bigr)

Each factor :math:`P(X_i \mid \mathrm{parents}(X_i))` is a conditional
probability table (CPT), stored as a :class:`~sds.probabilistic.factor.Factor`
whose scope is ``(X_i,) + parents(X_i)`` and which is normalized so that, for
every configuration of the parents, the values over :math:`X_i`'s states sum
to 1.

.. mermaid::

   graph TD
       Cloudy((Cloudy)) --> Sprinkler((Sprinkler))
       Cloudy --> Rain((Rain))
       Sprinkler --> WetGrass((WetGrass))
       Rain --> WetGrass

       style Cloudy fill:#3498db,color:#fff
       style WetGrass fill:#e74c3c,color:#fff

Detailed Documentation
========================

.. autoclass:: BayesianNetwork
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __repr__

Design Notes
==============

Cycle Rejection
-------------------

``DirectedGraph`` itself permits cycles (it is a general-purpose directed
graph) — the DAG constraint is enforced by :class:`BayesianNetwork` itself:
``add_edge()`` adds to the composed graph, checks ``is_acyclic()``, and rolls
back (``remove_edge``) if the new edge would introduce a cycle.

.. code-block:: python

   from sds.probabilistic import BayesianNetwork, RandomVariable

   a = RandomVariable("A", ("0", "1"))
   b = RandomVariable("B", ("0", "1"))

   bn = BayesianNetwork()
   bn.add_variable(a)
   bn.add_variable(b)
   bn.add_edge(a, b)

   bn.add_edge(b, a)  # ValueError: would introduce a cycle

CPT Scope Validated By Set, Not Order
------------------------------------------

``set_cpt()`` checks a factor's scope against ``{variable} ∪ parents(variable)``
by **set** membership, not tuple order. This is deliberate:
``DirectedGraph.predecessors()`` iterates an internal ``Set[str]`` with no
guaranteed order, so a CPT with more than one parent cannot rely on a fixed
parent ordering. This does not affect correctness —
:meth:`~sds.probabilistic.factor.Factor.value` resolves lookups by mapping,
independent of scope order.

Completeness Enforced at ``joint()``
------------------------------------------

Unlike :class:`~sds.probabilistic.markov_random_field.MarkovRandomField`,
``joint()`` raises if any registered variable does not yet have a CPT —
silently omitting a variable's contribution from the product would produce a
wrong result without any indication that something was missing.

Usage Examples
================

The Classic Rain/Sprinkler Network
----------------------------------------

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

Querying Structure
-----------------------

.. code-block:: python

   list(bn.parents(sprinkler))    # [rain]
   list(bn.children(rain))        # [sprinkler]
   bn.is_acyclic()                # True

Finding Every Factor Referencing a Variable
-------------------------------------------------

.. code-block:: python

   # factors_for(rain) returns BOTH Rain's own CPT and Sprinkler's CPT
   # (which conditions on Rain) -- unlike get_cpt(rain), which returns
   # only the CPT assigned to Rain itself.
   list(bn.factors_for(rain))   # [rain's CPT, sprinkler's CPT]
   bn.get_cpt(rain)             # rain's CPT only

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
     - O(V + E)
     - dominated by the ``is_acyclic()`` check
   * - ``set_cpt``
     - :math:`O(\prod |\mathrm{dom}(\text{parent}_i)|)`
     - normalization check enumerates every parent configuration
   * - ``parents`` / ``children``
     - O(deg)
     - delegates to ``DirectedGraph``
   * - ``joint``
     - O(number of factors)
     - one ``Factor.value`` lookup per stored CPT
   * - ``factors_for``
     - O(number of factors × scope size)
     - linear scan of stored CPTs

Best Practices
================

✅ **Add all variables and edges before setting CPTs**

.. code-block:: python

   # Good: topology is fixed, then CPTs are validated against it
   bn.add_variable(rain); bn.add_variable(sprinkler)
   bn.add_edge(rain, sprinkler)
   bn.set_cpt(sprinkler, cpt)  # validated against sprinkler's actual parents

✗ **Don't assume a fixed parent order in multi-parent CPTs**

.. code-block:: python

   # Both orders are equally valid -- the scope's OWN order at construction
   # is what matters, not the order add_edge() was called in.
   Factor((child, parent_a, parent_b), table)
   Factor((child, parent_b, parent_a), other_table)  # also valid

See Also
==========

* :doc:`interfaces` — the ``AbstractBayesianNetwork`` contract
* :doc:`markov_random_field` — the undirected counterpart
* :doc:`../graph/directed` — ``DirectedGraph``, composed here for topology
* :doc:`../../guide/probabilistic_structures/bayesian_network` — user guide

References
============

* **[1]** Pearl, J. "Probabilistic Reasoning in Intelligent Systems", Morgan
   Kaufmann, 1988.
* **[2]** Koller, D., Friedman, N. "Probabilistic Graphical Models", MIT Press,
   2009, Chapter 3 (The Bayesian Network Representation).

Open Educational Resources
============================

* **[StanfordCS228BN]** Stanford University. "CS228 Notes: Bayesian networks"
   https://ermongroup.github.io/cs228-notes/representation/directed/
