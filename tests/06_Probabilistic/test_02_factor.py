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

"""Unit tests for Factor."""

import pytest

from sds.probabilistic.factor import Factor
from sds.probabilistic.variable import RandomVariable


class TestFactorCreation:
    """Test Factor construction and validation."""

    def test_create_single_variable_factor(self, rain: RandomVariable) -> None:
        """Test creating a factor over a single variable."""
        factor = Factor((rain,), {("true",): 0.2, ("false",): 0.8})
        assert factor.scope == (rain,)

    def test_create_two_variable_factor(
        self,
        rain: RandomVariable,
        sprinkler: RandomVariable,
        binary_cpt_table: dict,
    ) -> None:
        """Test creating a factor over two variables with a complete table."""
        factor = Factor((rain, sprinkler), binary_cpt_table)
        assert factor.scope == (rain, sprinkler)

    def test_empty_scope_raises(self) -> None:
        """Test that an empty scope raises ValueError."""
        with pytest.raises(ValueError, match="at least one variable"):
            Factor((), {})

    def test_missing_entries_raise(self, rain: RandomVariable) -> None:
        """Test that an incomplete table (missing a combination) raises."""
        with pytest.raises(ValueError, match="incomplete or invalid"):
            Factor((rain,), {("true",): 0.2})  # missing ("false",)

    def test_unknown_key_raises(self, rain: RandomVariable) -> None:
        """Test that a table with a key outside the domain raises."""
        with pytest.raises(ValueError, match="incomplete or invalid"):
            Factor(
                (rain,),
                {("true",): 0.2, ("false",): 0.7, ("maybe",): 0.1},
            )

    def test_negative_value_raises(self, rain: RandomVariable) -> None:
        """Test that a negative table value raises ValueError."""
        with pytest.raises(ValueError, match="non-negative"):
            Factor((rain,), {("true",): -0.1, ("false",): 1.1})

    def test_full_cartesian_product_required_for_two_variables(
        self, rain: RandomVariable, sprinkler: RandomVariable
    ) -> None:
        """Test that a 2x2 scope requires exactly 4 entries."""
        incomplete = {
            ("true", "true"): 0.01,
            ("true", "false"): 0.99,
            ("false", "true"): 0.4,
            # missing ("false", "false")
        }
        with pytest.raises(ValueError, match="incomplete or invalid"):
            Factor((rain, sprinkler), incomplete)


class TestFactorValue:
    """Test Factor.value() lookups."""

    def test_value_single_variable(self, rain: RandomVariable) -> None:
        """Test value lookup for a single-variable factor."""
        factor = Factor((rain,), {("true",): 0.2, ("false",): 0.8})
        assert factor.value({rain: "true"}) == 0.2
        assert factor.value({rain: "false"}) == 0.8

    def test_value_two_variables(
        self,
        rain: RandomVariable,
        sprinkler: RandomVariable,
        binary_cpt_table: dict,
    ) -> None:
        """Test value lookup for a two-variable factor respects scope order."""
        factor = Factor((rain, sprinkler), binary_cpt_table)
        assert factor.value({rain: "true", sprinkler: "false"}) == 0.99
        assert factor.value({sprinkler: "false", rain: "true"}) == 0.99

    def test_value_ignores_extra_assignment_entries(
        self, rain: RandomVariable, weather: RandomVariable
    ) -> None:
        """Test that extra variables in the assignment mapping are ignored."""
        factor = Factor((rain,), {("true",): 0.2, ("false",): 0.8})
        assignment = {rain: "true", weather: "sunny"}
        assert factor.value(assignment) == 0.2

    def test_value_missing_variable_raises_key_error(
        self, rain: RandomVariable, sprinkler: RandomVariable, binary_cpt_table: dict
    ) -> None:
        """Test that an incomplete assignment raises KeyError."""
        factor = Factor((rain, sprinkler), binary_cpt_table)
        with pytest.raises(KeyError):
            factor.value({rain: "true"})


class TestFactorRepr:
    """Test Factor string representation."""

    def test_repr_contains_variable_names_and_entry_count(
        self,
        rain: RandomVariable,
        sprinkler: RandomVariable,
        binary_cpt_table: dict,
    ) -> None:
        """Test that repr() surfaces scope names and table size."""
        factor = Factor((rain, sprinkler), binary_cpt_table)
        text = repr(factor)
        assert "Rain" in text
        assert "Sprinkler" in text
        assert "4" in text
