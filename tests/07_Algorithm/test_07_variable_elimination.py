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

"""Tests for variable_elimination (#61, #62, #84)."""

import itertools
import math
from types import ModuleType
from typing import Any, Dict, Tuple

import pytest

from sds.algorithms.probabilistic_algorithms import variable_elimination
from sds.probabilistic import Factor, RandomVariable


def _as_dict(factor: Factor) -> Dict[Tuple[str, ...], float]:
    return {
        key: factor.value(dict(zip(factor.scope, key)))
        for key in itertools.product(*(v.domain for v in factor.scope))
    }


def _close(a: Dict[Any, float], b: Dict[Any, float]) -> bool:
    keys = set(a) | set(b)
    return all(math.isclose(a.get(k, 0.0), b.get(k, 0.0), abs_tol=1e-12) for k in keys)


class TestKnownValues:
    """Textbook results."""

    def test_alarm_burglary_given_both_calls(self, pgm: ModuleType) -> None:
        """P(B | J, M) = 0.284 (Russell & Norvig)."""
        bn, v = pgm.alarm()
        post = variable_elimination(bn, [v["B"]], {v["J"]: "true", v["M"]: "true"})
        assert round(post.value({v["B"]: "true"}), 3) == 0.284

    def test_sprinkler_rain_given_wet(self, pgm: ModuleType) -> None:
        """P(R | W) on the sprinkler network matches enumeration."""
        bn, v = pgm.sprinkler()
        post = variable_elimination(bn, [v["R"]], {v["W"]: "true"})
        expected = pgm.brute_force(bn, [v["R"]], {v["W"]: "true"})
        assert _close(_as_dict(post), expected)

    def test_prior_without_evidence(self, pgm: ModuleType) -> None:
        """Without evidence, a root's marginal is its CPT."""
        bn, v = pgm.alarm()
        post = variable_elimination(bn, [v["E"]])
        assert math.isclose(post.value({v["E"]: "true"}), 0.002)


class TestResultShape:
    """The returned factor."""

    def test_is_normalized(self, pgm: ModuleType) -> None:
        """Values sum to 1."""
        bn, v = pgm.sprinkler()
        post = variable_elimination(bn, [v["S"], v["R"]], {v["W"]: "true"})
        assert math.isclose(sum(_as_dict(post).values()), 1.0)

    def test_scope_follows_query_order(self, pgm: ModuleType) -> None:
        """The factor's scope is the query, in the order given."""
        bn, v = pgm.sprinkler()
        post = variable_elimination(bn, [v["R"], v["S"]])
        assert post.scope == (v["R"], v["S"])

    def test_model_unchanged(self, pgm: ModuleType) -> None:
        """Inference leaves the model's factors untouched."""
        bn, v = pgm.alarm()
        before = [_as_dict(f) for f in bn.factors()]
        variable_elimination(bn, [v["B"]], {v["J"]: "true"})
        assert [_as_dict(f) for f in bn.factors()] == before


class TestAgainstEnumeration:
    """Random models checked against brute-force enumeration."""

    @pytest.mark.parametrize("seed", range(25))
    def test_random_bayesian_networks(self, pgm: ModuleType, seed: int) -> None:
        """Every single-variable posterior matches, with evidence on the last."""
        bn = pgm.random_bn(seed)
        variables = list(bn.variables())
        evidence = {variables[-1]: variables[-1].domain[0]}
        for q in variables[:-1]:
            post = variable_elimination(bn, [q], evidence)
            assert _close(_as_dict(post), pgm.brute_force(bn, [q], evidence))

    @pytest.mark.parametrize("seed", range(10))
    def test_joint_query(self, pgm: ModuleType, seed: int) -> None:
        """A two-variable query matches too."""
        bn = pgm.random_bn(seed)
        variables = list(bn.variables())
        query = variables[:2]
        post = variable_elimination(bn, query)
        assert _close(_as_dict(post), pgm.brute_force(bn, query, {}))

    @pytest.mark.parametrize("seed", range(10))
    def test_markov_random_field_with_loop(self, pgm: ModuleType, seed: int) -> None:
        """Unnormalized MRF potentials are normalized correctly."""
        edges = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"), ("A", "C")]
        mrf, v = pgm.pairwise_mrf(edges, "ABCD", seed)
        evidence = {v["D"]: v["D"].domain[-1]}
        for name in "ABC":
            post = variable_elimination(mrf, [v[name]], evidence)
            assert _close(_as_dict(post), pgm.brute_force(mrf, [v[name]], evidence))

    def test_order_does_not_change_result(self, pgm: ModuleType) -> None:
        """Any valid elimination order gives the same answer."""
        bn, v = pgm.sprinkler()
        a = variable_elimination(bn, [v["W"]], order=[v["C"], v["S"], v["R"]])
        b = variable_elimination(bn, [v["W"]], order=[v["R"], v["S"], v["C"]])
        assert _close(_as_dict(a), _as_dict(b))


class TestEdgeCases:
    """Unconstrained variables and invalid calls."""

    def test_variable_without_factor_is_uniform(self) -> None:
        """A variable no factor mentions has a uniform posterior."""
        from sds.probabilistic import MarkovRandomField

        lone = RandomVariable("Lone", ("p", "q", "r"))
        other = RandomVariable("Other", ("x", "y"))
        mrf = MarkovRandomField()
        mrf.add_variable(lone)
        mrf.add_variable(other)
        mrf.add_factor(Factor((other,), {("x",): 1.0, ("y",): 3.0}))
        post = variable_elimination(mrf, [lone])
        assert all(math.isclose(p, 1 / 3) for p in _as_dict(post).values())

    def test_zero_probability_evidence(self, pgm: ModuleType) -> None:
        """Impossible evidence raises ValueError."""
        bn, v = pgm.sprinkler()
        # W is certainly false when S and R are both false.
        with pytest.raises(ValueError, match="probability zero"):
            variable_elimination(
                bn, [v["C"]], {v["S"]: "false", v["R"]: "false", v["W"]: "true"}
            )

    def test_empty_query(self, pgm: ModuleType) -> None:
        """At least one query variable is required."""
        bn, _ = pgm.alarm()
        with pytest.raises(ValueError, match="at least one"):
            variable_elimination(bn, [])

    def test_duplicate_query(self, pgm: ModuleType) -> None:
        """A variable cannot be queried twice."""
        bn, v = pgm.alarm()
        with pytest.raises(ValueError, match="twice"):
            variable_elimination(bn, [v["A"], v["A"]])

    def test_query_observed(self, pgm: ModuleType) -> None:
        """A query variable cannot also be observed."""
        bn, v = pgm.alarm()
        with pytest.raises(ValueError, match="also observed"):
            variable_elimination(bn, [v["A"]], {v["A"]: "true"})

    def test_unknown_variable(self, pgm: ModuleType) -> None:
        """Variables outside the model are rejected."""
        bn, _ = pgm.alarm()
        with pytest.raises(ValueError, match="not a variable"):
            variable_elimination(bn, [RandomVariable("X", ("a", "b"))])

    def test_unknown_state(self, pgm: ModuleType) -> None:
        """Evidence states must belong to the domain."""
        bn, v = pgm.alarm()
        with pytest.raises(ValueError):
            variable_elimination(bn, [v["B"]], {v["J"]: "maybe"})

    def test_bad_order(self, pgm: ModuleType) -> None:
        """An order must list exactly the hidden variables."""
        bn, v = pgm.sprinkler()
        with pytest.raises(ValueError, match="hidden variable"):
            variable_elimination(bn, [v["W"]], order=[v["C"], v["S"]])
