.. _api_probabilistic_interfaces:

=====================
Abstract Interfaces
=====================

.. currentmodule:: sds.probabilistic.interfaces

Overview
========

Four abstract base classes define the contracts implemented by this module's
concrete structures. Three of them share a common ancestor
(:class:`AbstractGraphicalModel`); the fourth
(:class:`AbstractHiddenMarkovModel`) is deliberately independent. This page
documents the contracts themselves — for the reasoning behind the split, see
:ref:`why-two-families` below, and :doc:`index` for the module-level summary.

None of these interfaces declares any inference method (marginal query,
most-probable-explanation, ...). Every abstract method here is either
structural bookkeeping (register a variable, attach a factor) or a direct,
deterministic product over stored factors (``joint``) — never a search over
an exponential space of possibilities. That boundary is intentional: see
:doc:`index` for where inference is expected to live instead.

.. _why-two-families:

Why Two Independent Design Families?
========================================

``BayesianNetwork`` and ``MarkovRandomField`` both manage an **open** set of
variables and factors: you can add any number of either, at any time, and
query "what is this model's potential for a full assignment?" the same way —
multiply every stored factor together.

A hidden Markov model has a **fixed** shape: exactly two variables (states,
observations) and exactly three components (initial distribution, transition
model, emission model), never more, never fewer. Forcing it under
:class:`AbstractGraphicalModel` would require:

* A degenerate ``add_variable()``/``variables()`` — there is no open variable
  set to add to.
* A ``joint(assignment: Mapping[RandomVariable, Any])`` that cannot represent
  a *sequence* of assignments over time.

This is the same category of Liskov-substitution concern that already
justified keeping ``AbstractDirectedGraph`` separate from ``AbstractGraph`` in
:doc:`../graph/interfaces` — a method that has no coherent meaning for a
subclass should not be inherited from a shared base just for the sake of a
shorter class hierarchy.

.. mermaid::

   classDiagram
       class Collection {
           <<abstract>>
           +__len__()
           +is_empty()
           +clear()
           +__iter__()
           +__contains__(item)
       }

       class AbstractGraphicalModel {
           <<abstract>>
           +add_variable(variable)
           +has_variable(variable)
           +get_variable(name)
           +variables()
           +add_factor(factor)
           +factors()
           +factors_for(variable)
           +joint(assignment)
       }

       class AbstractBayesianNetwork {
           <<abstract>>
           +add_edge(parent, child)
           +parents(variable)
           +children(variable)
           +is_acyclic()
           +set_cpt(variable, factor)
       }

       class AbstractMarkovRandomField {
           <<abstract>>
           +add_edge(a, b)
           +neighbors(variable)
       }

       class AbstractHiddenMarkovModel {
           <<abstract>>
           +set_states(variable)
           +set_observations(variable)
           +previous_states()
           +set_initial_distribution(factor)
           +set_transition_model(factor)
           +set_emission_model(factor)
           +joint(states_seq, obs_seq)
       }

       Collection <|-- AbstractGraphicalModel
       AbstractGraphicalModel <|-- AbstractBayesianNetwork
       AbstractGraphicalModel <|-- AbstractMarkovRandomField
       Collection <|-- AbstractHiddenMarkovModel

AbstractGraphicalModel
==========================

.. autoclass:: AbstractGraphicalModel
   :members:
   :undoc-members:
   :show-inheritance:

``Collection`` semantics (``__len__``, ``__iter__``, ``__contains__``, ...)
operate on the **variable set**, mirroring how ``AbstractGraph`` iterates over
its nodes. ``joint(assignment)`` multiplies every attached factor's value for
a full assignment:

.. math::

   \phi_{\text{model}}(\mathbf{x}) = \prod_{f \in \text{factors}} f(\mathbf{x})

For a Bayesian network, this product *is* the true joint probability
:math:`P(X_1, \ldots, X_n)` (CPTs are locally normalized). For a Markov random
field, it is only **proportional** to the true joint — recovering the actual
probability requires dividing by the partition function :math:`Z`, an
inference computation deliberately left to ``sds.algorithms``.

