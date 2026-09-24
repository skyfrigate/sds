.. _guide_algorithms_probabilistic:

=======================
Probabilistic Inference
=======================

.. currentmodule:: sds.algorithms.probabilistic_algorithms

Introduction
============

A probabilistic graphical model (see :doc:`../probabilistic_structures/index`)
describes a joint distribution compactly, as a product of small factors.
**Inference** answers questions about that distribution: how likely is a
cause given an observed effect? How likely is an observation sequence?
Which hidden sequence best explains it?

The difficulty is size. With :math:`n` binary variables the joint
distribution has :math:`2^n` entries; summing over all of them is out of
reach beyond a few dozen variables. Every algorithm on this page exploits
the factorization to avoid that enumeration, and every one of them is an
instance of **dynamic programming** (see :doc:`paradigms`).

.. list-table::
   :header-rows: 1
   :widths: 25 45 30

   * - Algorithm
     - Question
     - Model
   * - ``variable_elimination``
     - :math:`P(Q \mid e)` for chosen query variables
     - Bayesian network, Markov random field
   * - ``belief_propagation``
     - :math:`P(X \mid e)` for every variable
     - Bayesian network, Markov random field
   * - ``forward``
     - :math:`P(o_{1:T})` and :math:`P(S_t \mid o_{1:t})`
     - hidden Markov model
   * - ``viterbi``
     - :math:`\arg\max_{s_{1:T}} P(s_{1:T}, o_{1:T})`
     - hidden Markov model

Running Example: the Alarm Network
==================================

.. mermaid::

   graph TD
       B((Burglary<br/>0.001)) --> A((Alarm))
       E((Earthquake<br/>0.002)) --> A
       A --> J((JohnCalls))
       A --> M((MaryCalls))

.. list-table:: Probability that the alarm rings
   :header-rows: 1
   :widths: 50 50

   * - Burglary, Earthquake
     - :math:`P(A = \text{true} \mid B, E)`
   * - true, true
     - 0.95
   * - true, false
     - 0.94
   * - false, true
     - 0.29
   * - false, false
     - 0.001

John calls with probability 0.90 when the alarm rings and 0.05 otherwise;
Mary with probability 0.70 and 0.01.

Both neighbours call. How likely is a burglary?

Variable Elimination
====================

Idea
----

By definition, with the hidden variables :math:`E` and :math:`A` summed
out:

.. math::

   P(B \mid j, m) \;\propto\; \sum_{e} \sum_{a}
       P(B)\, P(e)\, P(a \mid B, e)\, P(j \mid a)\, P(m \mid a)

Enumerating the double sum repeats work: for each value of :math:`B` it
recomputes every product. Factors that do not mention a summed variable can
be pulled out of that sum:

.. math::

   P(B \mid j, m) \;\propto\; P(B)
       \sum_{a} P(j \mid a)\, P(m \mid a)
       \underbrace{\sum_{e} P(e)\, P(a \mid B, e)}_{\tau_1(a,\,B)}

Summing out :math:`e` first produces a new table :math:`\tau_1(a, B)`,
computed once; summing out :math:`a` then produces :math:`\tau_2(B)`. The
normalized result is :math:`P(B = \text{true} \mid j, m) \approx 0.284`.

Algorithm
---------

.. code-block:: text

    tables <- factors of the model, restricted to the evidence
    for each hidden variable h (elimination order):
        combine <- tables whose scope contains h
        tables  <- (tables - combine) + { sum_h product(combine) }
    return normalize(product(tables))

Each intermediate table is a stored subproblem: this is dynamic
programming over the factors.

Cost and Elimination Order
--------------------------

Eliminating a variable builds a table over the union of the scopes it
touches. With domains of size :math:`d` and a largest intermediate scope of
:math:`w` variables:

.. math::

   T = O(n \cdot d^{\,w})

:math:`w` depends on the order: eliminating the hub of a star graph first
creates a table over all its neighbours, eliminating the leaves first keeps
every table small. Finding the best order is NP-hard; ``sds`` uses the
greedy rule "eliminate the variable that builds the smallest table",
which works well in practice. On tree-shaped models :math:`w` never
exceeds the largest factor, and inference is linear in the model size.

Belief Propagation
==================

Messages on the Factor Graph
----------------------------

The **factor graph** connects each factor to the variables of its scope.
Belief propagation sends two kinds of messages along its edges:

.. math::

   \mu_{x \to f}(x) = \prod_{g \in N(x) \setminus \{f\}} \mu_{g \to x}(x)

   \mu_{f \to x}(x) = \sum_{\mathbf{x}_f \setminus x} f(\mathbf{x}_f)
       \prod_{y \in N(f) \setminus \{x\}} \mu_{y \to f}(y)

and every marginal is the normalized product of the messages a variable
receives:

.. math::

   P(x \mid e) \;\propto\; \prod_{f \in N(x)} \mu_{f \to x}(x)

.. mermaid::

   graph LR
       fB[P B] --- B((B))
       fE[P E] --- E((E))
       B --- fA[P A given B,E]
       E --- fA
       fA --- A((A))
       A --- fJ[P J given A]
       A --- fM[P M given A]
       fJ --- J((J))
       fM --- M((M))

