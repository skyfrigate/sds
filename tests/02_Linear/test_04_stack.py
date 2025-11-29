"""Tests for Stack from sds.linear.stack module."""

import pytest

from sds.core.exceptions import EmptyStructureError
from sds.core.interfaces import LinearCollection
from sds.linear.stack import Stack


@pytest.fixture
def empty_stack():
    """Provide an empty Stack."""
    return Stack()


@pytest.fixture
def populated_stack():
    """Provide a Stack with elements [3, 2, 1] (1 on top)."""
    stack = Stack()
    stack.push(3)
    stack.push(2)
    stack.push(1)
    return stack


class TestStackCreation:
    """Tests for Stack creation and initialization."""

    def test_stack_creation(self):
        """Test creating an empty Stack."""
        stack = Stack()

        assert isinstance(stack, Stack)
        assert isinstance(stack, LinearCollection)

    def test_initial_state(self, empty_stack):
        """Test the initial state of an empty Stack."""
        assert empty_stack.is_empty() is True
        assert len(empty_stack) == 0
        assert empty_stack.size == 0


class TestStackProperties:
    """Tests for Stack properties."""

    def test_size_property(self, populated_stack):
        """Test the size property."""
        assert populated_stack.size == 3

        populated_stack.push(0)
        assert populated_stack.size == 4

        populated_stack.pop()
        assert populated_stack.size == 3

    def test_size_is_read_only(self, empty_stack):
        """Test that size property cannot be set directly."""
        with pytest.raises(AttributeError):
            empty_stack.size = 10


class TestStackPush:
    """Tests for Stack push operation."""

    def test_push_to_empty_stack(self, empty_stack):
        """Test pushing to an empty stack."""
        empty_stack.push(1)

        assert len(empty_stack) == 1
        assert empty_stack.peek() == 1

    def test_push_multiple_items(self, empty_stack):
        """Test pushing multiple items."""
        empty_stack.push(1)
        empty_stack.push(2)
        empty_stack.push(3)

        assert len(empty_stack) == 3
        assert empty_stack.peek() == 3

    def test_push_order_lifo(self, empty_stack):
        """Test that push follows LIFO order."""
        empty_stack.push(1)
        empty_stack.push(2)
        empty_stack.push(3)

        assert list(empty_stack) == [3, 2, 1]


class TestStackPop:
    """Tests for Stack pop operation."""

    def test_pop_from_single_element(self, empty_stack):
        """Test popping from a single-element stack."""
        empty_stack.push(1)

        item = empty_stack.pop()

        assert item == 1
        assert empty_stack.is_empty()

    def test_pop_multiple_times(self, populated_stack):
        """Test popping multiple times follows LIFO."""
        assert populated_stack.pop() == 1
        assert populated_stack.pop() == 2
        assert populated_stack.pop() == 3
        assert populated_stack.is_empty()

    def test_pop_from_empty_stack(self, empty_stack):
        """Test that popping from empty stack raises error."""
        with pytest.raises(EmptyStructureError):
            empty_stack.pop()

    def test_push_pop_alternating(self, empty_stack):
        """Test alternating push and pop operations."""
        empty_stack.push(1)
        assert empty_stack.pop() == 1

        empty_stack.push(2)
        empty_stack.push(3)
        assert empty_stack.pop() == 3
        assert empty_stack.pop() == 2


class TestStackPeek:
    """Tests for Stack peek operation."""

    def test_peek_at_top(self, populated_stack):
        """Test peeking at the top element."""
        assert populated_stack.peek() == 1
        assert len(populated_stack) == 3  # peek doesn't remove

    def test_peek_empty_stack(self, empty_stack):
        """Test that peeking at empty stack raises error."""
        with pytest.raises(EmptyStructureError):
            empty_stack.peek()

    def test_peek_after_operations(self, empty_stack):
        """Test peek after various operations."""
        empty_stack.push(1)
        assert empty_stack.peek() == 1

        empty_stack.push(2)
        assert empty_stack.peek() == 2

        empty_stack.pop()
        assert empty_stack.peek() == 1


class TestStackClear:
    """Tests for Stack clear operation."""

    def test_clear_populated_stack(self, populated_stack):
        """Test clearing a populated stack."""
        populated_stack.clear()

        assert populated_stack.is_empty()
        assert len(populated_stack) == 0

    def test_clear_empty_stack(self, empty_stack):
        """Test clearing an already empty stack."""
        empty_stack.clear()

        assert empty_stack.is_empty()


class TestStackIteration:
    """Tests for Stack iteration."""

    def test_iterate_over_stack(self, populated_stack):
        """Test iterating over the stack (top to bottom)."""
        result = []
        for item in populated_stack:
            result.append(item)

        assert result == [1, 2, 3]

    def test_list_conversion(self, populated_stack):
        """Test converting to Python list."""
        assert list(populated_stack) == [1, 2, 3]

    def test_iterate_empty_stack(self, empty_stack):
        """Test iterating over empty stack."""
        result = list(empty_stack)

        assert result == []

    def test_iteration_does_not_modify_stack(self, populated_stack):
        """Test that iteration doesn't modify the stack."""
        original_size = len(populated_stack)

        list(populated_stack)

        assert len(populated_stack) == original_size


