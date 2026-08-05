.. _api_probabilistic_factor:

============
Factor Class
============

.. currentmodule:: sds.probabilistic.factor

Overview
========

:class:`Factor` is a non-negative, real-valued function defined over a scope
(an ordered tuple) of :doc:`variable` instances. It is pure storage plus
lookup — it makes **no** assumption about normalization, so the same class
backs a Bayesian network's conditional probability tables (locally normalized)
and a Markov random field's potentials (generally unnormalized). It plays the
same structural role for this module that ``Edge`` plays for
:doc:`../graph/index`.

Mathematical Foundation
=========================

Given a scope of variables :math:`\mathbf{X} = (X_1, \ldots, X_n)`, a factor is
a function

.. math::

   \phi(\mathbf{X}) : \mathrm{dom}(X_1) \times \cdots \times \mathrm{dom}(X_n) \to \mathbb{R}_{\geq 0}

The library requires :math:`\phi` to be **total** over the scope: the
constructor rejects any table that does not provide exactly one entry per
element of the Cartesian product :math:`\prod_i \mathrm{dom}(X_i)`, and rejects
any negative value. This is a structural (fail-fast) guarantee, not a
probabilistic one — :math:`\phi` is *not* required to sum to 1. Whether it must
(a Bayesian network CPT) or need not (a Markov random field potential) is a
constraint enforced by the *caller*, not by :class:`Factor` itself.

Detailed Documentation
========================

.. autoclass:: Factor
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __repr__
   :exclude-members: scope

Scope Order Matters — But Only At Construction
==================================================

:meth:`Factor.value` resolves lookups through a mapping
(``assignment[variable]``), not by position — so the order you pass variables
into an *assignment* dict never matters:

.. code-block:: python

   factor.value({rain: "true", sprinkler: "false"})
   factor.value({sprinkler: "false", rain: "true"})  # identical result

But the order of ``scope`` fixed at *construction* time determines how the
**table keys** must be written, since each key is a plain tuple read
positionally against ``scope``:

.. code-block:: python

   # scope = (sprinkler, rain) -> keys are (sprinkler_state, rain_state)
   Factor((sprinkler, rain), {("true", "true"): 0.01, ...})

   # scope = (rain, sprinkler) -> keys are (rain_state, sprinkler_state)
   Factor((rain, sprinkler), {("true", "true"): 0.01, ...})

Both are valid, self-consistent factors — they are simply different objects
with a different table layout. This is why
:class:`~sds.probabilistic.bayesian_network.BayesianNetwork` and
:class:`~sds.probabilistic.hidden_markov_model.HiddenMarkovModel` fix a strict
convention: **the first variable in scope is always the conditioned variable**,
the rest are the conditioning ("parent") variables — see :doc:`bayesian_network`.

Usage Examples
================

A Marginal Distribution (Single Variable)
---------------------------------------------

.. code-block:: python

   from sds.probabilistic import Factor, RandomVariable

   rain = RandomVariable("Rain", ("true", "false"))
   prior = Factor((rain,), {("true",): 0.2, ("false",): 0.8})

   prior.value({rain: "true"})  # 0.2

A Conditional Table (Two Variables)
---------------------------------------

.. code-block:: python

   sprinkler = RandomVariable("Sprinkler", ("true", "false"))

   cpt = Factor(
       (sprinkler, rain),  # sprinkler conditioned on rain
       {
           ("true", "true"): 0.01, ("false", "true"): 0.99,
           ("true", "false"): 0.4, ("false", "false"): 0.6,
       },
   )
   cpt.value({sprinkler: "true", rain: "false"})  # 0.4

An Unnormalized Potential (Markov Random Field)
----------------------------------------------------

.. code-block:: python

   # Values need not sum to 1 -- this is a valid potential, not a distribution
   potential = Factor(
       (rain, sprinkler),
       {
           ("true", "true"): 2.0, ("true", "false"): 0.5,
           ("false", "true"): 0.5, ("false", "false"): 2.0,
       },
   )

Validation Failures
------------------------

.. code-block:: python

   # Missing a combination -> ValueError ("incomplete or invalid")
   Factor((rain,), {("true",): 0.2})

   # Negative value -> ValueError ("must be non-negative")
   Factor((rain,), {("true",): -0.1, ("false",): 1.1})

Complexity
============

.. list-table::
   :header-rows: 1
   :widths: 40 25 35

   * - Operation
     - Complexity
     - Notes
   * - Construction
     - :math:`O(\prod_i |\mathrm{dom}(X_i)|)`
     - validates the full Cartesian product
   * - ``value(assignment)``
     - :math:`O(n)`
     - n = scope size (builds the lookup key), O(1) dict lookup after
   * - Storage
     - :math:`O(\prod_i |\mathrm{dom}(X_i)|)`
     - one float per joint state combination — grows exponentially with scope size

.. warning::

   Because storage and construction are exponential in scope size, factors over
   more than a handful of variables become impractical with this dense,
   table-backed representation. This is a known, deliberate limitation of the
   pedagogical design — production PGM libraries use sparse or structured
   factor representations for wide scopes.

Best Practices
================

✅ **Fix a scope-order convention and stick to it**

.. code-block:: python

   # Convention used throughout this library: conditioned variable first
   Factor((child, parent_1, parent_2, ...), table)

✗ **Don't assume normalization is checked here**

.. code-block:: python

   # Factor accepts this silently -- it is the caller's job to validate
   # normalization if the semantics require it (see BayesianNetwork.set_cpt)
   Factor((rain,), {("true",): 0.9, ("false",): 0.9})  # sums to 1.8, no error

See Also
==========

* :doc:`variable` — ``RandomVariable``, the scope element type
* :doc:`bayesian_network` — enforces normalization on top of ``Factor``
* :doc:`../graph/edge` — structural precedent (``Edge``) for this pattern

References
============

* **[1]** Koller, D., Friedman, N. "Probabilistic Graphical Models", MIT Press,
   2009, Chapter 4 (Undirected Graphical Models) for the general factor concept.
