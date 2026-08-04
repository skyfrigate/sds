"""Shared fixtures for the probabilistic module tests."""

import pytest

from sds.probabilistic.variable import RandomVariable

# ============================================================================
# RandomVariable Fixtures
# ============================================================================


@pytest.fixture
def rain() -> RandomVariable:
    """Binary RandomVariable: Rain in {true, false}.

    Returns
    -------
    RandomVariable
        A binary variable named "Rain".
    """
    return RandomVariable("Rain", ("true", "false"))


@pytest.fixture
def sprinkler() -> RandomVariable:
    """Binary RandomVariable: Sprinkler in {true, false}.

    Returns
    -------
    RandomVariable
        A binary variable named "Sprinkler".
    """
    return RandomVariable("Sprinkler", ("true", "false"))


@pytest.fixture
def wet_grass() -> RandomVariable:
    """Binary RandomVariable: WetGrass in {true, false}.

    Returns
    -------
    RandomVariable
        A binary variable named "WetGrass", conventionally depending on
        both Rain and Sprinkler.
    """
    return RandomVariable("WetGrass", ("true", "false"))


@pytest.fixture
def weather() -> RandomVariable:
    """Ternary RandomVariable: Weather in {sunny, rainy, cloudy}.

    Returns
    -------
    RandomVariable
        A three-state variable named "Weather".
    """
    return RandomVariable("Weather", ("sunny", "rainy", "cloudy"))


@pytest.fixture
def binary_cpt_table() -> dict[tuple[str, str], float]:
    """Complete 2x2 joint table for (Rain, Sprinkler), summing to 1.

    Returns
    -------
    dict
        Maps every (rain_state, sprinkler_state) pair to a probability.
    """
    return {
        ("true", "true"): 0.01,
        ("true", "false"): 0.99,
        ("false", "true"): 0.4,
        ("false", "false"): 0.6,
    }
