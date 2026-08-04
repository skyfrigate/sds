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

"""Unit tests for BayesianNetwork."""

import pytest

from sds.probabilistic.bayesian_network import BayesianNetwork
from sds.probabilistic.factor import Factor
from sds.probabilistic.interfaces import AbstractBayesianNetwork
from sds.probabilistic.variable import RandomVariable


class TestBayesianNetworkCreation:
    """Test BayesianNetwork construction."""

    def test_empty_network(self) -> None:
        """Test that a new network is empty."""
        bn = BayesianNetwork()
        assert len(bn) == 0
        assert bn.is_empty()

    def test_satisfies_abstract_interface(self) -> None:
        """Test that BayesianNetwork is an AbstractBayesianNetwork."""
        assert isinstance(BayesianNetwork(), AbstractBayesianNetwork)


class TestVariableManagement:
    """Test variable registration on BayesianNetwork."""

    def test_add_variable(self, rain: RandomVariable) -> None:
        """Test adding a variable increases the network size."""
        bn = BayesianNetwork()
        bn.add_variable(rain)
        assert len(bn) == 1
        assert not bn.is_empty()

    def test_add_duplicate_variable_raises(self, rain: RandomVariable) -> None:
        """Test that re-adding the same variable name raises ValueError."""
        bn = BayesianNetwork()
        bn.add_variable(rain)
        with pytest.raises(ValueError, match="already exists"):
            bn.add_variable(RandomVariable("Rain", ("true", "false")))

    def test_has_variable(
        self, rain: RandomVariable, sprinkler: RandomVariable
    ) -> None:
        """Test has_variable distinguishes registered from unregistered variables."""
        bn = BayesianNetwork()
        bn.add_variable(rain)
        assert bn.has_variable(rain) is True
        assert bn.has_variable(sprinkler) is False

    def test_get_variable(self, rain: RandomVariable) -> None:
        """Test retrieving a variable by name."""
        bn = BayesianNetwork()
        bn.add_variable(rain)
        assert bn.get_variable("Rain") == rain

    def test_get_unknown_variable_raises_key_error(self) -> None:
        """Test that get_variable on an unknown name raises KeyError."""
        bn = BayesianNetwork()
        with pytest.raises(KeyError):
            bn.get_variable("Unknown")

    def test_variables_iteration(
        self, rain: RandomVariable, sprinkler: RandomVariable
    ) -> None:
        """Test iterating over all registered variables."""
        bn = BayesianNetwork()
        bn.add_variable(rain)
        bn.add_variable(sprinkler)
        assert set(bn.variables()) == {rain, sprinkler}

    def test_contains_and_iter(
        self, rain: RandomVariable, sprinkler: RandomVariable
    ) -> None:
        """Test __contains__ and __iter__ Collection semantics."""
        bn = BayesianNetwork()
        bn.add_variable(rain)
        assert rain in bn
        assert sprinkler not in bn
        assert list(bn) == [rain]

    def test_contains_rejects_non_variable(self, rain: RandomVariable) -> None:
        """Test that __contains__ returns False for non-RandomVariable objects."""
        bn = BayesianNetwork()
        bn.add_variable(rain)
        assert "Rain" not in bn


