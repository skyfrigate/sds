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

"""Tests for belief_propagation (#61, #62, #84)."""

import math
import warnings
from types import ModuleType

import pytest

from sds.algorithms.probabilistic_algorithms import (
    belief_propagation,
    variable_elimination,
)
from sds.probabilistic import Factor, MarkovRandomField, RandomVariable


def _marginal(factor: Factor) -> dict:
    variable = factor.scope[0]
    return {s: factor.value({variable: s}) for s in variable.domain}


def _exact(pgm: ModuleType, model, variable, evidence) -> dict:  # type: ignore[no-untyped-def]
    table = pgm.brute_force(model, [variable], evidence)
    return {s: table.get((s,), 0.0) for s in variable.domain}


def _assert_close(a: dict, b: dict, tol: float = 1e-9) -> None:
    for key in a:
        assert math.isclose(a[key], b[key], abs_tol=tol), (key, a[key], b[key])


class TestExactOnTrees:
    """On tree-shaped factor graphs the marginals are exact."""

    @pytest.mark.parametrize(
        "evidence_names",
        [(), ("J",), ("J", "M"), ("B",)],
        ids=["none", "J", "J+M", "B"],
    )
    def test_alarm_polytree(self, pgm: ModuleType, evidence_names: tuple) -> None:
        """Every marginal of the alarm network matches enumeration."""
        bn, v = pgm.alarm()
        evidence = {v[n]: "true" for n in evidence_names}
        marginals = belief_propagation(bn, evidence)
        for variable in bn.variables():
            if variable not in evidence:
                _assert_close(
                    _marginal(marginals[variable]), _exact(pgm, bn, variable, evidence)
                )

    def test_alarm_textbook_value(self, pgm: ModuleType) -> None:
        """P(B | J, M) = 0.284."""
        bn, v = pgm.alarm()
        marginals = belief_propagation(bn, {v["J"]: "true", v["M"]: "true"})
        assert round(marginals[v["B"]].value({v["B"]: "true"}), 3) == 0.284

    @pytest.mark.parametrize("seed", range(10))
    def test_chain_mrf(self, pgm: ModuleType, seed: int) -> None:
        """A random pairwise chain MRF is solved exactly."""
        edges = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "E")]
        mrf, v = pgm.pairwise_mrf(edges, "ABCDE", seed)
        evidence = {v["E"]: v["E"].domain[0]}
        marginals = belief_propagation(mrf, evidence)
        for name in "ABCD":
            _assert_close(
                _marginal(marginals[v[name]]), _exact(pgm, mrf, v[name], evidence)
            )

    def test_no_warning_on_tree(self, pgm: ModuleType) -> None:
        """A tree converges well within the default iteration budget."""
        bn, _ = pgm.alarm()
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            belief_propagation(bn)


class TestLoopy:
    """On factor graphs with cycles the result is approximate."""

    def test_sprinkler_approximate(self, pgm: ModuleType) -> None:
        """Loopy BP converges near, but not exactly on, the posterior.

        The cycle C-S-W-R-C makes evidence on W count twice: BP gives
        P(R | W) of about 0.784 where the exact value is about 0.708.
        """
        bn, v = pgm.sprinkler()
        evidence = {v["W"]: "true"}
        with warnings.catch_warnings():
            warnings.simplefilter("error")  # it does converge
            marginals = belief_propagation(bn, evidence)
        errors = []
        for name in "CSR":
            exact = _exact(pgm, bn, v[name], evidence)["true"]
            approx = marginals[v[name]].value({v[name]: "true"})
            errors.append(abs(exact - approx))
        assert max(errors) < 0.1
        assert max(errors) > 1e-3  # not exact: documented loopy behaviour

    def test_non_convergence_warns(self, pgm: ModuleType) -> None:
        """Too few iterations on a loopy graph emit a RuntimeWarning."""
        bn, v = pgm.sprinkler()
        with pytest.warns(RuntimeWarning, match="did not converge"):
            belief_propagation(bn, {v["W"]: "true"}, max_iterations=1)


class TestContract:
    """Result shape and argument checks."""

    def test_every_variable_present_in_model_order(self, pgm: ModuleType) -> None:
        """One normalized marginal per variable, in the model's order."""
        bn, _ = pgm.sprinkler()
        marginals = belief_propagation(bn)
        assert list(marginals) == list(bn.variables())
        for factor in marginals.values():
            assert math.isclose(sum(_marginal(factor).values()), 1.0)

    def test_observed_variable_is_point_mass(self, pgm: ModuleType) -> None:
        """An observed variable's marginal is all on the observed state."""
        bn, v = pgm.alarm()
        marginals = belief_propagation(bn, {v["A"]: "false"})
        assert _marginal(marginals[v["A"]]) == {"true": 0.0, "false": 1.0}

    def test_variable_without_factor_is_uniform(self) -> None:
        """A variable no factor mentions gets a uniform marginal."""
        lone = RandomVariable("Lone", ("p", "q", "r"))
        mrf = MarkovRandomField()
        mrf.add_variable(lone)
        marginals = belief_propagation(mrf)
        assert all(math.isclose(p, 1 / 3) for p in _marginal(marginals[lone]).values())

    def test_matches_variable_elimination_on_tree(self, pgm: ModuleType) -> None:
        """Both exact methods agree on a polytree."""
        bn, v = pgm.alarm()
        evidence = {v["M"]: "true"}
        marginals = belief_propagation(bn, evidence)
        ve = variable_elimination(bn, [v["E"]], evidence)
        assert math.isclose(
            marginals[v["E"]].value({v["E"]: "true"}), ve.value({v["E"]: "true"})
        )

    def test_zero_probability_evidence(self, pgm: ModuleType) -> None:
        """Contradictory evidence raises ValueError."""
        bn, v = pgm.sprinkler()
        with pytest.raises(ValueError, match="probability zero"):
            belief_propagation(bn, {v["S"]: "false", v["R"]: "false", v["W"]: "true"})

    def test_bad_iterations(self, pgm: ModuleType) -> None:
        """max_iterations must be positive."""
        bn, _ = pgm.alarm()
        with pytest.raises(ValueError, match="positive"):
            belief_propagation(bn, max_iterations=0)

    def test_unknown_evidence_variable(self, pgm: ModuleType) -> None:
        """Evidence on a foreign variable is rejected."""
        bn, _ = pgm.alarm()
        with pytest.raises(ValueError, match="not a variable"):
            belief_propagation(bn, {RandomVariable("X", ("a", "b")): "a"})
