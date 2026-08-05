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

"""Unit tests for MarkovRandomField."""

import pytest

from sds.probabilistic.factor import Factor
from sds.probabilistic.interfaces import AbstractMarkovRandomField
from sds.probabilistic.markov_random_field import MarkovRandomField
from sds.probabilistic.variable import RandomVariable


class TestMarkovRandomFieldCreation:
    """Test MarkovRandomField construction."""

    def test_empty_field(self) -> None:
        """Test that a new field is empty."""
        mrf = MarkovRandomField()
        assert len(mrf) == 0
        assert mrf.is_empty()

    def test_satisfies_abstract_interface(self) -> None:
        """Test that MarkovRandomField is an AbstractMarkovRandomField."""
        assert isinstance(MarkovRandomField(), AbstractMarkovRandomField)


class TestVariableManagement:
    """Test variable registration on MarkovRandomField."""

    def test_add_variable(self, rain: RandomVariable) -> None:
        """Test adding a variable increases the field size."""
        mrf = MarkovRandomField()
        mrf.add_variable(rain)
        assert len(mrf) == 1

    def test_add_duplicate_variable_raises(self, rain: RandomVariable) -> None:
        """Test that re-adding the same variable name raises ValueError."""
        mrf = MarkovRandomField()
        mrf.add_variable(rain)
        with pytest.raises(ValueError, match="already exists"):
            mrf.add_variable(RandomVariable("Rain", ("true", "false")))

    def test_has_variable(
        self, rain: RandomVariable, sprinkler: RandomVariable
    ) -> None:
        """Test has_variable distinguishes registered from unregistered variables."""
        mrf = MarkovRandomField()
        mrf.add_variable(rain)
        assert mrf.has_variable(rain) is True
        assert mrf.has_variable(sprinkler) is False

    def test_get_variable(self, rain: RandomVariable) -> None:
        """Test retrieving a variable by name."""
        mrf = MarkovRandomField()
        mrf.add_variable(rain)
        assert mrf.get_variable("Rain") == rain

    def test_get_unknown_variable_raises_key_error(self) -> None:
        """Test that get_variable on an unknown name raises KeyError."""
        mrf = MarkovRandomField()
        with pytest.raises(KeyError):
            mrf.get_variable("Unknown")

    def test_variables_iteration(
        self, rain: RandomVariable, sprinkler: RandomVariable
    ) -> None:
        """Test iterating over all registered variables."""
        mrf = MarkovRandomField()
        mrf.add_variable(rain)
        mrf.add_variable(sprinkler)
        assert set(mrf.variables()) == {rain, sprinkler}

    def test_contains_and_iter(
        self, rain: RandomVariable, sprinkler: RandomVariable
    ) -> None:
        """Test __contains__ and __iter__ Collection semantics."""
        mrf = MarkovRandomField()
        mrf.add_variable(rain)
        assert rain in mrf
        assert sprinkler not in mrf
        assert list(mrf) == [rain]

    def test_contains_rejects_non_variable(self, rain: RandomVariable) -> None:
        """Test that __contains__ returns False for non-RandomVariable objects."""
        mrf = MarkovRandomField()
        mrf.add_variable(rain)
        assert "Rain" not in mrf


class TestEdgeManagement:
    """Test add_edge and undirected topology (cycles allowed)."""

    def test_add_edge(self, rain: RandomVariable, sprinkler: RandomVariable) -> None:
        """Test adding a valid undirected edge is symmetric."""
        mrf = MarkovRandomField()
        mrf.add_variable(rain)
        mrf.add_variable(sprinkler)
        mrf.add_edge(rain, sprinkler)
        assert list(mrf.neighbors(rain)) == [sprinkler]
        assert list(mrf.neighbors(sprinkler)) == [rain]

    def test_add_edge_unknown_first_raises(
        self, rain: RandomVariable, sprinkler: RandomVariable
    ) -> None:
        """Test that referencing an unregistered variable raises ValueError."""
        mrf = MarkovRandomField()
        mrf.add_variable(sprinkler)
        with pytest.raises(ValueError, match="not in the field"):
            mrf.add_edge(rain, sprinkler)

    def test_add_edge_unknown_second_raises(
        self, rain: RandomVariable, sprinkler: RandomVariable
    ) -> None:
        """Test that referencing an unregistered second variable raises ValueError."""
        mrf = MarkovRandomField()
        mrf.add_variable(rain)
        with pytest.raises(ValueError, match="not in the field"):
            mrf.add_edge(rain, sprinkler)

    def test_self_loop_raises(self, rain: RandomVariable) -> None:
        """Test that a variable cannot neighbor itself."""
        mrf = MarkovRandomField()
        mrf.add_variable(rain)
        with pytest.raises(ValueError, match="Self-loop"):
            mrf.add_edge(rain, rain)

    def test_cycle_is_allowed(
        self,
        rain: RandomVariable,
        sprinkler: RandomVariable,
        cloudy: RandomVariable,
    ) -> None:
        """Test that a 3-node cycle is permitted (unlike BayesianNetwork)."""
        mrf = MarkovRandomField()
        for var in (rain, sprinkler, cloudy):
            mrf.add_variable(var)
        mrf.add_edge(rain, sprinkler)
        mrf.add_edge(sprinkler, cloudy)
        mrf.add_edge(cloudy, rain)  # closes the triangle, no error expected

        assert set(mrf.neighbors(rain)) == {sprinkler, cloudy}

    def test_duplicate_edge_raises(
        self, rain: RandomVariable, sprinkler: RandomVariable
    ) -> None:
        """Test that adding the same edge twice raises ValueError."""
        mrf = MarkovRandomField()
        mrf.add_variable(rain)
        mrf.add_variable(sprinkler)
        mrf.add_edge(rain, sprinkler)
        with pytest.raises(ValueError):
            mrf.add_edge(rain, sprinkler)

    def test_isolated_variable_has_no_neighbors(self, rain: RandomVariable) -> None:
        """Test that a variable with no edges has an empty neighbor set."""
        mrf = MarkovRandomField()
        mrf.add_variable(rain)
        assert list(mrf.neighbors(rain)) == []


