.. _api_probabilistic_variable:

=====================
Random Variable Class
=====================

.. currentmodule:: sds.probabilistic.variable

Overview
========

:class:`RandomVariable` is the discrete random variable building block shared by
every structure in :doc:`index`. It plays the same structural role for this
module that ``GraphNode`` plays for :doc:`../graph/index`: a small, immutable,
hashable value referenced by container classes (:doc:`factor`,
:class:`~sds.probabilistic.bayesian_network.BayesianNetwork`,
:class:`~sds.probabilistic.markov_random_field.MarkovRandomField`,
:class:`~sds.probabilistic.hidden_markov_model.HiddenMarkovModel`).

Mathematical Foundation
=========================

A discrete random variable :math:`X` is defined by a finite, non-empty set of
mutually exclusive states — its domain:

.. math::

   \mathrm{dom}(X) = \{x_1, x_2, \ldots, x_k\}, \quad k = |\mathrm{dom}(X)| \geq 2

The library requires :math:`k \geq 2`: a variable with a single possible state
carries no information and is rejected at construction. The domain is stored as
an **ordered** tuple — this order fixes how joint state-tuples are read by
:class:`~sds.probabilistic.factor.Factor`, but carries no probabilistic meaning
by itself (states are not assumed ordinal unless the modeler treats them as such).

Detailed Documentation
========================

.. autoclass:: RandomVariable
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __eq__, __hash__, __repr__
   :exclude-members: name, domain

Equality and Hashing
=======================

Two :class:`RandomVariable` instances are equal — and hash equally — if and only
if they have the same ``name`` **and** the same ``domain``:

.. code-block:: python

   from sds.probabilistic import RandomVariable

   a = RandomVariable("Rain", ("true", "false"))
   b = RandomVariable("Rain", ("true", "false"))
   c = RandomVariable("Rain", ("yes", "no"))

   a == b        # True — same name, same domain
   a == c        # False — same name, different domain
   len({a, b})   # 1 — deduplicated

This is what allows :class:`~sds.probabilistic.factor.Factor` to use
``RandomVariable`` instances as dictionary keys in an assignment mapping, and
what allows :class:`~sds.probabilistic.bayesian_network.BayesianNetwork` to
derive a genuinely distinct ``previous_states()`` variable (different ``name``,
same ``domain``) for
:class:`~sds.probabilistic.hidden_markov_model.HiddenMarkovModel`'s transition
model — see :doc:`hidden_markov_model`.

Usage Examples
================

Creating Variables
---------------------

.. code-block:: python

   from sds.probabilistic import RandomVariable

   # Binary variable
   rain = RandomVariable("Rain", ("true", "false"))

   # Multi-state variable
   weather = RandomVariable("Weather", ("sunny", "rainy", "cloudy"))

   print(rain.cardinality)      # 2
   print(weather.cardinality)   # 3
   print(weather.index("rainy"))  # 1

Validation at Construction
------------------------------

.. code-block:: python

   from sds.probabilistic import RandomVariable

   # Rejected: fewer than 2 states
   try:
       RandomVariable("Constant", ("only",))
   except ValueError as e:
       print(e)  # "... must have at least 2 states, got 1"

   # Rejected: duplicate states
   try:
       RandomVariable("Broken", ("true", "true"))
   except ValueError as e:
       print(e)  # "... domain contains duplicates"

Complexity
============

.. list-table::
   :header-rows: 1
   :widths: 40 20 40

   * - Operation
     - Complexity
     - Notes
   * - Construction
     - O(k)
     - k = domain size (duplicate check)
   * - ``cardinality``
     - O(1)
     - ``len(domain)``
   * - ``index(state)``
     - O(k)
     - linear scan of the domain tuple
   * - Equality / hash
     - O(k)
     - compares/hashes the full domain tuple

Best Practices
================

✅ **Reuse the same instance across structures that share it**

.. code-block:: python

   # Good: the same RandomVariable object is used everywhere it appears
   rain = RandomVariable("Rain", ("true", "false"))
   bn.add_variable(rain)
   mrf.add_variable(rain)  # same variable, different structure

✗ **Don't rely on domain order carrying probabilistic meaning**

.. code-block:: python

   # The order fixes how Factor reads state tuples — it does not imply
   # the states are ordinal (e.g. "low" < "medium" < "high") unless you
   # deliberately treat them that way in your own code.
   status = RandomVariable("Status", ("low", "medium", "high"))

See Also
==========

* :doc:`factor` — potential tables defined over a scope of ``RandomVariable``
* :doc:`../graph/node` — structural precedent (``GraphNode``) for this pattern

References
============

* **[1]** Koller, D., Friedman, N. "Probabilistic Graphical Models", MIT Press,
   2009, Chapter 2 (Random Variables and Probability Distributions).
