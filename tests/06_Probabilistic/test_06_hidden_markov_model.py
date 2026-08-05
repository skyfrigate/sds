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

"""Unit tests for HiddenMarkovModel."""

from typing import Callable

import pytest

from sds.probabilistic.factor import Factor
from sds.probabilistic.hidden_markov_model import HiddenMarkovModel
from sds.probabilistic.interfaces import AbstractHiddenMarkovModel
from sds.probabilistic.variable import RandomVariable


@pytest.fixture
def weather() -> RandomVariable:
    """Binary RandomVariable: Weather in {sunny, rainy} (HMM states)."""
    return RandomVariable("Weather", ("sunny", "rainy"))


@pytest.fixture
def umbrella() -> RandomVariable:
    """Binary RandomVariable: Umbrella in {yes, no} (HMM observations)."""
    return RandomVariable("Umbrella", ("yes", "no"))


@pytest.fixture
def initial_factor(weather: RandomVariable) -> Factor:
    """A valid initial distribution over Weather."""
    return Factor((weather,), {("sunny",): 0.6, ("rainy",): 0.4})


@pytest.fixture
def transition_factor(weather: RandomVariable) -> Callable[[RandomVariable], Factor]:
    """A valid transition model; scope built lazily against previous_states()."""

    def _build(previous: RandomVariable) -> Factor:
        return Factor(
            (weather, previous),
            {
                ("sunny", "sunny"): 0.7,
                ("rainy", "sunny"): 0.3,
                ("sunny", "rainy"): 0.4,
                ("rainy", "rainy"): 0.6,
            },
        )

    return _build


@pytest.fixture
def emission_factor(weather: RandomVariable, umbrella: RandomVariable) -> Factor:
    """A valid emission model over (Umbrella, Weather)."""
    return Factor(
        (umbrella, weather),
        {
            ("yes", "sunny"): 0.1,
            ("no", "sunny"): 0.9,
            ("yes", "rainy"): 0.8,
            ("no", "rainy"): 0.2,
        },
    )


class TestHiddenMarkovModelCreation:
    """Test HiddenMarkovModel construction."""

    def test_empty_model(self) -> None:
        """Test that a new model is empty."""
        hmm = HiddenMarkovModel()
        assert len(hmm) == 0
        assert hmm.is_empty()

    def test_satisfies_abstract_interface(self) -> None:
        """Test that HiddenMarkovModel is an AbstractHiddenMarkovModel."""
        assert isinstance(HiddenMarkovModel(), AbstractHiddenMarkovModel)


class TestVariableManagement:
    """Test set_states/set_observations and their getters."""

    def test_set_states(self, weather: RandomVariable) -> None:
        """Test setting the states variable."""
        hmm = HiddenMarkovModel()
        hmm.set_states(weather)
        assert hmm.states() == weather
        assert len(hmm) == 1

    def test_set_states_twice_raises(self, weather: RandomVariable) -> None:
        """Test that re-setting the states variable raises ValueError."""
        hmm = HiddenMarkovModel()
        hmm.set_states(weather)
        with pytest.raises(ValueError, match="already set"):
            hmm.set_states(RandomVariable("Weather", ("sunny", "rainy")))

    def test_states_unset_raises(self) -> None:
        """Test that states() raises before set_states() is called."""
        hmm = HiddenMarkovModel()
        with pytest.raises(ValueError, match="not been set"):
            hmm.states()

    def test_set_observations(self, umbrella: RandomVariable) -> None:
        """Test setting the observations variable."""
        hmm = HiddenMarkovModel()
        hmm.set_observations(umbrella)
        assert hmm.observations() == umbrella

    def test_set_observations_twice_raises(self, umbrella: RandomVariable) -> None:
        """Test that re-setting the observations variable raises."""
        hmm = HiddenMarkovModel()
        hmm.set_observations(umbrella)
        with pytest.raises(ValueError, match="already set"):
            hmm.set_observations(RandomVariable("Umbrella", ("yes", "no")))

    def test_observations_unset_raises(self) -> None:
        """Test that observations() raises before set_observations() is called."""
        hmm = HiddenMarkovModel()
        with pytest.raises(ValueError, match="not been set"):
            hmm.observations()

    def test_previous_states_derived_automatically(
        self, weather: RandomVariable
    ) -> None:
        """Test that previous_states() is derived when set_states() is called."""
        hmm = HiddenMarkovModel()
        hmm.set_states(weather)
        previous = hmm.previous_states()
        assert previous.domain == weather.domain
        assert previous != weather

    def test_previous_states_unset_raises(self) -> None:
        """Test that previous_states() raises before set_states() is called."""
        hmm = HiddenMarkovModel()
        with pytest.raises(ValueError, match="not been set"):
            hmm.previous_states()

    def test_contains_and_iter(
        self, weather: RandomVariable, umbrella: RandomVariable
    ) -> None:
        """Test __contains__ and __iter__ Collection semantics."""
        hmm = HiddenMarkovModel()
        hmm.set_states(weather)
        assert weather in hmm
        assert umbrella not in hmm
        assert list(hmm) == [weather]

    def test_iter_excludes_previous_states(self, weather: RandomVariable) -> None:
        """Test that __iter__ does not yield the derived previous_states()."""
        hmm = HiddenMarkovModel()
        hmm.set_states(weather)
        assert hmm.previous_states() not in list(hmm)

    def test_contains_rejects_non_variable(self, weather: RandomVariable) -> None:
        """Test that __contains__ returns False for non-RandomVariable objects."""
        hmm = HiddenMarkovModel()
        hmm.set_states(weather)
        assert "Weather" not in hmm


