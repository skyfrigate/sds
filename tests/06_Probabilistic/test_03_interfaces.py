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

"""Unit tests for sds.probabilistic abstract interfaces."""

from typing import Any, Dict, Iterator, Mapping

import pytest

from sds.core.interfaces import Collection
from sds.probabilistic.factor import Factor
from sds.probabilistic.interfaces import (
    AbstractBayesianNetwork,
    AbstractGraphicalModel,
    AbstractMarkovRandomField,
)
from sds.probabilistic.variable import RandomVariable

# ============================================================================
# AbstractGraphicalModel
# ============================================================================


class TestAbstractGraphicalModelInterface:
    """Test AbstractGraphicalModel interface contract."""

    def test_is_abstract(self) -> None:
        """Test that AbstractGraphicalModel cannot be instantiated."""
        with pytest.raises(TypeError, match="abstract"):
            AbstractGraphicalModel()  # type: ignore[abstract]

    def test_inherits_from_collection(self) -> None:
        """Test that AbstractGraphicalModel inherits from Collection."""
        assert issubclass(AbstractGraphicalModel, Collection)

    def test_has_required_abstract_methods(self) -> None:
        """Test that AbstractGraphicalModel defines the required abstract methods."""
        required = {
            "__len__",
            "is_empty",
            "clear",
            "__iter__",
            "__contains__",
            "add_variable",
            "has_variable",
            "get_variable",
            "variables",
            "add_factor",
            "factors",
            "joint",
        }
        abstract_methods = {
            name
            for name in dir(AbstractGraphicalModel)
            if getattr(
                getattr(AbstractGraphicalModel, name, None),
                "__isabstractmethod__",
                False,
            )
        }
        assert required <= abstract_methods

    def test_incomplete_subclass_cannot_be_instantiated(self) -> None:
        """Test that a subclass missing methods cannot be instantiated."""

        class IncompleteModel(AbstractGraphicalModel):
            pass

        with pytest.raises(TypeError, match="abstract"):
            IncompleteModel()  # type: ignore[abstract]


class _MinimalGraphicalModel(AbstractGraphicalModel):
    """Minimal concrete AbstractGraphicalModel used only to test the contract."""

    def __init__(self) -> None:
        self._variables: Dict[str, RandomVariable] = {}
        self._factors: list[Factor] = []

    def __len__(self) -> int:
        return len(self._variables)

    def is_empty(self) -> bool:
        return len(self._variables) == 0

    def clear(self) -> None:
        self._variables.clear()
        self._factors.clear()

    def __iter__(self) -> Iterator[RandomVariable]:
        return iter(self._variables.values())

    def __contains__(self, item: Any) -> bool:
        return item in self._variables.values()

    def add_variable(self, variable: RandomVariable) -> None:
        if variable.name in self._variables:
            raise ValueError(f"Variable '{variable.name}' already exists")
        self._variables[variable.name] = variable

    def has_variable(self, variable: RandomVariable) -> bool:
        return variable.name in self._variables

    def get_variable(self, name: str) -> RandomVariable:
        return self._variables[name]

    def variables(self) -> Iterator[RandomVariable]:
        return iter(self._variables.values())

    def add_factor(self, factor: Factor) -> None:
        for variable in factor.scope:
            if not self.has_variable(variable):
                raise ValueError(f"'{variable.name}' is not in the model")
        self._factors.append(factor)

    def factors(self) -> Iterator[Factor]:
        return iter(self._factors)

    def joint(self, assignment: Mapping[RandomVariable, Any]) -> float:
        result = 1.0
        for factor in self._factors:
            result *= factor.value(assignment)
        return result


class TestConcreteGraphicalModel:
    """Test a minimal concrete AbstractGraphicalModel implementation."""

    def test_can_be_instantiated(self) -> None:
        """Test that a complete concrete subclass can be instantiated."""
        model = _MinimalGraphicalModel()
        assert isinstance(model, AbstractGraphicalModel)

    def test_add_and_contains_variable(self, rain: RandomVariable) -> None:
        """Test adding a variable and membership checks."""
        model = _MinimalGraphicalModel()
        model.add_variable(rain)
        assert rain in model
        assert len(model) == 1

    def test_joint_multiplies_factor_values(
        self,
        rain: RandomVariable,
        sprinkler: RandomVariable,
        binary_cpt_table: dict,
    ) -> None:
        """Test that joint() combines factors as documented (product)."""
        model = _MinimalGraphicalModel()
        model.add_variable(rain)
        model.add_variable(sprinkler)
        model.add_factor(Factor((rain, sprinkler), binary_cpt_table))

        assert model.joint({rain: "true", sprinkler: "false"}) == pytest.approx(0.99)

    def test_add_factor_with_unknown_variable_raises(
        self, rain: RandomVariable
    ) -> None:
        """Test that attaching a factor over an unregistered variable raises."""
        model = _MinimalGraphicalModel()
        with pytest.raises(ValueError, match="not in the model"):
            model.add_factor(Factor((rain,), {("true",): 0.2, ("false",): 0.8}))


# ============================================================================
# AbstractBayesianNetwork
# ============================================================================


class TestAbstractBayesianNetworkInterface:
    """Test AbstractBayesianNetwork interface contract."""

    def test_is_abstract(self) -> None:
        """Test that AbstractBayesianNetwork cannot be instantiated."""
        with pytest.raises(TypeError, match="abstract"):
            AbstractBayesianNetwork()  # type: ignore[abstract]

    def test_inherits_from_graphical_model(self) -> None:
        """Test that AbstractBayesianNetwork extends AbstractGraphicalModel."""
        assert issubclass(AbstractBayesianNetwork, AbstractGraphicalModel)

    def test_has_directed_specific_abstract_methods(self) -> None:
        """Test the BN-specific abstract methods are present."""
        required = {"add_edge", "parents", "children", "is_acyclic", "set_cpt"}
        abstract_methods = {
            name
            for name in dir(AbstractBayesianNetwork)
            if getattr(
                getattr(AbstractBayesianNetwork, name, None),
                "__isabstractmethod__",
                False,
            )
        }
        assert required <= abstract_methods


# ============================================================================
# AbstractMarkovRandomField
# ============================================================================


class TestAbstractMarkovRandomFieldInterface:
    """Test AbstractMarkovRandomField interface contract."""

    def test_is_abstract(self) -> None:
        """Test that AbstractMarkovRandomField cannot be instantiated."""
        with pytest.raises(TypeError, match="abstract"):
            AbstractMarkovRandomField()  # type: ignore[abstract]

    def test_inherits_from_graphical_model(self) -> None:
        """Test that AbstractMarkovRandomField extends AbstractGraphicalModel."""
        assert issubclass(AbstractMarkovRandomField, AbstractGraphicalModel)

    def test_has_undirected_specific_abstract_methods(self) -> None:
        """Test the MRF-specific abstract methods are present."""
        required = {"add_edge", "neighbors"}
        abstract_methods = {
            name
            for name in dir(AbstractMarkovRandomField)
            if getattr(
                getattr(AbstractMarkovRandomField, name, None),
                "__isabstractmethod__",
                False,
            )
        }
        assert required <= abstract_methods

    def test_bn_and_mrf_add_edge_are_independent_contracts(self) -> None:
        """Test that BN and MRF each declare their own add_edge (different arity)."""
        assert "add_edge" in AbstractBayesianNetwork.__abstractmethods__
        assert "add_edge" in AbstractMarkovRandomField.__abstractmethods__
