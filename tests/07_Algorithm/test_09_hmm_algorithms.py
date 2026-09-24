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

"""Tests for the HMM algorithms forward and viterbi (#61, #62, #84)."""

import itertools
import math
import random
from types import ModuleType
from typing import Dict, List, Tuple

import pytest

from sds.algorithms.probabilistic_algorithms import forward, viterbi
from sds.probabilistic import Factor, HiddenMarkovModel, RandomVariable


def _sequences(hmm: HiddenMarkovModel, length: int) -> List[Tuple[str, ...]]:
    return list(itertools.product(hmm.states().domain, repeat=length))


def _brute_likelihood(hmm: HiddenMarkovModel, obs: List[str]) -> float:
    return sum(hmm.joint(list(s), obs) for s in _sequences(hmm, len(obs)))


def _brute_filtered(hmm: HiddenMarkovModel, obs: List[str], t: int) -> Dict[str, float]:
    prefix = obs[: t + 1]
    weights: Dict[str, float] = {s: 0.0 for s in hmm.states().domain}
    for seq in _sequences(hmm, len(prefix)):
        weights[seq[-1]] += hmm.joint(list(seq), prefix)
    total = sum(weights.values())
    return {s: w / total for s, w in weights.items()}


def _random_observations(hmm: HiddenMarkovModel, seed: int) -> List[str]:
    rng = random.Random(seed)
    return [rng.choice(hmm.observations().domain) for _ in range(rng.randint(1, 6))]


class TestForward:
    """Log-likelihood and filtered distributions."""

    def test_umbrella_filtering(self, pgm: ModuleType) -> None:
        """Russell & Norvig: P(Rain_2 | u1, u2) = 0.883."""
        hmm, weather = pgm.umbrella()
        _, filtered = forward(hmm, ["yes", "yes"])
        assert round(filtered[0].value({weather: "rain"}), 3) == 0.818
        assert round(filtered[1].value({weather: "rain"}), 3) == 0.883

    @pytest.mark.parametrize("seed", range(30))
    def test_random_against_enumeration(self, pgm: ModuleType, seed: int) -> None:
        """Likelihood and every filtered distribution match brute force."""
        hmm = pgm.random_hmm(seed)
        obs = _random_observations(hmm, seed)
        likelihood = _brute_likelihood(hmm, obs)
        if likelihood == 0.0:
            with pytest.raises(ValueError, match="probability zero"):
                forward(hmm, obs)
            return
        log_p, filtered = forward(hmm, obs)
        assert math.isclose(log_p, math.log(likelihood), rel_tol=1e-9)
        states = hmm.states()
        for t, factor in enumerate(filtered):
            expected = _brute_filtered(hmm, obs, t)
            for s in states.domain:
                assert math.isclose(
                    factor.value({states: s}), expected[s], abs_tol=1e-12
                )

    def test_one_factor_per_step(self, pgm: ModuleType) -> None:
        """One normalized factor over the state variable per observation."""
        hmm, weather = pgm.umbrella()
        _, filtered = forward(hmm, ["yes", "no", "yes"])
        assert len(filtered) == 3
        for factor in filtered:
            assert factor.scope == (weather,)
            assert math.isclose(
                sum(factor.value({weather: s}) for s in weather.domain), 1.0
            )

    def test_long_sequence_no_underflow(self, pgm: ModuleType) -> None:
        """Scaling keeps a 5000-step sequence finite."""
        hmm, _ = pgm.umbrella()
        obs = ["yes", "no"] * 2500
        log_p, filtered = forward(hmm, obs)
        assert math.isfinite(log_p) and log_p < -1000
        assert math.exp(log_p) == 0.0  # the raw likelihood would underflow
        assert len(filtered) == 5000


