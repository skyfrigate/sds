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

"""Abstract interfaces for probabilistic graphical model structures.

This module provides the abstract base classes that define the contract for
``sds.probabilistic`` structures: Bayesian networks, Markov random fields,
and hidden Markov models.

These structures encode probability distributions over discrete random
variables (GitHub issue #26), backed by ``RandomVariable`` and ``Factor``.
The module intentionally holds **no inference logic** (Variable Elimination,
Belief Propagation, ...): that belongs to ``sds.algorithms``, consistent
with the strict separation of structures and algorithms (GitHub issue #14).
Topology is provided by composing ``sds.graph`` classes (``DirectedGraph``
for Bayesian networks, ``Graph`` for Markov random fields) rather than
reimplementing adjacency locally.

Classes
-------
AbstractGraphicalModel
    Common base for Bayesian networks and Markov random fields: manages
    variables and factors, evaluates a joint assignment's potential.
AbstractBayesianNetwork
    Directed, acyclic graphical model with locally normalized CPTs.
AbstractMarkovRandomField
    Undirected graphical model with (generally unnormalized) potentials;
    may contain cycles.
AbstractHiddenMarkovModel
    Sequential model over a fixed pair of variables (states, observations)
    with an initial distribution, a transition model and an emission
    model. Deliberately **not** part of the ``AbstractGraphicalModel``
    hierarchy (see Notes).

Notes
-----
``AbstractHiddenMarkovModel`` inherits directly from ``Collection``, not
from ``AbstractGraphicalModel``. An HMM does not hold an open set of
variables and factors the way a Bayesian network or Markov random field
does — it has exactly two fixed variables (states, observations) and
exactly three fixed components (initial distribution, transition model,
emission model). Forcing it under ``AbstractGraphicalModel`` would require
degenerate implementations of ``add_variable``/``variables()`` (there is no
open variable set to add to) and ``joint(assignment: Mapping[...])`` (which
cannot represent a time sequence), the same category of Liskov violation
DD-006 already avoided for ``AbstractDirectedGraph``.

The transition model conditions ``states`` on the state at the *previous*
time step — the same ``RandomVariable`` cannot appear twice in one
``Factor.scope`` (its mapping-based value lookup would collide). Each
concrete implementation therefore derives a second variable,
``previous_states``, sharing the same domain as ``states``, exposed
alongside it. With this in place, all three HMM components become
structurally identical to a Bayesian network CPT: ``initial_distribution``
is a parent-less CPT for ``states``; ``transition_model`` is ``states``
conditioned on ``previous_states``; ``emission_model`` is ``observations``
conditioned on ``states``.

See Also
--------
sds.probabilistic.variable : RandomVariable, the scope element type.
sds.probabilistic.factor : Factor, the potential-table type.
sds.graph.interfaces : AbstractDirectedGraph / AbstractGraph, composed here.
sds.core.interfaces : Collection, the root interface.
"""

from abc import ABC, abstractmethod
from typing import Any, Iterator, Mapping, Sequence

from ..core.interfaces import Collection
from .factor import Factor
from .variable import RandomVariable

__all__ = [
    "AbstractGraphicalModel",
    "AbstractBayesianNetwork",
    "AbstractMarkovRandomField",
    "AbstractHiddenMarkovModel",
]