class TestComponentValidation:
    """Test set_initial_distribution/set_transition_model/set_emission_model."""

    def test_set_initial_distribution(
        self, weather: RandomVariable, initial_factor: Factor
    ) -> None:
        """Test assigning a valid initial distribution."""
        hmm = HiddenMarkovModel()
        hmm.set_states(weather)
        hmm.set_initial_distribution(initial_factor)
        assert hmm.initial_distribution() is initial_factor
        assert len(hmm) == 2

    def test_set_initial_distribution_before_states_raises(
        self, initial_factor: Factor
    ) -> None:
        """Test that setting the initial distribution before states() raises."""
        hmm = HiddenMarkovModel()
        with pytest.raises(ValueError, match="not been set"):
            hmm.set_initial_distribution(initial_factor)

    def test_set_initial_distribution_wrong_scope_raises(
        self, weather: RandomVariable, umbrella: RandomVariable
    ) -> None:
        """Test that an initial distribution over the wrong variable raises."""
        hmm = HiddenMarkovModel()
        hmm.set_states(weather)
        wrong = Factor((umbrella,), {("yes",): 0.5, ("no",): 0.5})
        with pytest.raises(ValueError, match="Initial distribution scope"):
            hmm.set_initial_distribution(wrong)

    def test_set_initial_distribution_not_normalized_raises(
        self, weather: RandomVariable
    ) -> None:
        """Test that a non-normalized initial distribution raises."""
        hmm = HiddenMarkovModel()
        hmm.set_states(weather)
        bad = Factor((weather,), {("sunny",): 0.5, ("rainy",): 0.9})
        with pytest.raises(ValueError, match="not normalized"):
            hmm.set_initial_distribution(bad)

    def test_initial_distribution_unset_raises(self, weather: RandomVariable) -> None:
        """Test that initial_distribution() raises before it is set."""
        hmm = HiddenMarkovModel()
        hmm.set_states(weather)
        with pytest.raises(ValueError, match="not been set"):
            hmm.initial_distribution()

    def test_set_transition_model(
        self, weather: RandomVariable, transition_factor
    ) -> None:
        """Test assigning a valid transition model using previous_states()."""
        hmm = HiddenMarkovModel()
        hmm.set_states(weather)
        factor = transition_factor(hmm.previous_states())
        hmm.set_transition_model(factor)
        assert hmm.transition_model() is factor

    def test_set_transition_model_before_states_raises(self) -> None:
        """Test that setting the transition model before states() raises."""
        hmm = HiddenMarkovModel()
        dummy_weather = RandomVariable("Weather", ("sunny", "rainy"))
        dummy_previous = RandomVariable("Weather__prev", ("sunny", "rainy"))
        factor = Factor(
            (dummy_weather, dummy_previous),
            {
                ("sunny", "sunny"): 0.7,
                ("rainy", "sunny"): 0.3,
                ("sunny", "rainy"): 0.4,
                ("rainy", "rainy"): 0.6,
            },
        )
        with pytest.raises(ValueError, match="not been set"):
            hmm.set_transition_model(factor)

    def test_set_transition_model_wrong_scope_raises(
        self, weather: RandomVariable
    ) -> None:
        """Test that a transition model with the wrong scope raises."""
        hmm = HiddenMarkovModel()
        hmm.set_states(weather)
        # Scope order reversed (previous, weather) instead of (weather, previous).
        wrong = Factor(
            (hmm.previous_states(), weather),
            {
                ("sunny", "sunny"): 0.7,
                ("sunny", "rainy"): 0.3,
                ("rainy", "sunny"): 0.4,
                ("rainy", "rainy"): 0.6,
            },
        )
        with pytest.raises(ValueError, match="Transition model scope"):
            hmm.set_transition_model(wrong)

    def test_set_transition_model_not_normalized_raises(
        self, weather: RandomVariable
    ) -> None:
        """Test that a transition model not summing to 1 per row raises."""
        hmm = HiddenMarkovModel()
        hmm.set_states(weather)
        previous = hmm.previous_states()
        bad = Factor(
            (weather, previous),
            {
                ("sunny", "sunny"): 0.7,
                ("rainy", "sunny"): 0.9,  # sums to 1.6
                ("sunny", "rainy"): 0.4,
                ("rainy", "rainy"): 0.6,
            },
        )
        with pytest.raises(ValueError, match="not normalized"):
            hmm.set_transition_model(bad)

    def test_transition_model_unset_raises(self, weather: RandomVariable) -> None:
        """Test that transition_model() raises before it is set."""
        hmm = HiddenMarkovModel()
        hmm.set_states(weather)
        with pytest.raises(ValueError, match="not been set"):
            hmm.transition_model()

    def test_set_emission_model(
        self,
        weather: RandomVariable,
        umbrella: RandomVariable,
        emission_factor: Factor,
    ) -> None:
        """Test assigning a valid emission model."""
        hmm = HiddenMarkovModel()
        hmm.set_states(weather)
        hmm.set_observations(umbrella)
        hmm.set_emission_model(emission_factor)
        assert hmm.emission_model() is emission_factor

    def test_set_emission_model_before_observations_raises(
        self, weather: RandomVariable, emission_factor: Factor
    ) -> None:
        """Test that setting the emission model before observations() raises."""
        hmm = HiddenMarkovModel()
        hmm.set_states(weather)
        with pytest.raises(ValueError, match="not been set"):
            hmm.set_emission_model(emission_factor)

    def test_set_emission_model_wrong_scope_raises(
        self, weather: RandomVariable, umbrella: RandomVariable
    ) -> None:
        """Test that an emission model with scope order reversed raises."""
        hmm = HiddenMarkovModel()
        hmm.set_states(weather)
        hmm.set_observations(umbrella)
        wrong = Factor(
            (weather, umbrella),
            {
                ("sunny", "yes"): 0.1,
                ("sunny", "no"): 0.9,
                ("rainy", "yes"): 0.8,
                ("rainy", "no"): 0.2,
            },
        )
        with pytest.raises(ValueError, match="Emission model scope"):
            hmm.set_emission_model(wrong)

    def test_set_emission_model_not_normalized_raises(
        self, weather: RandomVariable, umbrella: RandomVariable
    ) -> None:
        """Test that an emission model not summing to 1 per state raises."""
        hmm = HiddenMarkovModel()
        hmm.set_states(weather)
        hmm.set_observations(umbrella)
        bad = Factor(
            (umbrella, weather),
            {
                ("yes", "sunny"): 0.1,
                ("no", "sunny"): 0.1,  # sums to 0.2
                ("yes", "rainy"): 0.8,
                ("no", "rainy"): 0.2,
            },
        )
        with pytest.raises(ValueError, match="not normalized"):
            hmm.set_emission_model(bad)

    def test_emission_model_unset_raises(
        self, weather: RandomVariable, umbrella: RandomVariable
    ) -> None:
        """Test that emission_model() raises before it is set."""
        hmm = HiddenMarkovModel()
        hmm.set_states(weather)
        hmm.set_observations(umbrella)
        with pytest.raises(ValueError, match="not been set"):
            hmm.emission_model()