class TestViterbi:
    """Most likely state path."""

    def test_umbrella_path(self, pgm: ModuleType) -> None:
        """The classic five-day umbrella sequence."""
        hmm, _ = pgm.umbrella()
        path, log_p = viterbi(hmm, ["yes", "yes", "no", "yes", "yes"])
        assert path == ["rain", "rain", "sun", "rain", "rain"]
        assert math.isclose(
            math.exp(log_p), hmm.joint(path, ["yes", "yes", "no", "yes", "yes"])
        )

    @pytest.mark.parametrize("seed", range(30))
    def test_random_against_enumeration(self, pgm: ModuleType, seed: int) -> None:
        """The path is a maximizer of the joint probability."""
        hmm = pgm.random_hmm(seed)
        obs = _random_observations(hmm, seed)
        scores = {s: hmm.joint(list(s), obs) for s in _sequences(hmm, len(obs))}
        best = max(scores.values())
        if best == 0.0:
            with pytest.raises(ValueError, match="probability zero"):
                viterbi(hmm, obs)
            return
        path, log_p = viterbi(hmm, obs)
        assert math.isclose(scores[tuple(path)], best, rel_tol=1e-12)
        assert math.isclose(log_p, math.log(best), rel_tol=1e-9)

    def test_ties_prefer_earlier_states(self) -> None:
        """With a fully symmetric model, the first state wins everywhere."""
        s = RandomVariable("S", ("a", "b"))
        o = RandomVariable("O", ("x", "y"))
        hmm = HiddenMarkovModel()
        hmm.set_states(s)
        hmm.set_observations(o)
        prev = hmm.previous_states()
        hmm.set_initial_distribution(Factor((s,), {("a",): 0.5, ("b",): 0.5}))
        hmm.set_transition_model(
            Factor((s, prev), {k: 0.5 for k in itertools.product("ab", "ab")})
        )
        hmm.set_emission_model(
            Factor((o, s), {k: 0.5 for k in itertools.product("xy", "ab")})
        )
        path, _ = viterbi(hmm, ["x", "y", "x"])
        assert path == ["a", "a", "a"]

    def test_long_sequence(self, pgm: ModuleType) -> None:
        """Log-domain computation handles 5000 steps."""
        hmm, _ = pgm.umbrella()
        path, log_p = viterbi(hmm, ["yes"] * 5000)
        assert path == ["rain"] * 5000
        assert math.isfinite(log_p)


@pytest.mark.parametrize("algorithm", [forward, viterbi], ids=["forward", "viterbi"])
class TestHmmArguments:
    """Argument checks shared by both algorithms."""

    def test_empty_sequence(self, pgm: ModuleType, algorithm) -> None:  # type: ignore[no-untyped-def]
        """At least one observation is required."""
        hmm, _ = pgm.umbrella()
        with pytest.raises(ValueError, match="at least one"):
            algorithm(hmm, [])

    def test_unknown_symbol(self, pgm: ModuleType, algorithm) -> None:  # type: ignore[no-untyped-def]
        """Symbols must belong to the observation domain."""
        hmm, _ = pgm.umbrella()
        with pytest.raises(ValueError):
            algorithm(hmm, ["yes", "maybe"])

    def test_unconfigured_model(self, algorithm) -> None:  # type: ignore[no-untyped-def]
        """A model without states raises ValueError."""
        with pytest.raises(ValueError):
            algorithm(HiddenMarkovModel(), ["x"])

    def test_zero_probability_sequence(self, algorithm) -> None:  # type: ignore[no-untyped-def]
        """A sequence no state can emit raises ValueError."""
        s = RandomVariable("S", ("a", "b"))
        o = RandomVariable("O", ("x", "y"))
        hmm = HiddenMarkovModel()
        hmm.set_states(s)
        hmm.set_observations(o)
        prev = hmm.previous_states()
        hmm.set_initial_distribution(Factor((s,), {("a",): 0.5, ("b",): 0.5}))
        hmm.set_transition_model(
            Factor((s, prev), {k: 0.5 for k in itertools.product("ab", "ab")})
        )
        hmm.set_emission_model(
            Factor(
                (o, s),
                {
                    ("x", "a"): 1.0,
                    ("y", "a"): 0.0,
                    ("x", "b"): 1.0,
                    ("y", "b"): 0.0,
                },
            )
        )
        with pytest.raises(ValueError, match="probability zero"):
            algorithm(hmm, ["x", "y"])
