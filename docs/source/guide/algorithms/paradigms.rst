.. _guide_algorithms_paradigms:

==================
Design Paradigms
==================

Introduction
============

Most algorithms of this library follow one of three classic design
strategies. Recognizing the strategy tells you how the algorithm is
proved correct and how its cost is analysed.

.. list-table::
   :header-rows: 1
   :widths: 22 38 40

   * - Paradigm
     - Idea
     - In ``sds.algorithms``
   * - Divide and conquer
     - split the problem, solve the parts recursively, combine
     - ``merge_sort``, ``quick_sort``
   * - Greedy
     - build the answer one locally best choice at a time
     - ``dijkstra``, ``kruskal``
   * - Dynamic programming
     - solve overlapping subproblems once and reuse their answers
     - ``forward``, ``viterbi``, ``variable_elimination``

Divide and Conquer
==================

A divide-and-conquer algorithm has three steps:

1. **Divide** the input into smaller instances of the same problem.
2. **Conquer** each instance recursively (small ones directly).
3. **Combine** the partial solutions into a solution of the whole.

Its running time satisfies a **recurrence**. If the input of size
:math:`n` is split into :math:`a` parts of size :math:`n/b`, and dividing
plus combining costs :math:`f(n)`:

.. math::

   T(n) = a\, T\!\left(\frac{n}{b}\right) + f(n)

The Master Theorem
------------------

Let :math:`c = \log_b a`. Then:

.. math::

   T(n) =
   \begin{cases}
     \Theta(n^{c}) & \text{if } f(n) = O(n^{c - \varepsilon}) \text{ for some } \varepsilon > 0 \\
     \Theta(n^{c} \log n) & \text{if } f(n) = \Theta(n^{c}) \\
     \Theta(f(n)) & \text{if } f(n) = \Omega(n^{c + \varepsilon}) \text{ and } a f(n/b) \le k f(n),\ k < 1
   \end{cases}

**Merge sort** splits into :math:`a = 2` halves of size :math:`n/2` and
merges in :math:`\Theta(n)`: :math:`c = \log_2 2 = 1`, so the second case
applies and :math:`T(n) = \Theta(n \log n)`.

.. mermaid::

   graph TD
       A["n — merge cost n"] --> B["n/2"]
       A --> C["n/2"]
       B --> D["n/4"]
       B --> E["n/4"]
       C --> F["n/4"]
       C --> G["n/4"]

   %% Each level costs n in total; there are log2 n levels.

The recursion tree makes it visible: level :math:`i` holds :math:`2^i`
subproblems of size :math:`n/2^i`, so every level costs :math:`n` in
total, and there are :math:`\log_2 n` levels.

Greedy Algorithms
=================

A greedy algorithm builds its answer step by step, always taking the
choice that looks best *now*, and never revisits a choice. It is fast and
simple, but correct only for problems with two properties:

- **Greedy-choice property**: some optimal solution contains the greedy
  choice.
- **Optimal substructure**: once the greedy choice is made, the rest of an
  optimal solution is an optimal solution of the remaining subproblem.

Greedy algorithms are usually proved correct by an **exchange argument**:
take any optimal solution that differs from the greedy one, and show it can
be modified, without getting worse, to agree with the greedy choice.

**Kruskal** is proved this way through the cut property (see
:ref:`guide_algorithms_mst`); **Dijkstra** through the invariant that every
settled distance is final (see :ref:`guide_algorithms_shortest_paths`).

.. warning::

   Greed fails as soon as a local choice can be undone by later
   information. With a negative edge weight, the node Dijkstra settles
   first may later be reached more cheaply; that is why ``dijkstra()``
   rejects negative weights.

Dynamic Programming
===================

Dynamic programming applies when a problem breaks into subproblems that
**overlap**: the same subproblem is needed many times. Instead of solving
it again each time, its answer is computed once and stored in a table.
Two ingredients are required:

- **Optimal substructure** (or, for sums, *decomposability*): the answer to
  the problem is a simple function of answers to subproblems.
- **Overlapping subproblems**: the number of distinct subproblems is small
  (polynomial), even if a naive recursion would visit them exponentially
  often.

**Viterbi** is a textbook example. The best path ending in state :math:`s`
at time :math:`t` extends the best path ending in some state :math:`r` at
time :math:`t-1`:

.. math::

   \delta_t(s) = e(o_t \mid s)\, \max_{r} \delta_{t-1}(r)\, T(s \mid r)

There are only :math:`T \cdot |S|` values :math:`\delta_t(s)`, each
computed in :math:`O(|S|)`: :math:`O(T |S|^2)` in total, instead of
enumerating :math:`|S|^T` paths. The **forward** algorithm has the same
shape with a sum in place of the maximum, and **variable elimination** is
dynamic programming over the factors of a graphical model, each
intermediate table being a stored subproblem.

Summary
=======

.. list-table::
   :header-rows: 1
   :widths: 20 30 25 25

   * - Paradigm
     - Correctness argument
     - Cost analysis
     - Typical pitfall
   * - Divide and conquer
     - induction on the input size
     - recurrence, master theorem
     - unbalanced splits (quicksort worst case)
   * - Greedy
     - exchange argument, invariant
     - sorting or priority queue cost
     - applied where the greedy choice is not safe
   * - Dynamic programming
     - optimal substructure
     - number of subproblems × cost per subproblem
     - exponential table size

References
==========

* T. H. Cormen, C. E. Leiserson, R. L. Rivest, C. Stein, *Introduction to
  Algorithms* (CLRS), 3rd ed., chapters 4 (divide and conquer, master
  theorem), 15 (dynamic programming) and 16 (greedy algorithms).
* OpenDSA, *Algorithm Analysis* and *Recurrence Relations* modules —
  https://opendsa-server.cs.vt.edu/ODSA/Books/Everything/html/
* J. Erickson, *Algorithms* (open-access), chapters 1 (recursion), 3
  (dynamic programming) and 4 (greedy algorithms) —
  https://jeffe.cs.illinois.edu/teaching/algorithms/