class AbstractGraphicalModel(Collection, ABC):
    """Abstract base class for probabilistic graphical models.

    A graphical model manages a set of ``RandomVariable`` and a set of
    ``Factor`` defined over subsets of those variables. ``Collection``
    semantics (``__len__``, ``__iter__``, ``__contains__``, ``is_empty``,
    ``clear``) operate on the **variable set**, mirroring how
    ``AbstractGraph`` iterates over its structural elements (nodes).

    Notes
    -----
    Concrete implementations must provide:
    - Variable management (``add_variable``, ``has_variable``, ``get_variable``)
    - Factor management (``add_factor``, ``factors``, ``scope``)
    - Joint evaluation (``joint``)

    This class holds no inference logic. Marginal queries, MAP estimation,
    and similar require an algorithm from ``sds.algorithms`` operating on
    an instance of this class.

    See Also
    --------
    AbstractBayesianNetwork : Directed, acyclic specialization.
    AbstractMarkovRandomField : Undirected specialization.
    """

    @abstractmethod
    def add_variable(self, variable: RandomVariable) -> None:
        """Add a random variable to the model.

        Parameters
        ----------
        variable : RandomVariable
            Variable to add.

        Raises
        ------
        ValueError
            If a variable with the same name already exists in the model.
        """
        pass

    @abstractmethod
    def has_variable(self, variable: RandomVariable) -> bool:
        """Check whether ``variable`` belongs to the model.

        Parameters
        ----------
        variable : RandomVariable
            Variable to check.

        Returns
        -------
        bool
            True if ``variable`` is part of the model.
        """
        pass

    @abstractmethod
    def get_variable(self, name: str) -> RandomVariable:
        """Retrieve a variable by its name.

        Parameters
        ----------
        name : str
            Name of the variable to retrieve.

        Returns
        -------
        RandomVariable
            The matching variable.

        Raises
        ------
        KeyError
            If no variable with that name exists in the model.
        """
        pass

    @abstractmethod
    def variables(self) -> Iterator[RandomVariable]:
        """Iterate over all variables in the model.

        Yields
        ------
        RandomVariable
            Each variable currently in the model.
        """
        pass

    @abstractmethod
    def add_factor(self, factor: Factor) -> None:
        """Attach a factor to the model.

        Parameters
        ----------
        factor : Factor
            Factor to add. Every variable in ``factor.scope`` must already
            belong to the model.

        Raises
        ------
        ValueError
            If any variable in ``factor.scope`` is not part of the model.
        """
        pass

    @abstractmethod
    def factors(self) -> Iterator[Factor]:
        """Iterate over all factors attached to the model.

        Yields
        ------
        Factor
            Each factor currently attached to the model.
        """
        pass

    @abstractmethod
    def factors_for(self, variable: RandomVariable) -> Iterator[Factor]:
        """Iterate over every factor whose scope includes ``variable``.

        Parameters
        ----------
        variable : RandomVariable
            Variable to query.

        Yields
        ------
        Factor
            Each factor that references ``variable`` anywhere in its scope.

        Raises
        ------
        ValueError
            If ``variable`` is not part of the model.

        Notes
        -----
        This is the generic, model-agnostic query that inference algorithms
        (Variable Elimination, Belief Propagation, ...) need to find every
        factor touching a variable before combining them. It differs from a
        Bayesian network's own ``get_cpt(variable)``: ``get_cpt`` returns the
        single CPT *assigned to* ``variable``, whereas ``factors_for`` also
        returns other factors that merely *reference* it — for instance, in
        a Bayesian network, ``factors_for(rain)`` includes both ``Rain``'s
        own CPT and any child's CPT that conditions on ``Rain``.
        """
        pass

    @abstractmethod
    def joint(self, assignment: Mapping[RandomVariable, Any]) -> float:
        """Evaluate the model's potential for a full joint assignment.

        Parameters
        ----------
        assignment : mapping of RandomVariable to str
            Must provide a state for every variable in the model.

        Returns
        -------
        float
            The product of every attached factor's value under
            ``assignment``.

        Notes
        -----
        For a Bayesian network (locally normalized CPTs), this value *is*
        the true joint probability P(X1, ..., Xn). For a Markov random
        field, this value is only **proportional** to the true joint
        distribution; recovering the true probability requires dividing by
        the partition function Z, which is an inference concern
        (``sds.algorithms``), not a structural one.

        Raises
        ------
        KeyError
            If ``assignment`` does not cover every variable required by
            the model's factors.
        """
        pass


class AbstractBayesianNetwork(AbstractGraphicalModel, ABC):
    """Abstract base class for Bayesian network implementations.

    A Bayesian network is a directed acyclic graphical model: each variable
    has a conditional probability table (CPT) — a ``Factor`` whose scope is
    ``{variable} ∪ parents(variable)`` — locally normalized so that it sums
    to 1 over ``variable`` for every fixed configuration of its parents.

    Notes
    -----
    Implementations compose a ``sds.graph.DirectedGraph`` internally to
    carry the parent/child topology, rather than reimplementing adjacency.
    ``is_acyclic`` should delegate to the composed graph's own DAG check.

    See Also
    --------
    AbstractGraphicalModel : Base interface.
    sds.graph.interfaces.AbstractDirectedGraph : Composed for topology.
    """

    @abstractmethod
    def add_edge(self, parent: RandomVariable, child: RandomVariable) -> None:
        """Add a directed dependency from ``parent`` to ``child``.

        Parameters
        ----------
        parent : RandomVariable
            The parent (conditioning) variable.
        child : RandomVariable
            The child (dependent) variable.

        Raises
        ------
        ValueError
            If either variable is not in the model, or if adding the edge
            would introduce a cycle.
        """
        pass

    @abstractmethod
    def parents(self, variable: RandomVariable) -> Iterator[RandomVariable]:
        """Iterate over the parents of ``variable``.

        Parameters
        ----------
        variable : RandomVariable
            Variable to query.

        Yields
        ------
        RandomVariable
            Each parent of ``variable``.
        """
        pass

    @abstractmethod
    def children(self, variable: RandomVariable) -> Iterator[RandomVariable]:
        """Iterate over the children of ``variable``.

        Parameters
        ----------
        variable : RandomVariable
            Variable to query.

        Yields
        ------
        RandomVariable
            Each child of ``variable``.
        """
        pass

    @abstractmethod
    def is_acyclic(self) -> bool:
        """Check that the network's dependency graph has no cycles.

        Returns
        -------
        bool
            True if the network is a valid DAG.
        """
        pass

    @abstractmethod
    def set_cpt(self, variable: RandomVariable, factor: Factor) -> None:
        """Assign the conditional probability table for ``variable``.

        Parameters
        ----------
        variable : RandomVariable
            The variable this CPT is conditioning.
        factor : Factor
            A factor whose scope is exactly ``{variable} ∪ parents(variable)``
            and which is normalized so that, for every fixed configuration
            of the parents, the values over ``variable``'s states sum to 1.

        Raises
        ------
        ValueError
            If ``factor.scope`` does not match ``{variable} ∪ parents(variable)``,
            or if ``factor`` is not normalized per-parent-configuration.
        """
        pass


