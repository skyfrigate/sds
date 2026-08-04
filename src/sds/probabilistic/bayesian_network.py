# Copyright 2024-2025, skyfrigate, biface
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

"""Bayesian network implementation.

This module provides ``BayesianNetwork``, a concrete
``AbstractBayesianNetwork``. Topology (parent/child dependencies) is
delegated to a composed ``sds.graph.DirectedGraph`` rather than
reimplemented; each ``RandomVariable`` is wrapped in a ``GraphNode`` (using
the variable's name as node id) so the graph's own DAG check
(``is_acyclic``) can be reused directly.

No inference lives here: ``joint()`` only multiplies the stored conditional
probability tables (CPTs) together, which is a direct structural
consequence of the chain rule for Bayesian networks — not a search or
optimization algorithm. Marginal queries, MAP estimation, etc. belong to
``sds.algorithms``.

Classes
-------
BayesianNetwork
    Directed acyclic graphical model with per-variable CPTs.

Examples
--------
>>> from sds.probabilistic import BayesianNetwork, Factor, RandomVariable
>>> rain = RandomVariable("Rain", ("true", "false"))
>>> sprinkler = RandomVariable("Sprinkler", ("true", "false"))
>>> bn = BayesianNetwork()
>>> bn.add_variable(rain)
>>> bn.add_variable(sprinkler)
>>> bn.add_edge(rain, sprinkler)
>>> bn.set_cpt(rain, Factor((rain,), {("true",): 0.2, ("false",): 0.8}))
>>> sprinkler_cpt = Factor(
...     (sprinkler, rain),
...     {
...         ("true", "true"): 0.01,
...         ("false", "true"): 0.99,
...         ("true", "false"): 0.4,
...         ("false", "false"): 0.6,
...     },
... )
>>> bn.set_cpt(sprinkler, sprinkler_cpt)
>>> round(bn.joint({rain: "true", sprinkler: "true"}), 4)
0.002

See Also
--------
sds.probabilistic.interfaces.AbstractBayesianNetwork : Contract implemented here.
sds.graph.directed.DirectedGraph : Composed for topology.
"""

import math
from itertools import product
from typing import Any, Dict, Iterator, List, Mapping, Tuple

from ..graph import DirectedEdge, DirectedGraph, GraphNode
from .factor import Factor
from .interfaces import AbstractBayesianNetwork
from .variable import RandomVariable

__all__ = ["BayesianNetwork"]

_NORMALIZATION_TOLERANCE = 1e-9