Why It Is Exact on Trees
------------------------

On a tree, the message :math:`\mu_{f \to x}` summarizes exactly the part of
the model on :math:`f`'s side of the edge :math:`f - x`: removing that edge
splits the tree in two, and the recursion above is variable elimination
performed along that split. Each message is therefore computed once per
edge and direction, and all marginals come out exact for the price of two
passes.

When the Graph Has Cycles
-------------------------

On a factor graph with cycles the same updates can still be iterated, but
information comes back around each cycle and is counted more than once.
This *loopy* belief propagation often converges to good approximations, but
not to exact marginals. On the sprinkler network, whose four variables form
a cycle (Cloudy → Sprinkler → WetGrass ← Rain ← Cloudy), it estimates
:math:`P(\text{Rain} \mid \text{WetGrass}) \approx 0.78` where the exact
answer is about 0.71. ``belief_propagation()`` emits a ``RuntimeWarning``
if the messages do not settle; use ``variable_elimination`` when an exact
answer matters.

Hidden Markov Models
====================

.. mermaid::

   graph LR
       S1((Rain₁)) --> S2((Rain₂)) --> S3((Rain₃))
       S1 --> O1[Umbrella₁]
       S2 --> O2[Umbrella₂]
       S3 --> O3[Umbrella₃]

The umbrella world: each day it rains or not (hidden), and the director
arrives with an umbrella or not (observed). Rain persists with probability
0.7; an umbrella is seen on 90 % of rainy days and 20 % of dry ones.

Forward: Evaluation and Filtering
---------------------------------

Summing :math:`P(s_{1:T}, o_{1:T})` over the :math:`|S|^T` state sequences
is exponential. The forward variable
:math:`\alpha_t(s) = P(o_{1:t}, S_t = s)` satisfies a recurrence on
:math:`t`:

.. math::

   \alpha_1(s) = \pi(s)\, e(o_1 \mid s), \qquad
   \alpha_t(s) = e(o_t \mid s) \sum_{r} \alpha_{t-1}(r)\, T(s \mid r)

   P(o_{1:T}) = \sum_{s} \alpha_T(s)

There are :math:`T \cdot |S|` values, each costing :math:`O(|S|)`:

.. math::

   T_{\text{forward}} = O(T\, |S|^2)

The :math:`\alpha_t` shrink exponentially with :math:`t`. ``forward()``
divides them by their sum :math:`c_t` at every step; the rescaled values
are the **filtered** distributions :math:`P(S_t \mid o_{1:t})`, and

.. math::

   \log P(o_{1:T}) = \sum_{t=1}^{T} \log c_t

stays finite for any length. After two umbrella days,
:math:`P(\text{Rain}_2 \mid u_1, u_2) = 0.883`.

Viterbi: Decoding
-----------------

Replacing the sum by a maximum gives the probability of the best path
ending in each state, plus a pointer to its best predecessor:

.. math::

   \delta_t(s) = e(o_t \mid s)\, \max_{r}\; \delta_{t-1}(r)\, T(s \mid r),
   \qquad
   \psi_t(s) = \arg\max_{r}\; \delta_{t-1}(r)\, T(s \mid r)

The best final state is :math:`\arg\max_s \delta_T(s)`; following
:math:`\psi` backwards rebuilds the path. **Optimal substructure** makes
this correct: the best path to :math:`s` at time :math:`t` extends the best
path to some :math:`r` at time :math:`t - 1`. ``viterbi()`` works on
logarithms, so products become sums and long sequences do not underflow.

.. mermaid::

   graph LR
       R1((rain)) --> R2((rain)) --> D3((sun)) --> R4((rain)) --> R5((rain))

   %% Umbrella observed: yes, yes, no, yes, yes

.. warning::

   The most likely **path** is not the sequence of individually most
   likely states. Picking the best state at each step separately can yield
   a sequence whose transitions are improbable, or impossible, as a whole.

Summary
=======

.. list-table::
   :header-rows: 1
   :widths: 25 30 20 25

   * - Algorithm
     - Recurrence over
     - Time
     - Exact
   * - ``variable_elimination``
     - factors, one hidden variable at a time
     - :math:`O(n\, d^{\,w})`
     - yes
   * - ``belief_propagation``
     - messages on the factor graph
     - :math:`O(I \sum_f |f|)` per run
     - on trees
   * - ``forward``
     - time steps, sum
     - :math:`O(T\, |S|^2)`
     - yes
   * - ``viterbi``
     - time steps, max
     - :math:`O(T\, |S|^2)`
     - yes

References
==========

* D. Koller and N. Friedman, *Probabilistic Graphical Models*, chapters 9
  (variable elimination) and 10–11 (belief propagation); the open Stanford
  CS228 notes follow the same path — https://ermongroup.github.io/cs228-notes/
* S. Russell and P. Norvig, *Artificial Intelligence: A Modern Approach*,
  chapters 13–14 (the alarm network, the umbrella world).
* D. Jurafsky and J. H. Martin, *Speech and Language Processing* (3rd ed.
  draft, free online), appendix *Hidden Markov Models* —
  https://web.stanford.edu/~jurafsky/slp3/
* CLRS, chapter 15 (dynamic programming).