class AbstractMarkovRandomField(AbstractGraphicalModel, ABC):
    """Abstract base class for Markov random field implementations.

    A Markov random field is an undirected graphical model: edges express
    symmetric dependency between variables, and factors (potentials) are
    generally **unnormalized**. Unlike a Bayesian network, the undirected
    dependency graph may contain cycles.

    Notes
    -----
    Implementations compose a ``sds.graph.Graph`` internally to carry the
    neighbor topology, rather than reimplementing adjacency.

    See Also
    --------
    AbstractGraphicalModel : Base interface.
    sds.graph.interfaces.AbstractGraph : Composed for topology.
    """

    @abstractmethod
    def add_edge(self, first: RandomVariable, second: RandomVariable) -> None:
        """Add an undirected dependency between two variables.

        Parameters
        ----------
        first : RandomVariable
            One endpoint of the dependency.
        second : RandomVariable
            The other endpoint of the dependency.

        Raises
        ------
        ValueError
            If either variable is not in the model.
        """
        pass

    @abstractmethod
    def neighbors(self, variable: RandomVariable) -> Iterator[RandomVariable]:
        """Iterate over the variables directly dependent on ``variable``.

        Parameters
        ----------
        variable : RandomVariable
            Variable to query.

        Yields
        ------
        RandomVariable
            Each neighbor of ``variable`` in the dependency graph.
        """
        pass


