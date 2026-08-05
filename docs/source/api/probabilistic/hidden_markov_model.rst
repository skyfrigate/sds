.. _api_probabilistic_hidden_markov_model:

===========================
HiddenMarkovModel Class
===========================

.. currentmodule:: sds.probabilistic.hidden_markov_model

Overview
========

:class:`HiddenMarkovModel` is a concrete
:class:`~sds.probabilistic.interfaces.AbstractHiddenMarkovModel`. Unlike
:class:`~sds.probabilistic.bayesian_network.BayesianNetwork` and
:class:`~sds.probabilistic.markov_random_field.MarkovRandomField`, it composes
no ``sds.graph`` structure — its topology (a two-variable chain) is fixed, not
an open graph to build.

Mathematical Foundation
=========================

A hidden Markov model describes a sequence of hidden states
:math:`s_0, \ldots, s_T` (each drawn from a single, fixed domain) and a
sequence of observations :math:`o_0, \ldots, o_T`, governed by two
Markov-property assumptions:

.. math::

   P(s_t \mid s_0, \ldots, s_{t-1}) = P(s_t \mid s_{t-1}) \quad \text{(transition)}

.. math::

   P(o_t \mid s_0, \ldots, s_t, o_0, \ldots, o_{t-1}) = P(o_t \mid s_t) \quad \text{(emission)}

Together with an initial distribution :math:`P(s_0)`, the joint probability of
a *fully known* sequence factorizes as:

.. math::

   P(s_0, \ldots, s_T, o_0, \ldots, o_T) = P(s_0) \cdot \prod_{t=1}^{T} P(s_t \mid s_{t-1}) \cdot \prod_{t=0}^{T} P(o_t \mid s_t)

.. mermaid::

   graph LR
       S0((s0)) --> S1((s1)) --> S2((s2))
       S0 -.-> O0((o0))
       S1 -.-> O1((o1))
       S2 -.-> O2((o2))

       style S0 fill:#3498db,color:#fff
       style S1 fill:#3498db,color:#fff
       style S2 fill:#3498db,color:#fff
       style O0 fill:#95a5a6,color:#fff
       style O1 fill:#95a5a6,color:#fff
       style O2 fill:#95a5a6,color:#fff

The Two-Variable Problem
============================

The transition term :math:`P(s_t \mid s_{t-1})` conditions the states variable
on *itself, at a different time step*. A single
:class:`~sds.probabilistic.variable.RandomVariable` cannot appear twice in one
:class:`~sds.probabilistic.factor.Factor` scope — its mapping-based value
lookup (``assignment[variable]``) would collide on the same dictionary key for
both occurrences.

:meth:`HiddenMarkovModel.set_states` resolves this by automatically deriving a
second variable, ``previous_states()`` — same domain as ``states()``, distinct
identity (a different ``name``) — the moment ``set_states()`` is called:

.. code-block:: python

   from sds.probabilistic import HiddenMarkovModel, RandomVariable

   weather = RandomVariable("Weather", ("sunny", "rainy"))

   hmm = HiddenMarkovModel()
   hmm.set_states(weather)

   previous = hmm.previous_states()
   previous.domain == weather.domain   # True
   previous == weather                 # False -- distinct identity

With this in place, all three components become structurally identical to a
:class:`~sds.probabilistic.bayesian_network.BayesianNetwork` CPT:

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

Detailed Documentation
========================

.. autoclass:: HiddenMarkovModel
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __repr__

Design Notes
==============

Declare-Once vs. Overwrite-on-Recall
------------------------------------------

``set_states()``/``set_observations()`` may only be called **once** each —
calling either a second time raises ``ValueError``, since the variable's
*identity* is structural (changing it after ``previous_states()`` has already
been derived, or after components reference it, would silently invalidate
them). ``set_initial_distribution()``/``set_transition_model()``/
``set_emission_model()`` follow a different rule, matching
``BayesianNetwork.set_cpt()``: calling them again **replaces** the previously
stored component.

Validation Mirrors ``BayesianNetwork.set_cpt``
------------------------------------------------------

Each of the three ``set_*`` component methods checks its factor's scope
**exactly** (tuple equality, not set membership — there is at most one
conditioning variable here, so no ordering ambiguity exists the way it does
for a Bayesian network with several parents) and validates normalization per
configuration of the conditioning variable, using the same
per-parent-configuration-sums-to-1 logic as
:meth:`~sds.probabilistic.bayesian_network.BayesianNetwork.set_cpt`.

