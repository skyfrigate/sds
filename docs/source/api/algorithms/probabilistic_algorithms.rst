.. _api_algorithms_probabilistic:

================================
Probabilistic Inference
================================

.. currentmodule:: sds.algorithms.probabilistic_algorithms

Overview
========

The structures of :mod:`sds.probabilistic` store a model: its variables,
its graph and its factors. They answer no question about it beyond the
probability of one complete assignment (``joint()``). This subpackage holds
the inference algorithms that do:

.. list-table::
   :header-rows: 1
   :widths: 25 25 30 20

   * - Function
     - Model
     - Answers
     - Exact?
   * - :func:`variable_elimination`
     - Bayesian network, Markov random field
     - :math:`P(Q \mid e)` for one or more query variables
     - yes
   * - :func:`belief_propagation`
     - Bayesian network, Markov random field
     - :math:`P(X \mid e)` for every variable at once
     - on tree-shaped models
   * - :func:`forward`
     - hidden Markov model
     - :math:`\log P(o_{1:T})` and :math:`P(S_t \mid o_{1:t})`
     - yes
   * - :func:`viterbi`
     - hidden Markov model
     - :math:`\arg\max_{s_{1:T}} P(s_{1:T}, o_{1:T})`
     - yes

.. note::

   ``Factor`` offers no product or marginalization. Each algorithm copies
   the model's factors into private working tables through ``scope`` and
   ``value()``, computes on those copies, and returns plain ``Factor``
   objects. The model is never modified.

Throughout this page, the running examples are two classic models: Pearl's
burglary alarm network and Russell and Norvig's umbrella world.

.. mermaid::

   graph TD
       B((Burglary)) --> A((Alarm))
       E((Earthquake)) --> A
       A --> J((JohnCalls))
       A --> M((MaryCalls))

Variable Elimination
====================

The posterior of a query given evidence is a sum of the factor product over
every hidden variable. Written naively, that sum enumerates every joint
assignment, exponentially many. Variable elimination distributes each sum
over the product and eliminates the hidden variables one at a time:
multiply the tables that mention the variable, sum it out, put the result
back.

For the alarm network and the query :math:`P(B \mid j, m)`, eliminating
:math:`E` then :math:`A` gives

.. math::

   P(B \mid j, m) \;\propto\; P(B) \sum_{a} P(j \mid a)\, P(m \mid a)
       \sum_{e} P(e)\, P(a \mid B, e)

and :math:`P(B = \mathrm{true} \mid j, m) \approx 0.284`: even when both
neighbours call, a burglary remains less likely than a false alarm.

The cost is exponential in the largest intermediate table, which depends
on the elimination order. By default the order is chosen greedily, always
eliminating the variable that builds the smallest table.

.. code-block:: python

   from sds.algorithms.probabilistic_algorithms import variable_elimination

   posterior = variable_elimination(alarm, [burglary],
                                    {john_calls: "true", mary_calls: "true"})
   posterior.value({burglary: "true"})      # 0.284...

.. autofunction:: variable_elimination

Belief Propagation
==================

Belief propagation computes every marginal at once by passing messages
along the model's *factor graph*, which links each factor to the variables
of its scope. Each variable tells each neighbouring factor what the rest
of the graph thinks of it, and each factor answers by summing its table
against the other messages.

.. mermaid::

   graph LR
       B((B)) --- fA[P A given B,E]
       E((E)) --- fA
       fA --- A((A))
       A --- fJ[P J given A]
       A --- fM[P M given A]
       fJ --- J((J))
       fM --- M((M))
       B --- fB[P B]
       E --- fE[P E]

The alarm network's factor graph above is a tree: messages settle after a
few rounds and the marginals are exact, the same as variable elimination.

.. warning::

   When the factor graph contains a cycle, the same procedure is *loopy*
   belief propagation. It frequently converges to useful approximations,
   but not to the exact answer. On the sprinkler network (Cloudy →
   Sprinkler, Cloudy → Rain, both → WetGrass), it estimates
   :math:`P(\mathrm{Rain} \mid \mathrm{WetGrass}) \approx 0.78` where the
   exact value is about 0.71: the evidence travels around the cycle and is
   counted twice. If the messages do not settle within ``max_iterations``,
   a ``RuntimeWarning`` is emitted.

.. autofunction:: belief_propagation

Hidden Markov Models
====================

.. mermaid::

   graph LR
       S1((S₁)) --> S2((S₂)) --> S3((S₃))
       S1 --> O1[O₁]
       S2 --> O2[O₂]
       S3 --> O3[O₃]

A hidden Markov model is a chain of hidden states, each emitting an
observation. Two questions dominate its use: *how likely is this
observation sequence?* (evaluation, the forward algorithm) and *which
state sequence best explains it?* (decoding, the Viterbi algorithm). Both
run in :math:`O(T\,|S|^2)` instead of enumerating the :math:`|S|^T` state
sequences, by reusing, at each step, a quantity computed for the previous
one.

Forward
-------

The forward recursion carries, for each state, the probability of the
observations so far ending in that state. It is rescaled at every step,
which yields the *filtered* distributions
:math:`P(S_t \mid o_{1:t})` and keeps long sequences from underflowing;
the likelihood is returned as a logarithm.

.. code-block:: python

   from sds.algorithms.probabilistic_algorithms import forward

   log_p, filtered = forward(umbrella_hmm, ["yes", "yes"])
   filtered[-1].value({weather: "rain"})    # 0.883

.. autofunction:: forward

Viterbi
-------

Viterbi replaces the sum of the forward recursion by a maximum and keeps a
back-pointer to the best predecessor of each state; following the pointers
back from the best final state rebuilds the path. It works on logarithms,
so a zero probability becomes :math:`-\infty` and long sequences are safe.

.. code-block:: python

   from sds.algorithms.probabilistic_algorithms import viterbi

   path, log_p = viterbi(umbrella_hmm, ["yes", "yes", "no", "yes", "yes"])
   # ['rain', 'rain', 'sun', 'rain', 'rain']

.. autofunction:: viterbi

Best Practices
==============

✅ Use ``variable_elimination`` for exact answers to a few specific
queries; use ``belief_propagation`` when every marginal is needed and the
model is tree-shaped.

✅ Set every CPT of a Bayesian network before inference: a variable no
factor mentions is treated as uniform.

✅ Compare HMM sequences by log-likelihood; ``math.exp`` of a long
sequence's log-likelihood underflows to 0.0.

❌ Do not read a loopy belief propagation result as exact.

❌ Do not reconstruct the most likely *path* from the most likely state at
each step: the individually best states can form an impossible sequence.
Use ``viterbi``.

References
==========

* D. Koller and N. Friedman, *Probabilistic Graphical Models*, chapters 9
  (variable elimination), 10–11 (belief propagation) — see also the
  open Stanford CS228 notes: https://ermongroup.github.io/cs228-notes/
* Stanford CS228 notes, *Variable elimination* and *Belief propagation* —
  https://ermongroup.github.io/cs228-notes/inference/ve/,
  https://ermongroup.github.io/cs228-notes/inference/jt/
* D. Jurafsky and J. H. Martin, *Speech and Language Processing*
  (3rd ed. draft, free online), appendix *Hidden Markov Models* —
  https://web.stanford.edu/~jurafsky/slp3/
* L. R. Rabiner, *A Tutorial on Hidden Markov Models and Selected
  Applications in Speech Recognition*, Proceedings of the IEEE, 1989.
