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

"""Shared models and brute-force oracles for the inference tests.

Tests reach these builders through the ``pgm`` fixture, which returns this
module: test files cannot import a conftest directly.
"""

import itertools
import random
import sys
from types import ModuleType
from typing import Dict, List, Mapping, Sequence, Tuple

import pytest

from sds.probabilistic import (
    BayesianNetwork,
    Factor,
    HiddenMarkovModel,
    MarkovRandomField,
    RandomVariable,
)
from sds.probabilistic.interfaces import AbstractGraphicalModel

TF = ("true", "false")


def alarm() -> Tuple[BayesianNetwork, Dict[str, RandomVariable]]:
    """Pearl's burglary/earthquake network: a polytree (tree factor graph)."""
    v = {n: RandomVariable(n, TF) for n in ("B", "E", "A", "J", "M")}
    bn = BayesianNetwork()
    for var in v.values():
        bn.add_variable(var)
    for parent, child in (("B", "A"), ("E", "A"), ("A", "J"), ("A", "M")):
        bn.add_edge(v[parent], v[child])
    bn.set_cpt(v["B"], Factor((v["B"],), {("true",): 0.001, ("false",): 0.999}))
    bn.set_cpt(v["E"], Factor((v["E"],), {("true",): 0.002, ("false",): 0.998}))
    a_true = {
        ("true", "true"): 0.95,
        ("true", "false"): 0.94,
        ("false", "true"): 0.29,
        ("false", "false"): 0.001,
    }
    table = {}
    for (b, e), p in a_true.items():
        table[("true", b, e)] = p
        table[("false", b, e)] = 1 - p
    bn.set_cpt(v["A"], Factor((v["A"], v["B"], v["E"]), table))
    for name, (p_t, p_f) in (("J", (0.90, 0.05)), ("M", (0.70, 0.01))):
        bn.set_cpt(
            v[name],
            Factor(
                (v[name], v["A"]),
                {
                    ("true", "true"): p_t,
                    ("false", "true"): 1 - p_t,
                    ("true", "false"): p_f,
                    ("false", "false"): 1 - p_f,
                },
            ),
        )
    return bn, v


def sprinkler() -> Tuple[BayesianNetwork, Dict[str, RandomVariable]]:
    """Cloudy/Sprinkler/Rain/WetGrass: its factor graph has a cycle."""
    v = {n: RandomVariable(n, TF) for n in ("C", "S", "R", "W")}
    bn = BayesianNetwork()
    for var in v.values():
        bn.add_variable(var)
    for parent, child in (("C", "S"), ("C", "R"), ("S", "W"), ("R", "W")):
        bn.add_edge(v[parent], v[child])
    bn.set_cpt(v["C"], Factor((v["C"],), {("true",): 0.5, ("false",): 0.5}))
    for name, (p_t, p_f) in (("S", (0.1, 0.5)), ("R", (0.8, 0.2))):
        bn.set_cpt(
            v[name],
            Factor(
                (v[name], v["C"]),
                {
                    ("true", "true"): p_t,
                    ("false", "true"): 1 - p_t,
                    ("true", "false"): p_f,
                    ("false", "false"): 1 - p_f,
                },
            ),
        )
    w_true = {
        ("true", "true"): 0.99,
        ("true", "false"): 0.9,
        ("false", "true"): 0.9,
        ("false", "false"): 0.0,
    }
    table = {}
    for (s, r), p in w_true.items():
        table[("true", s, r)] = p
        table[("false", s, r)] = 1 - p
    bn.set_cpt(v["W"], Factor((v["W"], v["S"], v["R"]), table))
    return bn, v


def pairwise_mrf(
    edges: Sequence[Tuple[str, str]], names: str, seed: int
) -> Tuple[MarkovRandomField, Dict[str, RandomVariable]]:
    """An MRF with random positive pairwise and unary potentials."""
    rng = random.Random(seed)
    v = {n: RandomVariable(n, ("x", "y", "z")[: rng.choice((2, 3))]) for n in names}
    mrf = MarkovRandomField()
    for var in v.values():
        mrf.add_variable(var)
    for a, b in edges:
        mrf.add_edge(v[a], v[b])
    for a, b in edges:
        scope = (v[a], v[b])
        mrf.add_factor(
            Factor(
                scope,
                {
                    k: rng.uniform(0.1, 3.0)
                    for k in itertools.product(v[a].domain, v[b].domain)
                },
            )
        )
    for var in v.values():
        mrf.add_factor(
            Factor((var,), {(s,): rng.uniform(0.1, 3.0) for s in var.domain})
        )
    return mrf, v