class TestFactorManagement:
    """Test add_factor and the clique-validity constraint."""

    def test_add_factor_over_an_edge(
        self,
        rain: RandomVariable,
        sprinkler: RandomVariable,
        binary_cpt_table: dict,
    ) -> None:
        """Test attaching a potential over two variables connected by an edge."""
        mrf = MarkovRandomField()
        mrf.add_variable(rain)
        mrf.add_variable(sprinkler)
        mrf.add_edge(rain, sprinkler)
        potential = Factor((rain, sprinkler), binary_cpt_table)
        mrf.add_factor(potential)
        assert list(mrf.factors()) == [potential]

    def test_add_factor_unknown_variable_raises(self, rain: RandomVariable) -> None:
        """Test that a factor over an unregistered variable raises."""
        mrf = MarkovRandomField()
        with pytest.raises(ValueError, match="not in the field"):
            mrf.add_factor(Factor((rain,), {("true",): 0.3, ("false",): 0.7}))

    def test_add_factor_over_single_variable_never_needs_a_clique_check(
        self, rain: RandomVariable
    ) -> None:
        """Test that a single-variable potential requires no edge at all."""
        mrf = MarkovRandomField()
        mrf.add_variable(rain)
        potential = Factor((rain,), {("true",): 0.3, ("false",): 0.7})
        mrf.add_factor(potential)
        assert list(mrf.factors()) == [potential]

    def test_add_factor_without_edge_raises(
        self,
        rain: RandomVariable,
        sprinkler: RandomVariable,
        binary_cpt_table: dict,
    ) -> None:
        """Test that a 2-variable potential without a connecting edge raises."""
        mrf = MarkovRandomField()
        mrf.add_variable(rain)
        mrf.add_variable(sprinkler)
        # No edge added between rain and sprinkler.
        potential = Factor((rain, sprinkler), binary_cpt_table)
        with pytest.raises(ValueError, match="not a clique"):
            mrf.add_factor(potential)

    def test_add_factor_over_non_clique_triple_raises(
        self,
        rain: RandomVariable,
        sprinkler: RandomVariable,
        cloudy: RandomVariable,
    ) -> None:
        """Test that a 3-variable potential missing one edge is rejected."""
        mrf = MarkovRandomField()
        for var in (rain, sprinkler, cloudy):
            mrf.add_variable(var)
        mrf.add_edge(rain, sprinkler)
        mrf.add_edge(sprinkler, cloudy)
        # rain-cloudy edge is missing: {rain, sprinkler, cloudy} is not a clique.
        table = {
            (r, s, c): 1.0
            for r in rain.domain
            for s in sprinkler.domain
            for c in cloudy.domain
        }
        with pytest.raises(ValueError, match="not a clique"):
            mrf.add_factor(Factor((rain, sprinkler, cloudy), table))

    def test_add_factor_over_full_triangle_clique_succeeds(
        self,
        rain: RandomVariable,
        sprinkler: RandomVariable,
        cloudy: RandomVariable,
    ) -> None:
        """Test that a 3-variable potential over a full triangle is accepted."""
        mrf = MarkovRandomField()
        for var in (rain, sprinkler, cloudy):
            mrf.add_variable(var)
        mrf.add_edge(rain, sprinkler)
        mrf.add_edge(sprinkler, cloudy)
        mrf.add_edge(cloudy, rain)
        table = {
            (r, s, c): 1.0
            for r in rain.domain
            for s in sprinkler.domain
            for c in cloudy.domain
        }
        potential = Factor((rain, sprinkler, cloudy), table)
        mrf.add_factor(potential)
        assert list(mrf.factors()) == [potential]

    def test_factors_for_returns_only_matching_factors(
        self,
        rain: RandomVariable,
        sprinkler: RandomVariable,
        cloudy: RandomVariable,
        binary_cpt_table: dict,
    ) -> None:
        """Test that factors_for() filters by scope membership."""
        mrf = MarkovRandomField()
        for var in (rain, sprinkler, cloudy):
            mrf.add_variable(var)
        mrf.add_edge(rain, sprinkler)
        mrf.add_edge(sprinkler, cloudy)

        rain_sprinkler = Factor((rain, sprinkler), binary_cpt_table)
        sprinkler_cloudy_table = {
            (s, c): 1.0 for s in sprinkler.domain for c in cloudy.domain
        }
        sprinkler_cloudy = Factor((sprinkler, cloudy), sprinkler_cloudy_table)
        mrf.add_factor(rain_sprinkler)
        mrf.add_factor(sprinkler_cloudy)

        assert list(mrf.factors_for(rain)) == [rain_sprinkler]
        assert set(mrf.factors_for(sprinkler)) == {rain_sprinkler, sprinkler_cloudy}
        assert list(mrf.factors_for(cloudy)) == [sprinkler_cloudy]

    def test_factors_for_unknown_variable_raises(self, rain: RandomVariable) -> None:
        """Test that factors_for() on an unregistered variable raises."""
        mrf = MarkovRandomField()
        with pytest.raises(ValueError, match="not in the field"):
            list(mrf.factors_for(rain))


