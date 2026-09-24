# Copyright 2024-2026, skyfrigate, biface
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Variable elimination: exact marginal and conditional probabilities.

A graphical model defines a joint distribution as a normalized product of
factors, :math:`P(X) = \\frac{1}{Z} \\prod_f f(X_f)`. The probability of a
query :math:`Q` given evidence :math:`E = e` sums that product over every
other (*hidden*) variable :math:`H`:

.. math::

    P(Q \\mid e) \\;\\propto\\; \\sum_{H} \\prod_f f(Q, H, e)

Summing the full product would enumerate every joint assignment,
exponential in the number of variables. Variable elimination pushes each
sum inward instead, as far as the factors allow:

.. code-block:: text

    tables <- factors of the model, reduced by the evidence
    for each hidden variable h, in elimination order:
        combine <- tables whose scope contains h
        remove them from tables
        add  sum_h ( product of combine )  to tables
    result <- product of the remaining tables, normalized

Each step touches only the tables mentioning ``h``. The cost is exponential
in the size of the largest intermediate table, which depends on the
elimination order; finding the best order is NP-hard, so a greedy heuristic
chooses it.
"""

from typing import Dict, List, Mapping, Optional, Sequence, Set

from ...probabilistic.factor import Factor
from ...probabilistic.interfaces import AbstractGraphicalModel
from ...probabilistic.variable import RandomVariable
from ._tables import Assignment, Table
from ._validation import check_evidence, check_variables

__all__ = ["variable_elimination"]


def variable_elimination(
    model: AbstractGraphicalModel,
    query: Sequence[RandomVariable],
    evidence: Optional[Mapping[RandomVariable, str]] = None,
    order: Optional[Sequence[RandomVariable]] = None,
) -> Factor:
    """Compute the exact distribution ``P(query | evidence)``.

    Parameters
    ----------
    model : AbstractGraphicalModel
        A Bayesian network or a Markov random field. Its factors are read
        through ``factors()`` and never modified.
    query : sequence of RandomVariable
        One or more variables of the model whose joint distribution is
        wanted. They must not be observed in ``evidence``.
    evidence : mapping of RandomVariable to str, optional
        Observed states. Defaults to no evidence.
    order : sequence of RandomVariable, optional
        Order in which to eliminate the hidden variables (every variable
        that is neither queried nor observed). It must list each hidden
        variable exactly once. By default a greedy *min-size* order is
        used: at each step, eliminate the variable whose elimination builds
        the smallest table, ties broken by the model's variable order.

    Returns
    -------
    Factor
        A factor over ``query`` (in the given order) whose values are
        normalized to sum to 1.

    Raises
    ------
    ValueError
        If ``query`` is empty, contains duplicates, a variable outside the
        model, or an observed variable; if the evidence names an unknown
        variable or state; if ``order`` does not list exactly the hidden
        variables; or if the evidence has probability zero.

    Examples
    --------
    >>> from sds.probabilistic import BayesianNetwork, Factor, RandomVariable
    >>> rain = RandomVariable("Rain", ("yes", "no"))
    >>> wet = RandomVariable("Wet", ("yes", "no"))
    >>> bn = BayesianNetwork()
    >>> for v in (rain, wet):
    ...     bn.add_variable(v)
    >>> bn.add_edge(rain, wet)
    >>> bn.set_cpt(rain, Factor((rain,), {("yes",): 0.2, ("no",): 0.8}))
    >>> bn.set_cpt(wet, Factor((wet, rain), {
    ...     ("yes", "yes"): 0.9, ("no", "yes"): 0.1,
    ...     ("yes", "no"): 0.1, ("no", "no"): 0.9}))
    >>> posterior = variable_elimination(bn, [rain], {wet: "yes"})
    >>> round(posterior.value({rain: "yes"}), 4)
    0.6923

    Notes
    -----
    Time and space complexity: O(n · d^w), with n the number of variables,
    d the largest domain size and w the size of the largest table built
    during elimination (the *induced width* of the chosen order, plus one).
    On a tree-structured model w is at most the largest factor scope.

    The model's factors are copied into working tables, and all products
    and sums happen on those copies: ``Factor`` itself offers no algebra
    (#84).

    A variable that no factor mentions contributes a constant and is
    treated as uniform. For a Bayesian network, every CPT must therefore be
    set before inference.
    """
    evidence = dict(evidence or {})
    query = list(query)
    if not query:
        raise ValueError("query must contain at least one variable")
    if len(set(query)) != len(query):
        raise ValueError("query contains the same variable twice")
    check_variables(model, query)
    check_evidence(model, evidence)
    observed = [v.name for v in query if v in evidence]
    if observed:
        raise ValueError(f"query variable(s) {observed} are also observed")

    tables: List[Table] = [
        Table.from_factor(factor).reduce(evidence) for factor in model.factors()
    ]
    queried = set(query)
    hidden = [v for v in model.variables() if v not in evidence and v not in queried]
    for variable in _elimination_order(tables, hidden, order):
        tables = _eliminate(tables, variable)

    result = Table.unit()
    for table in tables:
        result = result.multiply(table)
    # Query variables that no factor mentions are uniform: give them scope.
    for variable in query:
        if variable not in result.scope:
            uniform: Dict[Assignment, float] = {
                (state,): 1.0 for state in variable.domain
            }
            result = result.multiply(Table((variable,), uniform))
    return result.reordered(tuple(query)).normalized("the query").to_factor()


def _eliminate(tables: List[Table], variable: RandomVariable) -> List[Table]:
    """Multiply the tables mentioning ``variable`` and sum it out."""
    combine = [t for t in tables if variable in t.scope]
    if not combine:
        return tables  # mentioned by no factor: contributes a constant
    rest = [t for t in tables if variable not in t.scope]
    product = combine[0]
    for table in combine[1:]:
        product = product.multiply(table)
    return rest + [product.sum_out(variable)]


def _elimination_order(
    tables: List[Table],
    hidden: List[RandomVariable],
    order: Optional[Sequence[RandomVariable]],
) -> List[RandomVariable]:
    """Validate a user order, or build the greedy min-size order."""
    if order is not None:
        order = list(order)
        if len(order) != len(set(order)) or set(order) != set(hidden):
            names = sorted(v.name for v in hidden)
            raise ValueError(
                f"order must list each hidden variable exactly once: {names}"
            )
        return order

    scopes: List[Set[RandomVariable]] = [set(t.scope) for t in tables]
    remaining = list(hidden)
    chosen: List[RandomVariable] = []
    while remaining:
        best = min(remaining, key=lambda v: _cost(scopes, v))
        merged: Set[RandomVariable] = set()
        kept: List[Set[RandomVariable]] = []
        for scope in scopes:
            if best in scope:
                merged |= scope
            else:
                kept.append(scope)
        merged.discard(best)
        scopes = kept + ([merged] if merged else [])
        remaining.remove(best)
        chosen.append(best)
    return chosen


def _cost(scopes: List[Set[RandomVariable]], variable: RandomVariable) -> int:
    """Number of entries of the table that eliminating ``variable`` builds."""
    merged: Set[RandomVariable] = set()
    for scope in scopes:
        if variable in scope:
            merged |= scope
    merged.discard(variable)
    size = 1
    for v in merged:
        size *= v.cardinality
    return size