def random_bn(seed: int) -> BayesianNetwork:
    """A random DAG over 2-6 variables with random normalized CPTs."""
    rng = random.Random(seed)
    n = rng.randint(2, 6)
    variables = [
        RandomVariable(f"V{i}", ("a", "b", "c")[: rng.choice((2, 3))]) for i in range(n)
    ]
    bn = BayesianNetwork()
    for var in variables:
        bn.add_variable(var)
    parents: Dict[RandomVariable, List[RandomVariable]] = {v: [] for v in variables}
    for j, child in enumerate(variables):
        for parent in variables[:j]:
            if rng.random() < 0.4 and len(parents[child]) < 3:
                bn.add_edge(parent, child)
                parents[child].append(parent)
    for child in variables:
        scope = (child, *parents[child])
        table = {}
        for config in itertools.product(*(p.domain for p in parents[child])):
            weights = [rng.uniform(0.05, 1.0) for _ in child.domain]
            total = sum(weights)
            for state, w in zip(child.domain, weights):
                table[(state, *config)] = w / total
        bn.set_cpt(child, Factor(scope, table))
    return bn


def brute_force(
    model: AbstractGraphicalModel,
    query: Sequence[RandomVariable],
    evidence: Mapping[RandomVariable, str],
) -> Dict[Tuple[str, ...], float]:
    """P(query | evidence) by enumerating every joint assignment."""
    variables = list(model.variables())
    scores: Dict[Tuple[str, ...], float] = {}
    for states in itertools.product(*(v.domain for v in variables)):
        assignment = dict(zip(variables, states))
        if any(assignment[k] != s for k, s in evidence.items()):
            continue
        weight = 1.0
        for factor in model.factors():
            weight *= factor.value(assignment)
        key = tuple(assignment[q] for q in query)
        scores[key] = scores.get(key, 0.0) + weight
    total = sum(scores.values())
    return {k: w / total for k, w in scores.items()}


def umbrella() -> Tuple[HiddenMarkovModel, RandomVariable]:
    """Russell & Norvig's umbrella world."""
    weather = RandomVariable("Weather", ("rain", "sun"))
    umbrella_var = RandomVariable("Umbrella", ("yes", "no"))
    hmm = HiddenMarkovModel()
    hmm.set_states(weather)
    hmm.set_observations(umbrella_var)
    prev = hmm.previous_states()
    hmm.set_initial_distribution(Factor((weather,), {("rain",): 0.5, ("sun",): 0.5}))
    hmm.set_transition_model(
        Factor(
            (weather, prev),
            {
                ("rain", "rain"): 0.7,
                ("sun", "rain"): 0.3,
                ("rain", "sun"): 0.3,
                ("sun", "sun"): 0.7,
            },
        )
    )
    hmm.set_emission_model(
        Factor(
            (umbrella_var, weather),
            {
                ("yes", "rain"): 0.9,
                ("no", "rain"): 0.1,
                ("yes", "sun"): 0.2,
                ("no", "sun"): 0.8,
            },
        )
    )
    return hmm, weather


def random_hmm(seed: int) -> HiddenMarkovModel:
    """A random HMM with 2-3 states and 2-3 symbols, some zero entries."""
    rng = random.Random(seed)
    states = RandomVariable("S", ("p", "q", "r")[: rng.choice((2, 3))])
    symbols = RandomVariable("O", ("u", "v", "w")[: rng.choice((2, 3))])
    hmm = HiddenMarkovModel()
    hmm.set_states(states)
    hmm.set_observations(symbols)
    prev = hmm.previous_states()

    def dist(n: int) -> List[float]:
        w = [rng.choice((0.0, rng.uniform(0.1, 1.0))) for _ in range(n)]
        if sum(w) == 0:
            w[rng.randrange(n)] = 1.0
        return [x / sum(w) for x in w]

    hmm.set_initial_distribution(
        Factor(
            (states,),
            {(s,): p for s, p in zip(states.domain, dist(states.cardinality))},
        )
    )
    trans = {}
    for r in states.domain:
        for s, p in zip(states.domain, dist(states.cardinality)):
            trans[(s, r)] = p
    hmm.set_transition_model(Factor((states, prev), trans))
    emit = {}
    for s in states.domain:
        for o, p in zip(symbols.domain, dist(symbols.cardinality)):
            emit[(o, s)] = p
    hmm.set_emission_model(Factor((symbols, states), emit))
    return hmm


@pytest.fixture
def pgm() -> ModuleType:
    """The builders and oracles defined in this module."""
    return sys.modules[__name__]