class TestEdgeManagement:
    """Test add_edge and DAG topology enforcement."""

    def test_add_edge(self, rain: RandomVariable, sprinkler: RandomVariable) -> None:
        """Test adding a valid directed edge."""
        bn = BayesianNetwork()
        bn.add_variable(rain)
        bn.add_variable(sprinkler)
        bn.add_edge(rain, sprinkler)
        assert list(bn.children(rain)) == [sprinkler]
        assert list(bn.parents(sprinkler)) == [rain]

    def test_add_edge_unknown_parent_raises(
        self, rain: RandomVariable, sprinkler: RandomVariable
    ) -> None:
        """Test that referencing an unregistered parent raises ValueError."""
        bn = BayesianNetwork()
        bn.add_variable(sprinkler)
        with pytest.raises(ValueError, match="not in the network"):
            bn.add_edge(rain, sprinkler)

    def test_add_edge_unknown_child_raises(
        self, rain: RandomVariable, sprinkler: RandomVariable
    ) -> None:
        """Test that referencing an unregistered child raises ValueError."""
        bn = BayesianNetwork()
        bn.add_variable(rain)
        with pytest.raises(ValueError, match="not in the network"):
            bn.add_edge(rain, sprinkler)

    def test_self_loop_raises(self, rain: RandomVariable) -> None:
        """Test that a variable cannot be its own parent."""
        bn = BayesianNetwork()
        bn.add_variable(rain)
        with pytest.raises(ValueError, match="Self-loop"):
            bn.add_edge(rain, rain)

    def test_two_node_cycle_raises(
        self, rain: RandomVariable, sprinkler: RandomVariable
    ) -> None:
        """Test that a direct A->B, B->A cycle is rejected."""
        bn = BayesianNetwork()
        bn.add_variable(rain)
        bn.add_variable(sprinkler)
        bn.add_edge(rain, sprinkler)
        with pytest.raises(ValueError, match="cycle"):
            bn.add_edge(sprinkler, rain)

    def test_two_node_cycle_does_not_corrupt_state(
        self, rain: RandomVariable, sprinkler: RandomVariable
    ) -> None:
        """Test that a rejected cycle-forming edge is rolled back."""
        bn = BayesianNetwork()
        bn.add_variable(rain)
        bn.add_variable(sprinkler)
        bn.add_edge(rain, sprinkler)
        with pytest.raises(ValueError, match="cycle"):
            bn.add_edge(sprinkler, rain)
        assert bn.is_acyclic() is True
        assert list(bn.parents(rain)) == []

    def test_three_node_cycle_raises(
        self,
        rain: RandomVariable,
        sprinkler: RandomVariable,
        wet_grass: RandomVariable,
    ) -> None:
        """Test that a longer A->B->C->A cycle is rejected."""
        bn = BayesianNetwork()
        for var in (rain, sprinkler, wet_grass):
            bn.add_variable(var)
        bn.add_edge(rain, sprinkler)
        bn.add_edge(sprinkler, wet_grass)
        with pytest.raises(ValueError, match="cycle"):
            bn.add_edge(wet_grass, rain)

    def test_duplicate_edge_raises(
        self, rain: RandomVariable, sprinkler: RandomVariable
    ) -> None:
        """Test that adding the same edge twice raises ValueError."""
        bn = BayesianNetwork()
        bn.add_variable(rain)
        bn.add_variable(sprinkler)
        bn.add_edge(rain, sprinkler)
        with pytest.raises(ValueError):
            bn.add_edge(rain, sprinkler)

    def test_multiple_parents(
        self,
        rain: RandomVariable,
        sprinkler: RandomVariable,
        wet_grass: RandomVariable,
    ) -> None:
        """Test a variable can have more than one parent."""
        bn = BayesianNetwork()
        for var in (rain, sprinkler, wet_grass):
            bn.add_variable(var)
        bn.add_edge(rain, wet_grass)
        bn.add_edge(sprinkler, wet_grass)
        assert set(bn.parents(wet_grass)) == {rain, sprinkler}

    def test_root_variable_has_no_parents(self, rain: RandomVariable) -> None:
        """Test that a variable with no incoming edges has an empty parent set."""
        bn = BayesianNetwork()
        bn.add_variable(rain)
        assert list(bn.parents(rain)) == []

    def test_leaf_variable_has_no_children(
        self, rain: RandomVariable, sprinkler: RandomVariable
    ) -> None:
        """Test that a variable with no outgoing edges has an empty child set."""
        bn = BayesianNetwork()
        bn.add_variable(rain)
        bn.add_variable(sprinkler)
        bn.add_edge(rain, sprinkler)
        assert list(bn.children(sprinkler)) == []


