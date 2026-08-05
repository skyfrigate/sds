.. _guide_probabilistic_hidden_markov_model:

===========================
Hidden Markov Model Guide
===========================

.. currentmodule:: sds.probabilistic

Introduction
============

A **hidden Markov model** (HMM) describes a system that evolves through a
sequence of hidden states over discrete time, where each state produces an
observation. You never see the state directly — only the observation it
produces — yet the *sequence* of observations lets you reason about the
hidden sequence that most plausibly produced them.

.. mermaid::

   graph LR
       S0((Sunny)) --> S1((Rainy)) --> S2((Rainy))
       S0 -.-> O0([No umbrella])
       S1 -.-> O1([Umbrella])
       S2 -.-> O2([Umbrella])

       style S0 fill:#f39c12,color:#fff
       style S1 fill:#3498db,color:#fff
       style S2 fill:#3498db,color:#fff

Mathematical Model
=====================

Formal Definition
---------------------

An HMM is defined by:

* A finite set of hidden states, :math:`\mathrm{dom}(S)`.
* A finite set of observation symbols, :math:`\mathrm{dom}(O)`.
* An initial distribution :math:`P(S_0)`.
* A transition model :math:`P(S_t \mid S_{t-1})`.
* An emission model :math:`P(O_t \mid S_t)`.

Two Markov-style independence assumptions make the model tractable:

.. math::

   P(S_t \mid S_0, \ldots, S_{t-1}) = P(S_t \mid S_{t-1}) \quad \text{(transition depends only on the immediately previous state)}

.. math::

   P(O_t \mid S_0, \ldots, S_t, O_0, \ldots, O_{t-1}) = P(O_t \mid S_t) \quad \text{(observation depends only on the current state)}

The joint probability of a fully known sequence factorizes as:

.. math::

   P(S_0, \ldots, S_T, O_0, \ldots, O_T) = P(S_0) \cdot \prod_{t=1}^{T} P(S_t \mid S_{t-1}) \cdot \prod_{t=0}^{T} P(O_t \mid S_t)

The "Two Variables, Three Components" Model
==================================================

Unlike :class:`~sds.probabilistic.bayesian_network.BayesianNetwork` and
:class:`~sds.probabilistic.markov_random_field.MarkovRandomField`, an HMM's
shape is fixed: exactly two variables, exactly three components. Building one
means declaring the variables, then configuring each component in turn:

.. code-block:: python

   from sds.probabilistic import Factor, HiddenMarkovModel, RandomVariable

   # 1. Declare states and observations
   weather = RandomVariable("Weather", ("sunny", "rainy"))
   umbrella = RandomVariable("Umbrella", ("yes", "no"))

   hmm = HiddenMarkovModel()
   hmm.set_states(weather)
   hmm.set_observations(umbrella)

   # A second variable, sharing weather's domain, is now available --
   # needed because the transition conditions weather on itself at t-1.
   previous = hmm.previous_states()

   # 2. Initial distribution: P(weather at t=0)
   hmm.set_initial_distribution(
       Factor((weather,), {("sunny",): 0.6, ("rainy",): 0.4})
   )

   # 3. Transition model: P(weather at t | weather at t-1)
   hmm.set_transition_model(Factor(
       (weather, previous),
       {
           ("sunny", "sunny"): 0.7, ("rainy", "sunny"): 0.3,
           ("sunny", "rainy"): 0.4, ("rainy", "rainy"): 0.6,
       },
   ))

   # 4. Emission model: P(umbrella at t | weather at t)
   hmm.set_emission_model(Factor(
       (umbrella, weather),
       {
           ("yes", "sunny"): 0.1, ("no", "sunny"): 0.9,
           ("yes", "rainy"): 0.8, ("no", "rainy"): 0.2,
       },
   ))

Why ``previous_states()`` Exists
======================================

The transition term :math:`P(S_t \mid S_{t-1})` conditions the *same*
variable on itself at a different time step. A :class:`~sds.probabilistic.factor.Factor`
resolves values through a mapping (``assignment[variable]``) — the same
:class:`~sds.probabilistic.variable.RandomVariable` cannot appear twice in one
scope, since both occurrences would collide on the same dictionary key.

``set_states()`` solves this by deriving a second variable automatically:
same domain as ``states()``, but a distinct identity. The transition factor's
scope is then ``(states, previous_states)`` — two genuinely different
objects, no collision.

.. mermaid::

   classDiagram
       class weather["weather : RandomVariable"]
       class previous["previous : RandomVariable"]
       weather : name = "Weather"
       weather : domain = (sunny, rainy)
       previous : name = "Weather__prev"
       previous : domain = (sunny, rainy)
       note for previous "Same domain, distinct identity"