Usage Examples
================

The Classic Weather/Umbrella HMM
--------------------------------------

.. code-block:: python

   from sds.probabilistic import Factor, HiddenMarkovModel, RandomVariable

   weather = RandomVariable("Weather", ("sunny", "rainy"))
   umbrella = RandomVariable("Umbrella", ("yes", "no"))

   hmm = HiddenMarkovModel()
   hmm.set_states(weather)
   hmm.set_observations(umbrella)
   previous = hmm.previous_states()

   hmm.set_initial_distribution(
       Factor((weather,), {("sunny",): 0.6, ("rainy",): 0.4})
   )
   hmm.set_transition_model(Factor(
       (weather, previous),
       {
           ("sunny", "sunny"): 0.7, ("rainy", "sunny"): 0.3,
           ("sunny", "rainy"): 0.4, ("rainy", "rainy"): 0.6,
       },
   ))
   hmm.set_emission_model(Factor(
       (umbrella, weather),
       {
           ("yes", "sunny"): 0.1, ("no", "sunny"): 0.9,
           ("yes", "rainy"): 0.8, ("no", "rainy"): 0.2,
       },
   ))

   hmm.joint(["sunny", "rainy"], ["no", "yes"])  # 0.1296

Complexity
============

.. list-table::
   :header-rows: 1
   :widths: 35 20 45

   * - Operation
     - Complexity
     - Notes
   * - ``set_states`` / ``set_observations``
     - O(1)
     - ``previous_states`` derived in O(1) alongside ``set_states``
   * - ``set_initial_distribution``
     - :math:`O(|\mathrm{dom}(\text{states})|)`
     - normalization check, no conditioning variable
   * - ``set_transition_model`` / ``set_emission_model``
     - :math:`O(|\mathrm{dom}|^2)`
     - normalization check over one conditioning variable
   * - ``joint(states_seq, obs_seq)``
     - :math:`O(T)`
     - T = sequence length; direct product, not the Forward algorithm

.. note::

   :math:`O(T)` here evaluates the probability of **one specific, fully known**
   sequence. Computing the marginal likelihood :math:`P(o_0, \ldots, o_T)`
   over *every possible* hidden sequence (the Forward algorithm, :math:`O(T
   \cdot k^2)` with dynamic programming) or the single most likely hidden
   sequence (Viterbi, same complexity class) is inference, and is not provided
   by this class.

Best Practices
================

✅ **Always fetch ``previous_states()`` right after ``set_states()``**

.. code-block:: python

   hmm.set_states(weather)
   previous = hmm.previous_states()  # needed to build the transition Factor

✗ **Don't try to reuse ``states`` itself as the transition's "from" variable**

.. code-block:: python

   # Wrong -- collides on the same dict key inside Factor.value()
   Factor((weather, weather), table)  # nonsensical scope

   # Right -- use the derived previous_states() variable
   Factor((weather, hmm.previous_states()), table)

See Also
==========

* :doc:`interfaces` — the ``AbstractHiddenMarkovModel`` contract and the
  rationale for its independence from ``AbstractGraphicalModel``
* :doc:`bayesian_network` — the CPT-validation pattern mirrored here
* :doc:`../../guide/probabilistic_structures/hidden_markov_model` — user guide

References
============

* **[1]** Rabiner, L. R. "A tutorial on hidden Markov models and selected
   applications in speech recognition", Proceedings of the IEEE, 77(2),
   257-286, 1989.
* **[2]** Baum, L. E., Petrie, T. "Statistical Inference for Probabilistic
   Functions of Finite State Markov Chains", Annals of Mathematical
   Statistics, 37(6), 1966.

Open Educational Resources
============================

* **[Eddy2004]** Eddy, S. R. "What is a hidden Markov model?", Nature
   Biotechnology 22, 1315-1316 (2004). https://doi.org/10.1038/nbt1004-1315

   Freely accessible two-page introduction, bioinformatics-flavored but
   notation-compatible with the general HMM literature.

* **[StanfordCS228HMM]** Stanford University. "CS228 Notes: Hidden Markov models"
   https://ermongroup.github.io/cs228-notes/representation/undirected/