class TestConditionalProbabilityTables:
    """Test set_cpt validation and storage."""

    def test_set_cpt_for_root_variable(self, rain: RandomVariable) -> None:
        """Test setting a marginal (parent-less) CPT."""
        bn = BayesianNetwork()
        bn.add_variable(rain)
        bn.set_cpt(rain, Factor((rain,), {("true",): 0.2, ("false",): 0.8}))
        assert bn.get_cpt(rain).scope == (rain,)

    def test_set_cpt_for_variable_with_parent(
        self,
        rain: RandomVariable,
        sprinkler: RandomVariable,
        binary_cpt_table: dict,
    ) -> None:
        """Test setting a CPT for a variable with one parent."""
        bn = BayesianNetwork()
        bn.add_variable(rain)
        bn.add_variable(sprinkler)
        bn.add_edge(rain, sprinkler)

        sprinkler_table = {
            (s, r): binary_cpt_table[(r, s)]
            for r in rain.domain
            for s in sprinkler.domain
        }
        bn.set_cpt(sprinkler, Factor((sprinkler, rain), sprinkler_table))
        assert bn.get_cpt(sprinkler).scope == (sprinkler, rain)

    def test_set_cpt_unknown_variable_raises(self, rain: RandomVariable) -> None:
        """Test that setting a CPT for an unregistered variable raises."""
        bn = BayesianNetwork()
        with pytest.raises(ValueError, match="not in the network"):
            bn.set_cpt(rain, Factor((rain,), {("true",): 0.2, ("false",): 0.8}))

    def test_set_cpt_wrong_leading_variable_raises(
        self, rain: RandomVariable, sprinkler: RandomVariable
    ) -> None:
        """Test that a CPT whose scope doesn't start with the target variable raises."""
        bn = BayesianNetwork()
        bn.add_variable(rain)
        bn.add_variable(sprinkler)
        bn.add_edge(rain, sprinkler)
        wrong_scope_factor = Factor(
            (rain, sprinkler),
            {
                ("true", "true"): 0.01,
                ("true", "false"): 0.99,
                ("false", "true"): 0.4,
                ("false", "false"): 0.6,
            },
        )
        with pytest.raises(ValueError, match="must start with"):
            bn.set_cpt(sprinkler, wrong_scope_factor)

    def test_set_cpt_missing_parent_in_scope_raises(
        self, rain: RandomVariable, sprinkler: RandomVariable
    ) -> None:
        """Test that a CPT omitting a real parent from its scope raises."""
        bn = BayesianNetwork()
        bn.add_variable(rain)
        bn.add_variable(sprinkler)
        bn.add_edge(rain, sprinkler)
        no_parent_factor = Factor((sprinkler,), {("true",): 0.3, ("false",): 0.7})
        with pytest.raises(ValueError, match="parents"):
            bn.set_cpt(sprinkler, no_parent_factor)

    def test_set_cpt_extra_variable_in_scope_raises(
        self, rain: RandomVariable, sprinkler: RandomVariable
    ) -> None:
        """Test that a CPT scope naming a non-parent variable raises."""
        bn = BayesianNetwork()
        bn.add_variable(rain)
        bn.add_variable(sprinkler)
        # No edge added: sprinkler has no parents.
        factor_with_unrelated_scope = Factor(
            (sprinkler, rain),
            {
                ("true", "true"): 0.3,
                ("true", "false"): 0.3,
                ("false", "true"): 0.7,
                ("false", "false"): 0.7,
            },
        )
        with pytest.raises(ValueError, match="parents"):
            bn.set_cpt(sprinkler, factor_with_unrelated_scope)

    def test_set_cpt_not_normalized_raises(self, rain: RandomVariable) -> None:
        """Test that a CPT not summing to 1 per parent configuration raises."""
        bn = BayesianNetwork()
        bn.add_variable(rain)
        bad_factor = Factor((rain,), {("true",): 0.5, ("false",): 0.9})
        with pytest.raises(ValueError, match="not normalized"):
            bn.set_cpt(rain, bad_factor)

    def test_set_cpt_normalization_checked_per_parent_configuration(
        self,
        rain: RandomVariable,
        sprinkler: RandomVariable,
        binary_cpt_table: dict,
    ) -> None:
        """Test that normalization is required for every parent config, not just one."""
        bn = BayesianNetwork()
        bn.add_variable(rain)
        bn.add_variable(sprinkler)
        bn.add_edge(rain, sprinkler)

        # Correct for rain=true, broken for rain=false.
        broken_table = {
            ("true", "true"): 0.01,
            ("false", "true"): 0.99,
            ("true", "false"): 0.5,
            ("false", "false"): 0.9,  # sums to 1.4, not 1.0
        }
        with pytest.raises(ValueError, match="not normalized"):
            bn.set_cpt(sprinkler, Factor((sprinkler, rain), broken_table))

    def test_add_factor_delegates_to_set_cpt(self, rain: RandomVariable) -> None:
        """Test that add_factor infers the variable from scope[0]."""
        bn = BayesianNetwork()
        bn.add_variable(rain)
        bn.add_factor(Factor((rain,), {("true",): 0.2, ("false",): 0.8}))
        assert bn.get_cpt(rain).value({rain: "true"}) == 0.2

    def test_factors_iterates_all_cpts(
        self, rain: RandomVariable, sprinkler: RandomVariable
    ) -> None:
        """Test that factors() yields every CPT that was set."""
        bn = BayesianNetwork()
        bn.add_variable(rain)
        bn.add_variable(sprinkler)
        bn.set_cpt(rain, Factor((rain,), {("true",): 0.2, ("false",): 0.8}))
        bn.set_cpt(sprinkler, Factor((sprinkler,), {("true",): 0.3, ("false",): 0.7}))
        assert len(list(bn.factors())) == 2

    def test_get_cpt_unknown_raises_key_error(self, rain: RandomVariable) -> None:
        """Test that get_cpt on a variable without a CPT raises KeyError."""
        bn = BayesianNetwork()
        bn.add_variable(rain)
        with pytest.raises(KeyError):
            bn.get_cpt(rain)

    def test_factors_for_includes_own_cpt(self, rain: RandomVariable) -> None:
        """Test that factors_for() includes the variable's own CPT."""
        bn = BayesianNetwork()
        bn.add_variable(rain)
        rain_cpt = Factor((rain,), {("true",): 0.2, ("false",): 0.8})
        bn.set_cpt(rain, rain_cpt)
        assert list(bn.factors_for(rain)) == [rain_cpt]

    def test_factors_for_includes_children_cpts_referencing_it(
        self,
        rain: RandomVariable,
        sprinkler: RandomVariable,
        binary_cpt_table: dict,
    ) -> None:
        """Test that factors_for(parent) also returns children's CPTs.

        This is the behavior that distinguishes factors_for() from
        get_cpt(): Rain's own CPT does not mention Sprinkler, but
        Sprinkler's CPT does mention Rain (as a parent), so
        factors_for(rain) must return both.
        """
        bn = BayesianNetwork()
        bn.add_variable(rain)
        bn.add_variable(sprinkler)
        bn.add_edge(rain, sprinkler)

        rain_cpt = Factor((rain,), {("true",): 0.2, ("false",): 0.8})
        sprinkler_table = {
            (s, r): binary_cpt_table[(r, s)]
            for r in rain.domain
            for s in sprinkler.domain
        }
        sprinkler_cpt = Factor((sprinkler, rain), sprinkler_table)
        bn.set_cpt(rain, rain_cpt)
        bn.set_cpt(sprinkler, sprinkler_cpt)

        assert set(bn.factors_for(rain)) == {rain_cpt, sprinkler_cpt}
        assert set(bn.factors_for(sprinkler)) == {sprinkler_cpt}

    def test_factors_for_unknown_variable_raises(self, rain: RandomVariable) -> None:
        """Test that factors_for() on an unregistered variable raises."""
        bn = BayesianNetwork()
        with pytest.raises(ValueError, match="not in the network"):
            list(bn.factors_for(rain))

    def test_factors_for_empty_before_any_cpt_set(self, rain: RandomVariable) -> None:
        """Test that factors_for() yields nothing before any CPT is set."""
        bn = BayesianNetwork()
        bn.add_variable(rain)
        assert list(bn.factors_for(rain)) == []


