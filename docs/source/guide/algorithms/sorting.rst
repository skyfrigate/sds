.. _guide_algorithms_sorting:

=======
Sorting
=======

.. currentmodule:: sds.algorithms.sorting

Introduction
============

Sorting puts the items of a sequence in order. It is rarely an end in
itself, but many algorithms start with it: Kruskal sorts edges, binary
search requires sorted data, duplicates become adjacent once sorted.

``sds.algorithms.sorting`` provides two comparison sorts, both built on
divide and conquer (see :doc:`paradigms`), with opposite trade-offs:

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * -
     - ``merge_sort``
     - ``quick_sort``
   * - Divides by
     - position (two halves)
     - value (around a pivot)
   * - Work happens
     - after the recursion (merge)
     - before the recursion (partition)
   * - Time
     - :math:`\Theta(n \log n)` always
     - :math:`O(n \log n)` expected, :math:`O(n^2)` worst
   * - Extra space
     - :math:`O(n)`
     - :math:`O(\log n)`
   * - Stable
     - yes
     - no

The Lower Bound
===============

A comparison sort learns about its input only by comparing two keys at a
time. Its possible executions form a binary *decision tree*: each internal
node is a comparison, each leaf one of the :math:`n!` orderings it may
output. A binary tree of height :math:`h` has at most :math:`2^h` leaves,
so

.. math::

   2^h \ge n! \quad\Longrightarrow\quad
   h \ge \log_2 n! \ge \log_2 \left(\frac{n}{2}\right)^{n/2}
     = \frac{n}{2} \log_2 \frac{n}{2} = \Omega(n \log n)

No comparison sort can beat :math:`n \log n` comparisons in the worst
case; merge sort is therefore optimal up to a constant factor.

Merge Sort
==========

Algorithm
---------

.. code-block:: text

    merge_sort(A[0 .. n-1]):
        if n <= 1: return A
        L <- merge_sort(A[0 .. n/2 - 1])
        R <- merge_sort(A[n/2 .. n - 1])
        return merge(L, R)

    merge(L, R):
        out <- []
        while L and R both non-empty:
            if key(R[0]) < key(L[0]): move R[0] to out
            else:                     move L[0] to out     # ties: left first
        append what remains of L, then of R
        return out

.. mermaid::

   graph TD
       A["[38, 27, 43, 3]"] --> B["[38, 27]"]
       A --> C["[43, 3]"]
       B --> D["[38]"] & E["[27]"]
       C --> F["[43]"] & G["[3]"]
       D --> H["[27, 38]"]
       E --> H
       F --> I["[3, 43]"]
       G --> I
       H --> J["[3, 27, 38, 43]"]
       I --> J

       style J fill:#2ecc71,color:#fff

Correctness
-----------

By induction on :math:`n`. Sequences of length 0 or 1 are sorted. For
:math:`n \ge 2`, both recursive calls sort strictly shorter sequences, so
:math:`L` and :math:`R` are sorted by the induction hypothesis. ``merge``
maintains the invariant *out is sorted and every element of out is not
after any remaining element of L or R*: it always moves the smaller of the
two heads, and each head is the smallest of its sorted run. When one run
is empty, the rest of the other is appended in order.

**Stability**: an element of :math:`L` comes from earlier in the input
than any element of :math:`R`, and on equal keys ``merge`` takes from
:math:`L` first.

Cost
----

.. math::

   T(n) = 2\,T\!\left(\frac{n}{2}\right) + \Theta(n)
   \quad\Longrightarrow\quad T(n) = \Theta(n \log n)

by the master theorem, whatever the input. The merged runs need
:math:`O(n)` extra memory.

Quicksort
=========

Algorithm
---------

.. code-block:: text

    quick_sort(A, lo, hi):
        while lo < hi:
            move the median of A[lo], A[mid], A[hi] to A[lo]; pivot <- A[lo]
            i <- lo - 1; j <- hi + 1
            loop:                                    # Hoare partition
                repeat i <- i + 1 until A[i] >= pivot
                repeat j <- j - 1 until A[j] <= pivot
                if i >= j: split <- j; break
                swap A[i], A[j]
            sort the smaller of A[lo..split], A[split+1..hi] recursively
            continue the loop on the larger one

After partitioning, every key of ``A[lo..split]`` is at most the pivot and
every key of ``A[split+1..hi]`` at least the pivot; both parts are
non-empty, so each is strictly smaller than the input.

Cost
----

If the pivot split the input exactly in half every time, the recurrence
would be that of merge sort: :math:`\Theta(n \log n)`. If it always
isolated a single element:

.. math::

   T(n) = T(n - 1) + \Theta(n) = \Theta(n^2)

**Expected cost.** With pivots behaving like a random choice, two keys of
ranks :math:`i < j` are compared only if one of them is the first pivot
chosen among the :math:`j - i + 1` keys of ranks :math:`i..j`, which
happens with probability :math:`2 / (j - i + 1)`. Summing over all pairs:

.. math::

   \mathbb{E}[C] = \sum_{i<j} \frac{2}{j-i+1}
                 \le 2n \sum_{k=1}^{n} \frac{1}{k}
                 = 2n H_n \approx 1.39\, n \log_2 n

The median-of-three pivot makes the classic bad inputs (already sorted,
reverse sorted) behave like the good case, and recursing only on the
smaller part bounds the stack to :math:`O(\log n)` even when a partition
is unbalanced.

Why Quicksort Is Not Stable
---------------------------

Partitioning swaps elements that are far apart, jumping over equal keys in
between. With three records of equal key:

.. code-block:: python

   records = [(0, "a"), (0, "b"), (0, "c")]
   quick_sort(records, key=lambda r: r[0])
   # [(0, 'a'), (0, 'c'), (0, 'b')] — 'b' and 'c' swapped

When the order of ties matters, use ``merge_sort``; to update the list in
place and stably, write ``items[:] = merge_sort(items)``.

Choosing a Sort
===============

.. mermaid::

   graph TD
       Q1{Must equal keys<br/>keep their order?} -->|yes| M[merge_sort]
       Q1 -->|no| Q2{Is extra memory<br/>a concern?}
       Q2 -->|yes| QS[quick_sort]
       Q2 -->|no| Q3{Is a guaranteed<br/>worst case needed?}
       Q3 -->|yes| M
       Q3 -->|no| QS

       style M fill:#2ecc71,color:#fff
       style QS fill:#3498db,color:#fff

Sorting a Structure
-------------------

Both functions take a Python ``list``: their index-based access would cost
:math:`O(n)` per access on a linked list. Convert first:

.. code-block:: python

   from sds.linear import Deque, from_list, to_list
   from sds.algorithms.sorting import merge_sort

   deque = from_list(Deque, [5, 1, 4])
   deque = from_list(Deque, merge_sort(to_list(deque)))

References
==========

* CLRS, chapters 2.3 (merge sort), 7 (quicksort) and 8.1 (lower bound for
  comparison sorting).
* OpenDSA, *Mergesort*, *Quicksort* and *Lower Bounds for Sorting* —
  https://opendsa-server.cs.vt.edu/ODSA/Books/Everything/html/Mergesort.html,
  https://opendsa-server.cs.vt.edu/ODSA/Books/Everything/html/Quicksort.html,
  https://opendsa-server.cs.vt.edu/ODSA/Books/Everything/html/SortingLowerBound.html
* R. Sedgewick and K. Wayne, *Algorithms, 4th ed.*, sections 2.2–2.3 —
  https://algs4.cs.princeton.edu/20sorting/
