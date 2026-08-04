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

"""Unit tests for RandomVariable."""

import pytest

from sds.probabilistic.variable import RandomVariable


class TestRandomVariableCreation:
    """Test RandomVariable construction and validation."""

    def test_create_binary_variable(self) -> None:
        """Test creating a valid binary variable."""
        var = RandomVariable("Rain", ("true", "false"))
        assert var.name == "Rain"
        assert var.domain == ("true", "false")

    def test_create_ternary_variable(self) -> None:
        """Test creating a variable with more than two states."""
        var = RandomVariable("Weather", ("sunny", "rainy", "cloudy"))
        assert var.cardinality == 3

    def test_domain_with_single_state_raises(self) -> None:
        """Test that a domain with fewer than 2 states raises ValueError."""
        with pytest.raises(ValueError, match="at least 2 states"):
            RandomVariable("Constant", ("only",))

    def test_domain_empty_raises(self) -> None:
        """Test that an empty domain raises ValueError."""
        with pytest.raises(ValueError, match="at least 2 states"):
            RandomVariable("Empty", ())

    def test_duplicate_states_raise(self) -> None:
        """Test that duplicate states in the domain raise ValueError."""
        with pytest.raises(ValueError, match="duplicates"):
            RandomVariable("Broken", ("true", "true"))

    def test_domain_order_is_preserved(self) -> None:
        """Test that domain order is preserved, not sorted."""
        var = RandomVariable("Ordinal", ("high", "low", "medium"))
        assert var.domain == ("high", "low", "medium")

    def test_domain_stored_as_tuple_from_list(self) -> None:
        """Test that a list domain is normalized to a tuple."""
        var = RandomVariable("FromList", ["yes", "no"])  # type: ignore[arg-type]
        assert var.domain == ("yes", "no")
        assert isinstance(var.domain, tuple)


class TestRandomVariableProperties:
    """Test RandomVariable read-only properties."""

    def test_name_property(self, rain: RandomVariable) -> None:
        """Test the name property."""
        assert rain.name == "Rain"

    def test_domain_property(self, rain: RandomVariable) -> None:
        """Test the domain property."""
        assert rain.domain == ("true", "false")

    def test_cardinality_property(self, weather: RandomVariable) -> None:
        """Test the cardinality property matches domain length."""
        assert weather.cardinality == len(weather.domain)

    def test_slots_prevent_arbitrary_attributes(self, rain: RandomVariable) -> None:
        """Test that __slots__ blocks arbitrary attribute assignment (DD-003)."""
        with pytest.raises(AttributeError):
            rain.extra = "not allowed"  # type: ignore[attr-defined]


class TestRandomVariableIndex:
    """Test RandomVariable.index()."""

    def test_index_of_known_state(self, weather: RandomVariable) -> None:
        """Test index() returns the correct position for a known state."""
        assert weather.index("sunny") == 0
        assert weather.index("rainy") == 1
        assert weather.index("cloudy") == 2

    def test_index_of_unknown_state_raises(self, rain: RandomVariable) -> None:
        """Test index() raises ValueError for a state outside the domain."""
        with pytest.raises(ValueError, match="not a valid state"):
            rain.index("maybe")


class TestRandomVariableEquality:
    """Test RandomVariable equality and hashing semantics."""

    def test_equal_variables(self) -> None:
        """Test that two variables with the same name/domain are equal."""
        a = RandomVariable("Rain", ("true", "false"))
        b = RandomVariable("Rain", ("true", "false"))
        assert a == b

    def test_different_name_not_equal(self) -> None:
        """Test that variables with different names are not equal."""
        a = RandomVariable("Rain", ("true", "false"))
        b = RandomVariable("Sprinkler", ("true", "false"))
        assert a != b

    def test_different_domain_not_equal(self) -> None:
        """Test that variables with different domains are not equal."""
        a = RandomVariable("X", ("true", "false"))
        b = RandomVariable("X", ("yes", "no"))
        assert a != b

    def test_equality_against_other_type(self, rain: RandomVariable) -> None:
        """Test equality comparison against an unrelated type."""
        assert rain != "Rain"
        assert rain != 42

    def test_hashable_and_usable_as_dict_key(self, rain: RandomVariable) -> None:
        """Test that RandomVariable can be used as a dict key (needed by Factor)."""
        mapping = {rain: "assigned"}
        same_rain = RandomVariable("Rain", ("true", "false"))
        assert mapping[same_rain] == "assigned"

    def test_usable_in_set(self) -> None:
        """Test that RandomVariable can be stored in a set without duplication."""
        a = RandomVariable("Rain", ("true", "false"))
        b = RandomVariable("Rain", ("true", "false"))
        assert len({a, b}) == 1


class TestRandomVariableRepr:
    """Test RandomVariable string representation."""

    def test_repr_contains_name_and_domain(self, rain: RandomVariable) -> None:
        """Test that repr() includes both the name and the domain."""
        text = repr(rain)
        assert "Rain" in text
        assert "true" in text
        assert "false" in text