def _build_full_model(
    weather: RandomVariable,
    umbrella: RandomVariable,
    initial_factor: Factor,
    transition_factor,
    emission_factor: Factor,
) -> HiddenMarkovModel:
    """Assemble a fully configured HiddenMarkovModel for joint() tests."""
    hmm = HiddenMarkovModel()
    hmm.set_states(weather)
    hmm.set_observations(umbrella)
    hmm.set_initial_distribution(initial_factor)
    hmm.set_transition_model(transition_factor(hmm.previous_states()))
    hmm.set_emission_model(emission_factor)
    return hmm


class TestJoint:
    """Test joint() over a fully observed sequence."""

    def test_joint_single_time_step(
        self,
        weather: RandomVariable,
        umbrella: RandomVariable,
        initial_factor: Factor,
        transition_factor,
        emission_factor: Factor,
    ) -> None:
        """Test joint() with a single time step (no transition applied)."""
        hmm = _build_full_model(
            weather, umbrella, initial_factor, transition_factor, emission_factor
        )
        result = hmm.joint(["sunny"], ["no"])
        assert result == pytest.approx(0.6 * 0.9)

    def test_joint_two_time_steps(
        self,
        weather: RandomVariable,
        umbrella: RandomVariable,
        initial_factor: Factor,
        transition_factor,
        emission_factor: Factor,
    ) -> None:
        """Test joint() over two time steps matches the hand-computed value."""
        hmm = _build_full_model(
            weather, umbrella, initial_factor, transition_factor, emission_factor
        )
        result = hmm.joint(["sunny", "rainy"], ["no", "yes"])
        expected = 0.6 * 0.9 * 0.3 * 0.8
        assert result == pytest.approx(expected)

    def test_joint_three_time_steps(
        self,
        weather: RandomVariable,
        umbrella: RandomVariable,
        initial_factor: Factor,
        transition_factor,
        emission_factor: Factor,
    ) -> None:
        """Test joint() over three time steps."""
        hmm = _build_full_model(
            weather, umbrella, initial_factor, transition_factor, emission_factor
        )
        result = hmm.joint(["sunny", "sunny", "rainy"], ["no", "yes", "yes"])
        expected = 0.6 * 0.9 * 0.7 * 0.1 * 0.3 * 0.8
        assert result == pytest.approx(expected)

    def test_joint_mismatched_lengths_raises(
        self,
        weather: RandomVariable,
        umbrella: RandomVariable,
        initial_factor: Factor,
        transition_factor,
        emission_factor: Factor,
    ) -> None:
        """Test that mismatched sequence lengths raise ValueError."""
        hmm = _build_full_model(
            weather, umbrella, initial_factor, transition_factor, emission_factor
        )
        with pytest.raises(ValueError, match="same length"):
            hmm.joint(["sunny", "rainy"], ["no"])

    def test_joint_empty_sequences_raise(
        self,
        weather: RandomVariable,
        umbrella: RandomVariable,
        initial_factor: Factor,
        transition_factor,
        emission_factor: Factor,
    ) -> None:
        """Test that empty sequences raise ValueError."""
        hmm = _build_full_model(
            weather, umbrella, initial_factor, transition_factor, emission_factor
        )
        with pytest.raises(ValueError, match="at least one time step"):
            hmm.joint([], [])

    def test_joint_missing_component_raises(
        self, weather: RandomVariable, umbrella: RandomVariable
    ) -> None:
        """Test that joint() raises if a component was never configured."""
        hmm = HiddenMarkovModel()
        hmm.set_states(weather)
        hmm.set_observations(umbrella)
        with pytest.raises(ValueError, match="not been set"):
            hmm.joint(["sunny"], ["no"])


class TestClearAndRepr:
    """Test clear() and __repr__."""

    def test_clear_resets_everything(
        self,
        weather: RandomVariable,
        umbrella: RandomVariable,
        initial_factor: Factor,
        transition_factor,
        emission_factor: Factor,
    ) -> None:
        """Test that clear() removes every component, including previous_states."""
        hmm = _build_full_model(
            weather, umbrella, initial_factor, transition_factor, emission_factor
        )
        hmm.clear()

        assert len(hmm) == 0
        assert hmm.is_empty()
        with pytest.raises(ValueError, match="not been set"):
            hmm.states()
        with pytest.raises(ValueError, match="not been set"):
            hmm.previous_states()

    def test_repr_contains_configured_count(
        self, weather: RandomVariable, umbrella: RandomVariable
    ) -> None:
        """Test that repr() surfaces the configured/5 component count."""
        hmm = HiddenMarkovModel()
        hmm.set_states(weather)
        hmm.set_observations(umbrella)
        text = repr(hmm)
        assert "configured=2/5" in text