class TestJoint:
    """Test joint() potential evaluation."""

    def test_joint_multiplies_single_factor(
        self,
        rain: RandomVariable,
        sprinkler: RandomVariable,
        binary_cpt_table: dict,
    ) -> None:
        """Test joint() returns the raw (unnormalized) potential value."""
        mrf = MarkovRandomField()
        mrf.add_variable(rain)
        mrf.add_variable(sprinkler)
        mrf.add_edge(rain, sprinkler)
        mrf.add_factor(Factor((rain, sprinkler), binary_cpt_table))

        assert mrf.joint({rain: "true", sprinkler: "false"}) == pytest.approx(0.99)

    def test_joint_multiplies_across_multiple_factors(
        self,
        rain: RandomVariable,
        sprinkler: RandomVariable,
        cloudy: RandomVariable,
    ) -> None:
        """Test joint() multiplies every attached potential together."""
        mrf = MarkovRandomField()
        for var in (rain, sprinkler, cloudy):
            mrf.add_variable(var)
        mrf.add_edge(rain, sprinkler)
        mrf.add_edge(sprinkler, cloudy)

        mrf.add_factor(
            Factor(
                (rain, sprinkler),
                {
                    ("true", "true"): 2.0,
                    ("true", "false"): 3.0,
                    ("false", "true"): 1.0,
                    ("false", "false"): 1.0,
                },
            )
        )
        mrf.add_factor(
            Factor(
                (sprinkler, cloudy),
                {
                    ("true", "true"): 5.0,
                    ("true", "false"): 1.0,
                    ("false", "true"): 1.0,
                    ("false", "false"): 1.0,
                },
            )
        )

        assignment = {rain: "true", sprinkler: "true", cloudy: "true"}
        assert mrf.joint(assignment) == pytest.approx(2.0 * 5.0)

    def test_joint_is_one_with_no_factors(
        self, rain: RandomVariable, sprinkler: RandomVariable
    ) -> None:
        """Test that an empty product (no factors attached) evaluates to 1.0."""
        mrf = MarkovRandomField()
        mrf.add_variable(rain)
        mrf.add_variable(sprinkler)
        assert mrf.joint({rain: "true", sprinkler: "false"}) == 1.0

    def test_joint_does_not_require_full_coverage(
        self, rain: RandomVariable, sprinkler: RandomVariable
    ) -> None:
        """Test that joint() does not require every variable to have a factor
        (unlike BayesianNetwork.joint, which raises on missing CPTs)."""
        mrf = MarkovRandomField()
        mrf.add_variable(rain)
        mrf.add_variable(sprinkler)  # never referenced by any factor
        mrf.add_factor(Factor((rain,), {("true",): 0.4, ("false",): 0.6}))

        # sprinkler's state is irrelevant since no factor mentions it.
        result = mrf.joint({rain: "true", sprinkler: "false"})
        assert result == pytest.approx(0.4)


class TestClearAndRepr:
    """Test clear() and __repr__."""

    def test_clear_resets_everything(
        self,
        rain: RandomVariable,
        sprinkler: RandomVariable,
        binary_cpt_table: dict,
    ) -> None:
        """Test that clear() removes variables, edges and factors."""
        mrf = MarkovRandomField()
        mrf.add_variable(rain)
        mrf.add_variable(sprinkler)
        mrf.add_edge(rain, sprinkler)
        mrf.add_factor(Factor((rain, sprinkler), binary_cpt_table))

        mrf.clear()

        assert len(mrf) == 0
        assert mrf.is_empty()
        assert list(mrf.factors()) == []

    def test_repr_contains_counts(
        self,
        rain: RandomVariable,
        sprinkler: RandomVariable,
        binary_cpt_table: dict,
    ) -> None:
        """Test that repr() surfaces variable/edge/factor counts."""
        mrf = MarkovRandomField()
        mrf.add_variable(rain)
        mrf.add_variable(sprinkler)
        mrf.add_edge(rain, sprinkler)
        mrf.add_factor(Factor((rain, sprinkler), binary_cpt_table))

        text = repr(mrf)
        assert "variables=2" in text
        assert "edges=1" in text
        assert "factors=1" in text
