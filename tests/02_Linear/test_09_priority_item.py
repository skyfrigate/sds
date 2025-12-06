"""
This test_08_priority_item test file is used in sds to test functions, classes and methods with pytest library.

Created 29/11/2025
"""

import pytest

from sds.linear.queue import PriorityItem


@pytest.fixture
def priority_item_list():
    pl = []
    for data, priority in [
        ("Check email", 3.1),
        ("Fix critical bug", 1),
        ("Write documentation", 5),
        ("Code review", 2.5756),
    ]:
        pl.append(PriorityItem(data, priority))
    return pl


class TestPriorityItemCreation:
    """Tests PriorityItem creation."""

    @pytest.mark.parametrize(
        "data, priority",
        [
            ("Check email", 3.1),
            ("Fix critical bug", 1),
            ("Write documentation", 5),
            ("Code review", 2.5756),
        ],
    )
    def test_priority_item_creation(self, data, priority):
        """Tests PriorityItem creation."""
        priority_item = PriorityItem(data, priority)
        assert priority_item.data == data
        assert priority_item.priority == priority

    @pytest.mark.parametrize(
        "index, str_repr, str_expr",
        [
            (
                0,
                "PriorityItem(data='Check email', priority=3.1)",
                "Check email (priority: 3.1)",
            ),
            (
                1,
                "PriorityItem(data='Fix critical bug', priority=1)",
                "Fix critical bug (priority: 1)",
            ),
        ],
    )
    def test_priority_item_string(self, priority_item_list, index, str_repr, str_expr):
        """Tests PriorityItem repr."""
        assert repr(priority_item_list[index]) == str_repr
        assert str(priority_item_list[index]) == str_expr


class TestPriorityItemComparison:
    """Tests for PriorityItem comparison methods."""

    def test_priority_item_comparisons(self, priority_item_list):
        """Test that PriorityItem supports comparison operators."""
        item1 = PriorityItem("Low", 5)
        item2 = PriorityItem("High", 1)
        item3 = PriorityItem("Medium", 3)

        assert item2 < item3 < item1
        assert item1 > item3 > item2
        assert item2 <= item3
        assert item1 >= item3

        item4 = PriorityItem("Also High", 1)
        assert item2 == item4

    def test_priority_item_comparisons_not_implemented(self, priority_item_list):
        item = priority_item_list[0]

        with pytest.raises(NotImplementedError):
            item > 2

        with pytest.raises(NotImplementedError):
            item < 1

        with pytest.raises(NotImplementedError):
            item <= 0

        with pytest.raises(NotImplementedError):
            item >= 0

        with pytest.raises(NotImplementedError):
            item != 0

        with pytest.raises(NotImplementedError):
            item == 2