class TestJoint:
    """Test joint() probability evaluation."""

    def test_joint_two_variables(
        self,
        rain: RandomVariable,
        sprinkler: RandomVariable,
        binary_cpt_table: dict,
    ) -> None:
        """Test joint() multiplies parent and child CPTs correctly."""
        bn = BayesianNetwork()
        bn.add_variable(rain)
        bn.add_variable(sprinkler)
        bn.add_edge(rain, sprinkler)
        bn.set_cpt(rain, Factor((rain,), {("true",): 0.2, ("false",): 0.8}))
        sprinkler_table = {
            (s, r): binary_cpt_table[(r, s)]
            for r in rain.domain
            for s in sprinkler.domain
        }
        bn.set_cpt(sprinkler, Factor((sprinkler, rain), sprinkler_table))

        result = bn.joint({rain: "true", sprinkler: "false"})
        assert result == pytest.approx(0.2 * 0.99)

    def test_joint_three_variables_multiple_parents(
        self,
        rain: RandomVariable,
        sprinkler: RandomVariable,
        wet_grass: RandomVariable,
    ) -> None:
        """Test joint() over a network with a two-parent node (WetGrass)."""
        bn = BayesianNetwork()
        for var in (rain, sprinkler, wet_grass):
            bn.add_variable(var)
        bn.add_edge(rain, wet_grass)
        bn.add_edge(sprinkler, wet_grass)

        bn.set_cpt(rain, Factor((rain,), {("true",): 0.2, ("false",): 0.8}))
        bn.set_cpt(sprinkler, Factor((sprinkler,), {("true",): 0.3, ("false",): 0.7}))
        wet_grass_table = {
            ("true", "true", "true"): 0.99,
            ("false", "true", "true"): 0.01,
            ("true", "true", "false"): 0.9,
            ("false", "true", "false"): 0.1,
            ("true", "false", "true"): 0.9,
            ("false", "false", "true"): 0.1,
            ("true", "false", "false"): 0.0,
            ("false", "false", "false"): 1.0,
        }
        bn.set_cpt(wet_grass, Factor((wet_grass, rain, sprinkler), wet_grass_table))

        assignment = {rain: "true", sprinkler: "true", wet_grass: "true"}
        expected = 0.2 * 0.3 * 0.99
        assert bn.joint(assignment) == pytest.approx(expected)

    def test_joint_missing_cpt_raises(
        self, rain: RandomVariable, sprinkler: RandomVariable
    ) -> None:
        """Test that joint() refuses to compute with an incomplete network."""
        bn = BayesianNetwork()
        bn.add_variable(rain)
        bn.add_variable(sprinkler)
        bn.add_edge(rain, sprinkler)
        bn.set_cpt(rain, Factor((rain,), {("true",): 0.2, ("false",): 0.8}))
        # Sprinkler's CPT was never set.
        with pytest.raises(ValueError, match="missing CPT"):
            bn.joint({rain: "true", sprinkler: "false"})


class TestClearAndRepr:
    """Test clear() and __repr__."""

    def test_clear_resets_everything(
        self,
        rain: RandomVariable,
        sprinkler: RandomVariable,
        binary_cpt_table: dict,
    ) -> None:
        """Test that clear() removes variables, edges and CPTs."""
        bn = BayesianNetwork()
        bn.add_variable(rain)
        bn.add_variable(sprinkler)
        bn.add_edge(rain, sprinkler)
        bn.set_cpt(rain, Factor((rain,), {("true",): 0.2, ("false",): 0.8}))

        bn.clear()

        assert len(bn) == 0
        assert bn.is_empty()
        assert list(bn.factors()) == []

    def test_repr_contains_counts(
        self, rain: RandomVariable, sprinkler: RandomVariable
    ) -> None:
        """Test that repr() surfaces variable/edge/cpt counts."""
        bn = BayesianNetwork()
        bn.add_variable(rain)
        bn.add_variable(sprinkler)
        bn.add_edge(rain, sprinkler)
        bn.set_cpt(rain, Factor((rain,), {("true",): 0.2, ("false",): 0.8}))

        text = repr(bn)
        assert "variables=2" in text
        assert "edges=1" in text
        assert "cpts=1" in text