AbstractBayesianNetwork
============================

.. autoclass:: AbstractBayesianNetwork
   :members:
   :undoc-members:
   :show-inheritance:

Adds directed, acyclic structure on top of :class:`AbstractGraphicalModel`.
Implementations are expected to compose ``sds.graph.DirectedGraph`` for
topology (see :doc:`bayesian_network`) rather than reimplementing adjacency.
A CPT set via ``set_cpt(variable, factor)`` must have a scope of exactly
``{variable} ∪ parents(variable)``, and must satisfy, for every configuration
of the parents:

.. math::

   \sum_{x \in \mathrm{dom}(\text{variable})} P(\text{variable}=x \mid \text{parents}) = 1

AbstractMarkovRandomField
==============================

.. autoclass:: AbstractMarkovRandomField
   :members:
   :undoc-members:
   :show-inheritance:

Adds undirected structure (cycles allowed) on top of
:class:`AbstractGraphicalModel`. Implementations are expected to compose
``sds.graph.Graph`` for topology (see :doc:`markov_random_field`). Unlike a
Bayesian network, a factor's scope has no normalization requirement — but is
expected to correspond to a **clique** of the underlying graph (every pair of
variables in the scope connected by an edge), per the Hammersley-Clifford
correspondence between graph structure and factorization.

AbstractHiddenMarkovModel
==============================

.. autoclass:: AbstractHiddenMarkovModel
   :members:
   :undoc-members:
   :show-inheritance:

Independent from :class:`AbstractGraphicalModel` — see
:ref:`why-two-families` above. ``Collection`` semantics here count and iterate
over the model's **configuration** rather than an open variable set:
``__len__`` counts how many of the five components (states, observations,
initial distribution, transition model, emission model) have been set;
``__iter__`` yields ``states()``/``observations()`` once set (not
``previous_states()``, a derived implementation detail); ``__contains__``
checks membership against ``states()``/``observations()``.

The transition model conditions ``states`` on the state at the *previous*
time step — the same ``RandomVariable`` cannot appear twice in one
``Factor.scope`` (its mapping-based lookup would collide on the same key).
Implementations resolve this by deriving a second variable,
``previous_states()``, sharing ``states()``'s domain but distinct from it —
see :doc:`hidden_markov_model` for the full mechanics. With that in place, all
three components become structurally identical to a Bayesian network CPT:

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Component
     - Scope
     - Equivalent to
   * - ``initial_distribution``
     - ``(states,)``
     - Parent-less CPT for ``states``
   * - ``transition_model``
     - ``(states, previous_states)``
     - CPT of ``states`` given ``previous_states``
   * - ``emission_model``
     - ``(observations, states)``
     - CPT of ``observations`` given ``states``

``joint(states_sequence, observations_sequence)`` computes, for a fully known
sequence:

.. math::

   P(s_0, \ldots, s_T, o_0, \ldots, o_T) = P(s_0) \cdot \prod_{t=1}^{T} P(s_t \mid s_{t-1}) \cdot \prod_{t=0}^{T} P(o_t \mid s_t)

This is a direct :math:`O(T)` product — not the Forward algorithm (which sums
over every possible hidden sequence to get the *marginal* likelihood
:math:`P(o_0, \ldots, o_T)`), and not Viterbi (which searches for the most
likely hidden sequence). Both remain inference, reserved for
``sds.algorithms``.

See Also
==========

* :doc:`index` — module overview and structure comparison
* :doc:`bayesian_network` / :doc:`markov_random_field` / :doc:`hidden_markov_model`
  — concrete implementations
* :doc:`../graph/interfaces` — ``AbstractDirectedGraph``/``AbstractGraph``,
  the structural precedent for the two-family split
* :doc:`../core/interfaces` — ``Collection``, the root interface

References
============

* **[1]** Koller, D., Friedman, N. "Probabilistic Graphical Models", MIT Press,
   2009.