Evaluating a Sequence
=========================

.. code-block:: python

   # P(weather=[sunny,rainy], umbrella=[no,yes])
   hmm.joint(["sunny", "rainy"], ["no", "yes"])
   # = P(sunny) * P(no|sunny) * P(rainy|sunny) * P(yes|rainy)
   # = 0.6      * 0.9         * 0.3            * 0.8
   # = 0.1296

Algorithm: Evaluating a Known Sequence
==============================================

.. code-block:: text

   procedure JOINT(hmm, states, observations):
       assert len(states) == len(observations) > 0
       result <- hmm.initial_distribution().value({states: states[0]})
       result <- result * hmm.emission_model().value({obs: observations[0], states: states[0]})
       for t in 1..len(states)-1:
           result <- result * hmm.transition_model().value({states: states[t], previous: states[t-1]})
           result <- result * hmm.emission_model().value({obs: observations[t], states: states[t]})
       return result

This is a direct :math:`O(T)` product over **one specific** sequence — not the
Forward algorithm (which sums over *every possible* hidden sequence to obtain
the marginal likelihood :math:`P(O_0, \ldots, O_T)`), and not Viterbi (which
searches for the single most likely hidden sequence). Both remain future
``sds.algorithms`` work.

Complexity Summary
======================

.. list-table::
   :header-rows: 1
   :widths: 35 20 45

   * - Operation
     - Complexity
     - Notes
   * - Build (declare + configure)
     - :math:`O(|\mathrm{dom}|^2)`
     - dominated by transition normalization check
   * - ``joint(states, observations)``
     - :math:`O(T)`
     - T = sequence length

Real-World Example: Part-of-Speech Tagging (Simplified)
================================================================

.. code-block:: python

   from sds.probabilistic import Factor, HiddenMarkovModel, RandomVariable

   pos = RandomVariable("POS", ("noun", "verb"))
   word_class = RandomVariable("WordClass", ("short", "long"))

   tagger = HiddenMarkovModel()
   tagger.set_states(pos)
   tagger.set_observations(word_class)
   previous_pos = tagger.previous_states()

   tagger.set_initial_distribution(
       Factor((pos,), {("noun",): 0.7, ("verb",): 0.3})
   )
   tagger.set_transition_model(Factor(
       (pos, previous_pos),
       {
           ("noun", "noun"): 0.3, ("verb", "noun"): 0.7,
           ("noun", "verb"): 0.8, ("verb", "verb"): 0.2,
       },
   ))
   tagger.set_emission_model(Factor(
       (word_class, pos),
       {
           ("short", "noun"): 0.4, ("long", "noun"): 0.6,
           ("short", "verb"): 0.7, ("long", "verb"): 0.3,
       },
   ))

   # P(tags=[noun, verb], words=[long, short])
   tagger.joint(["noun", "verb"], ["long", "short"])

Best Practices
================

✅ **Fetch ``previous_states()`` immediately after ``set_states()``**

.. code-block:: python

   hmm.set_states(weather)
   previous = hmm.previous_states()  # needed for the transition Factor

✗ **Don't try to call ``set_states()`` twice to "fix" a mistake**

.. code-block:: python

   hmm.set_states(weather)
   hmm.set_states(other_weather)  # ValueError: already set -- use clear() instead

Common Pitfalls
==================

1. **Building the transition factor with ``states`` twice** instead of
   ``(states, previous_states)`` — raises a clear scope-mismatch error, but
   easy to trip over the first time.
2. **Expecting ``joint()`` to answer "what's the most likely weather
   sequence?"** — that's Viterbi, not yet implemented.
3. **Mismatched sequence lengths** — ``joint()`` requires ``len(states) ==
   len(observations)``, both non-empty.

See Also
==========

* :doc:`../../api/probabilistic/hidden_markov_model` — full API reference
* :doc:`bayesian_network` — the CPT-validation pattern mirrored here

References
============

* **[Rabiner1989]** Rabiner, L. R. "A tutorial on hidden Markov models and
  selected applications in speech recognition", Proceedings of the IEEE,
  77(2), 257-286, 1989.
* **[BaumPetrie1966]** Baum, L. E., Petrie, T. "Statistical Inference for
  Probabilistic Functions of Finite State Markov Chains", Annals of
  Mathematical Statistics, 37(6), 1966.

Open Educational Resources
==============================

* **[Eddy2004]** Eddy, S. R. "What is a hidden Markov model?", Nature
  Biotechnology 22, 1315-1316 (2004). https://doi.org/10.1038/nbt1004-1315
* **[StanfordCS228HMM]** Stanford University. "CS228 Notes"
  https://ermongroup.github.io/cs228-notes/representation/undirected/