class TestStackContains:
    """Tests for Stack membership testing."""

    def test_contains_existing_item(self, populated_stack):
        """Test membership for existing items."""
        assert 1 in populated_stack
        assert 2 in populated_stack
        assert 3 in populated_stack

    def test_contains_nonexistent_item(self, populated_stack):
        """Test membership for non-existent items."""
        assert 999 not in populated_stack
        assert 0 not in populated_stack

    def test_contains_empty_stack(self, empty_stack):
        """Test membership in empty stack."""
        assert 1 not in empty_stack


class TestStackRemove:
    """Tests for Stack remove operation (non-standard)."""

    def test_remove_existing_item(self, populated_stack):
        """Test removing an existing item."""
        item = populated_stack.remove(2)

        assert item == 2
        assert list(populated_stack) == [1, 3]

    def test_remove_top_item(self, populated_stack):
        """Test removing the top item."""
        item = populated_stack.remove(1)

        assert item == 1
        assert list(populated_stack) == [2, 3]

    def test_remove_nonexistent_item(self, populated_stack):
        """Test removing a non-existent item raises error."""
        with pytest.raises(ValueError):
            populated_stack.remove(999)

    def test_remove_from_empty_stack(self, empty_stack):
        """Test removing from empty stack raises error."""
        with pytest.raises(EmptyStructureError):
            empty_stack.remove(1)


class TestStackAdd:
    """Tests for Stack add operation (alias for push)."""

    def test_add_behaves_like_push(self, empty_stack):
        """Test that add behaves like push."""
        empty_stack.add(1)
        empty_stack.add(2)
        empty_stack.add(3)

        assert list(empty_stack) == [3, 2, 1]


class TestStackStringRepresentation:
    """Tests for Stack string representations."""

    def test_repr(self, populated_stack):
        """Test __repr__ method."""
        result = repr(populated_stack)

        assert result == "Stack([1, 2, 3])"

    def test_str(self, populated_stack):
        """Test __str__ method."""
        result = str(populated_stack)
        expected = """Stack (top to bottom):
  [1]
  [2]
  [3]"""

        assert result == expected

    def test_repr_empty_stack(self, empty_stack):
        """Test __repr__ for empty stack."""
        assert repr(empty_stack) == "Stack([])"

    def test_str_empty_stack(self, empty_stack):
        """Test __str__ for empty stack."""
        assert str(empty_stack) == "Stack: []"


class TestStackLifoProperty:
    """Tests to verify LIFO property of Stack."""

    def test_lifo_order_maintained(self, empty_stack):
        """Test that LIFO order is maintained through operations."""
        # Push items
        for i in range(10):
            empty_stack.push(i)

        # Pop all and verify reverse order
        popped = []
        while not empty_stack.is_empty():
            popped.append(empty_stack.pop())

        assert popped == list(range(9, -1, -1))

    def test_peek_shows_last_pushed(self, empty_stack):
        """Test that peek always shows the last pushed item."""
        empty_stack.push(1)
        assert empty_stack.peek() == 1

        empty_stack.push(2)
        assert empty_stack.peek() == 2

        empty_stack.push(3)
        assert empty_stack.peek() == 3


class TestStackWithVariousDataTypes:
    """Tests for Stack with various data types."""

    def test_with_strings(self, empty_stack):
        """Test stack with strings."""
        empty_stack.push("hello")
        empty_stack.push("world")

        assert empty_stack.pop() == "world"
        assert empty_stack.pop() == "hello"

    def test_with_mixed_types(self, empty_stack):
        """Test stack with mixed data types."""
        empty_stack.push(1)
        empty_stack.push("hello")
        empty_stack.push(3.14)
        empty_stack.push([1, 2, 3])

        assert empty_stack.pop() == [1, 2, 3]
        assert empty_stack.pop() == 3.14
        assert empty_stack.pop() == "hello"
        assert empty_stack.pop() == 1

    def test_with_none(self, empty_stack):
        """Test stack can store None."""
        empty_stack.push(None)
        empty_stack.push(1)

        assert empty_stack.pop() == 1
        assert empty_stack.pop() is None


class TestStackUseCases:
    """Tests demonstrating typical stack use cases."""

    def test_expression_evaluation_parentheses(self, empty_stack):
        """Test using stack for balanced parentheses checking."""
        expression = "((()))"

        for char in expression:
            if char == "(":
                empty_stack.push(char)
            elif char == ")":
                if empty_stack.is_empty():
                    assert False, "Unbalanced"
                empty_stack.pop()

        assert empty_stack.is_empty()  # Balanced

    def test_undo_functionality(self, empty_stack):
        """Test using stack for undo operations."""
        # Simulate actions
        actions = ["action1", "action2", "action3"]

        for action in actions:
            empty_stack.push(action)

        # Undo last two actions
        undone = []
        undone.append(empty_stack.pop())
        undone.append(empty_stack.pop())

        assert undone == ["action3", "action2"]
        assert empty_stack.peek() == "action1"