class AbstractHiddenMarkovModel(Collection, ABC):
    """Abstract base class for hidden Markov model implementations.

    A hidden Markov model has exactly two fixed variables — ``states``
    (the hidden variable) and ``observations`` — and exactly three fixed
    components: an initial distribution over ``states``, a transition
    model for ``states`` conditioned on the previous time step, and an
    emission model for ``observations`` conditioned on ``states``.

    Notes
    -----
    Deliberately independent from ``AbstractGraphicalModel`` — see the
    module-level docstring for the rationale. ``Collection`` semantics
    (``__len__``, ``is_empty``, ``clear``, ``__iter__``, ``__contains__``)
    are expected to operate over the model's configuration: ``__len__``
    counts how many of the five components (states, observations, initial
    distribution, transition model, emission model) have been set;
    ``__iter__`` yields ``states()`` and ``observations()`` once set (not
    ``previous_states()``, which is a derived implementation detail, not
    a variable the caller declared); ``__contains__`` checks membership
    against ``states()``/``observations()``.

    See Also
    --------
    AbstractBayesianNetwork : The CPT-validation pattern mirrored here for
        the initial/transition/emission components.
    """

    @abstractmethod
    def set_states(self, variable: RandomVariable) -> None:
        """Register the hidden state variable.

        Also derives and exposes ``previous_states()``, a second variable
        sharing ``variable``'s domain, used as the conditioning variable
        in the transition model's scope.

        Parameters
        ----------
        variable : RandomVariable
            The hidden state variable.

        Raises
        ------
        ValueError
            If the states variable has already been set.
        """
        pass

    @abstractmethod
    def set_observations(self, variable: RandomVariable) -> None:
        """Register the observation variable.

        Parameters
        ----------
        variable : RandomVariable
            The observation variable.

        Raises
        ------
        ValueError
            If the observations variable has already been set.
        """
        pass

    @abstractmethod
    def states(self) -> RandomVariable:
        """Return the hidden state variable.

        Returns
        -------
        RandomVariable
            The variable registered via :meth:`set_states`.

        Raises
        ------
        ValueError
            If :meth:`set_states` has not been called yet.
        """
        pass

    @abstractmethod
    def previous_states(self) -> RandomVariable:
        """Return the derived "previous time step" state variable.

        Returns
        -------
        RandomVariable
            A variable sharing ``states()``'s domain, distinct from it,
            used as the conditioning variable in the transition model's
            scope.

        Raises
        ------
        ValueError
            If :meth:`set_states` has not been called yet.
        """
        pass

    @abstractmethod
    def observations(self) -> RandomVariable:
        """Return the observation variable.

        Returns
        -------
        RandomVariable
            The variable registered via :meth:`set_observations`.

        Raises
        ------
        ValueError
            If :meth:`set_observations` has not been called yet.
        """
        pass

    @abstractmethod
    def set_initial_distribution(self, factor: Factor) -> None:
        """Assign the initial distribution P(states at t=0).

        Parameters
        ----------
        factor : Factor
            A factor with scope exactly ``(states(),)``, normalized to
            sum to 1 over ``states()``'s domain.

        Raises
        ------
        ValueError
            If ``states()`` has not been set, if ``factor.scope`` does not
            match ``(states(),)``, or if ``factor`` is not normalized.
        """
        pass

    @abstractmethod
    def set_transition_model(self, factor: Factor) -> None:
        """Assign the transition model P(states at t | states at t-1).

        Parameters
        ----------
        factor : Factor
            A factor with scope exactly ``(states(), previous_states())``,
            normalized so that, for every state of ``previous_states()``,
            the values over ``states()``'s states sum to 1.

        Raises
        ------
        ValueError
            If ``states()`` has not been set, if ``factor.scope`` does not
            match ``(states(), previous_states())``, or if ``factor`` is
            not normalized per previous-state configuration.
        """
        pass

    @abstractmethod
    def set_emission_model(self, factor: Factor) -> None:
        """Assign the emission model P(observations at t | states at t).

        Parameters
        ----------
        factor : Factor
            A factor with scope exactly ``(observations(), states())``,
            normalized so that, for every state of ``states()``, the
            values over ``observations()``'s states sum to 1.

        Raises
        ------
        ValueError
            If ``states()`` or ``observations()`` have not been set, if
            ``factor.scope`` does not match ``(observations(), states())``,
            or if ``factor`` is not normalized per state configuration.
        """
        pass

    @abstractmethod
    def initial_distribution(self) -> Factor:
        """Return the initial distribution.

        Returns
        -------
        Factor
            The factor assigned via :meth:`set_initial_distribution`.

        Raises
        ------
        ValueError
            If :meth:`set_initial_distribution` has not been called yet.
        """
        pass

    @abstractmethod
    def transition_model(self) -> Factor:
        """Return the transition model.

        Returns
        -------
        Factor
            The factor assigned via :meth:`set_transition_model`.

        Raises
        ------
        ValueError
            If :meth:`set_transition_model` has not been called yet.
        """
        pass

    @abstractmethod
    def emission_model(self) -> Factor:
        """Return the emission model.

        Returns
        -------
        Factor
            The factor assigned via :meth:`set_emission_model`.

        Raises
        ------
        ValueError
            If :meth:`set_emission_model` has not been called yet.
        """
        pass

    @abstractmethod
    def joint(
        self,
        states_sequence: Sequence[str],
        observations_sequence: Sequence[str],
    ) -> float:
        """Evaluate the joint probability of a fully observed sequence.

        Computes ``P(states) x P(observations | states)`` for a specific,
        fully known sequence of hidden states and observations:
        ``P(s_0) x prod_t P(s_t | s_{t-1}) x prod_t P(o_t | s_t)``.

        Parameters
        ----------
        states_sequence : sequence of str
            The hidden state at each time step, ``states()``'s domain.
        observations_sequence : sequence of str
            The observation at each time step, ``observations()``'s
            domain. Must be the same length as ``states_sequence``.

        Returns
        -------
        float
            The joint probability of the given sequence.

        Notes
        -----
        This is a direct O(n) product over stored factors — the same kind
        of structural computation as ``AbstractGraphicalModel.joint``, not
        an inference algorithm. Recovering the *marginal* likelihood
        P(observations) by summing over every possible hidden state
        sequence (the actual Forward algorithm), or the most likely hidden
        sequence (Viterbi), is inference and belongs to ``sds.algorithms``.

        Raises
        ------
        ValueError
            If the two sequences have different lengths, if either is
            empty, or if any of the three components has not been set.
        """
        pass