class BayesianNetwork(AbstractBayesianNetwork):
    """Directed acyclic graphical model with per-variable CPTs.

    Examples
    --------
    See the module-level docstring for a full worked example.

    Notes
    -----
    Each ``RandomVariable`` is stored as the ``data`` payload of a
    ``GraphNode`` whose id is the variable's name; topology is delegated
    entirely to a composed ``DirectedGraph``.

    See Also
    --------
    AbstractBayesianNetwork : The interface this class implements.
    """

    __slots__ = ("_graph", "_variables", "_nodes", "_cpts")

    def __init__(self) -> None:
        self._graph: DirectedGraph = DirectedGraph()
        self._variables: Dict[str, RandomVariable] = {}
        self._nodes: Dict[str, GraphNode] = {}
        self._cpts: Dict[str, Factor] = {}

    # ------------------------------------------------------------------
    # Collection
    # ------------------------------------------------------------------

    def __len__(self) -> int:
        return len(self._variables)

    def is_empty(self) -> bool:
        return len(self._variables) == 0

    def clear(self) -> None:
        self._graph = DirectedGraph()
        self._variables.clear()
        self._nodes.clear()
        self._cpts.clear()

    def __iter__(self) -> Iterator[RandomVariable]:
        return iter(self._variables.values())

    def __contains__(self, item: Any) -> bool:
        return isinstance(item, RandomVariable) and self.has_variable(item)

    # ------------------------------------------------------------------
    # Variables
    # ------------------------------------------------------------------

    def add_variable(self, variable: RandomVariable) -> None:
        """See AbstractGraphicalModel.add_variable."""
        if variable.name in self._variables:
            raise ValueError(f"Variable '{variable.name}' already exists")
        node = GraphNode(variable, variable.name)
        self._graph.add_node(node)
        self._variables[variable.name] = variable
        self._nodes[variable.name] = node

    def has_variable(self, variable: RandomVariable) -> bool:
        """See AbstractGraphicalModel.has_variable."""
        return self._variables.get(variable.name) == variable

    def get_variable(self, name: str) -> RandomVariable:
        """See AbstractGraphicalModel.get_variable."""
        return self._variables[name]

    def variables(self) -> Iterator[RandomVariable]:
        """See AbstractGraphicalModel.variables."""
        return iter(self._variables.values())

    # ------------------------------------------------------------------
    # Topology (delegated to the composed DirectedGraph)
    # ------------------------------------------------------------------

    def add_edge(self, parent: RandomVariable, child: RandomVariable) -> None:
        """See AbstractBayesianNetwork.add_edge."""
        if not self.has_variable(parent):
            raise ValueError(f"'{parent.name}' is not in the network")
        if not self.has_variable(child):
            raise ValueError(f"'{child.name}' is not in the network")
        if parent == child:
            raise ValueError(f"Self-loop is not allowed ('{parent.name}')")

        edge = DirectedEdge(self._nodes[parent.name], self._nodes[child.name])
        self._graph.add_edge(edge)

        if not self._graph.is_acyclic():
            self._graph.remove_edge(edge)
            raise ValueError(
                f"Adding edge '{parent.name}' -> '{child.name}' "
                "would introduce a cycle"
            )

    def parents(self, variable: RandomVariable) -> Iterator[RandomVariable]:
        """See AbstractBayesianNetwork.parents."""
        node = self._nodes[variable.name]
        for predecessor in self._graph.predecessors(node):
            yield predecessor.data

    def children(self, variable: RandomVariable) -> Iterator[RandomVariable]:
        """See AbstractBayesianNetwork.children."""
        node = self._nodes[variable.name]
        for successor in self._graph.successors(node):
            yield successor.data

    def is_acyclic(self) -> bool:
        """See AbstractBayesianNetwork.is_acyclic."""
        return self._graph.is_acyclic()

    # ------------------------------------------------------------------
    # Factors / CPTs
    # ------------------------------------------------------------------

    def set_cpt(self, variable: RandomVariable, factor: Factor) -> None:
        """See AbstractBayesianNetwork.set_cpt."""
        if not self.has_variable(variable):
            raise ValueError(f"'{variable.name}' is not in the network")

        parent_set = set(self.parents(variable))
        if len(factor.scope) == 0 or factor.scope[0] != variable:
            raise ValueError(
                f"CPT scope for '{variable.name}' must start with '{variable.name}' "
                f"itself, got scope={[v.name for v in factor.scope]}"
            )
        if set(factor.scope[1:]) != parent_set:
            raise ValueError(
                f"CPT scope for '{variable.name}' must be "
                f"{{'{variable.name}'}} \u222a parents "
                f"({sorted(v.name for v in parent_set)}), "
                f"got {[v.name for v in factor.scope]}"
            )

        self._validate_normalization(variable, factor)
        self._cpts[variable.name] = factor

    @staticmethod
    def _validate_normalization(variable: RandomVariable, factor: Factor) -> None:
        """Check that ``factor`` sums to 1 over ``variable`` for every
        configuration of the remaining scope (its parents)."""
        parent_vars: Tuple[RandomVariable, ...] = factor.scope[1:]
        parent_domains: List[Tuple[str, ...]] = [v.domain for v in parent_vars]

        for parent_states in product(*parent_domains):
            assignment: Dict[RandomVariable, str] = dict(
                zip(parent_vars, parent_states)
            )
            total = 0.0
            for state in variable.domain:
                assignment[variable] = state
                total += factor.value(assignment)
            if not math.isclose(total, 1.0, abs_tol=_NORMALIZATION_TOLERANCE):
                raise ValueError(
                    f"CPT for '{variable.name}' is not normalized: values for "
                    f"parent configuration {dict(zip((v.name for v in parent_vars), parent_states))} "
                    f"sum to {total}, expected 1.0"
                )

    def add_factor(self, factor: Factor) -> None:
        """See AbstractGraphicalModel.add_factor.

        Convention: the first variable in ``factor.scope`` is treated as
        the conditioned variable; this is a thin wrapper around
        :meth:`set_cpt`.
        """
        if len(factor.scope) == 0:
            raise ValueError("Factor scope must contain at least one variable")
        self.set_cpt(factor.scope[0], factor)

    def factors(self) -> Iterator[Factor]:
        """See AbstractGraphicalModel.factors."""
        return iter(self._cpts.values())

    def get_cpt(self, variable: RandomVariable) -> Factor:
        """Retrieve the CPT assigned to ``variable``.

        Parameters
        ----------
        variable : RandomVariable
            Variable whose CPT to retrieve.

        Returns
        -------
        Factor
            The CPT previously assigned via :meth:`set_cpt`.

        Raises
        ------
        KeyError
            If no CPT has been set for ``variable`` yet.
        """
        return self._cpts[variable.name]

    def joint(self, assignment: Mapping[RandomVariable, Any]) -> float:
        """See AbstractGraphicalModel.joint.

        Raises
        ------
        ValueError
            If one or more variables do not have a CPT assigned yet — the
            product would silently omit their contribution otherwise.
        """
        missing = [name for name in self._variables if name not in self._cpts]
        if missing:
            raise ValueError(
                f"Cannot compute joint(): missing CPT for variable(s) {missing}"
            )

        result = 1.0
        for factor in self._cpts.values():
            result *= factor.value(assignment)
        return result

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"BayesianNetwork(variables={len(self._variables)}, "
            f"edges={self._graph.edge_count()}, cpts={len(self._cpts)})"
        )
