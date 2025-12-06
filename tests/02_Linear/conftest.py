"""Configuration and fixtures for linear module tests."""

from types import NoneType

import pytest

from sds.linear import DoublyNode, SimpleNode
from sds.linear.list import CircularLinkedList, DoublyLinkedList, LinkedList
from sds.linear.queue import Deque, PriorityQueue, Queue
from sds.linear.stack import Stack


@pytest.fixture
def empty_linked_list():
    """Provide an empty LinkedList.

    Returns
    -------
    LinkedList
        An empty singly linked list.

    Examples
    --------
    >>> def test_example(empty_linked_list):
    ...     assert empty_linked_list.is_empty()
    ...     assert len(empty_linked_list) == 0
    """
    return LinkedList()


@pytest.fixture
def populated_linked_list():
    """Provide a LinkedList with elements [1, 2, 3, 4, 5].

    Returns
    -------
    LinkedList
        A singly linked list containing integers 1 through 5.

    Examples
    --------
    >>> def test_example(populated_linked_list):
    ...     assert len(populated_linked_list) == 5
    ...     assert list(populated_linked_list) == [1, 2, 3, 4, 5]
    """
    lst = LinkedList()
    for i in range(1, 6):
        lst.append(i)
    return lst


@pytest.fixture
def empty_doubly_linked_list():
    """Provide an empty DoublyLinkedList.

    Returns
    -------
    DoublyLinkedList
        An empty doubly linked list.

    Examples
    --------
    >>> def test_example(empty_doubly_linked_list):
    ...     assert empty_doubly_linked_list.is_empty()
    ...     assert len(empty_doubly_linked_list) == 0
    """
    return DoublyLinkedList()


@pytest.fixture
def populated_doubly_linked_list():
    """Provide a DoublyLinkedList with elements [1, 2, 3, 4, 5].

    Returns
    -------
    DoublyLinkedList
        A doubly linked list containing integers 1 through 5.

    Examples
    --------
    >>> def test_example(populated_doubly_linked_list):
    ...     assert len(populated_doubly_linked_list) == 5
    ...     assert list(populated_doubly_linked_list) == [1, 2, 3, 4, 5]
    """
    dll = DoublyLinkedList()
    for i in range(1, 6):
        dll.append(i)
    return dll


@pytest.fixture
def empty_circular_list():
    """Provide an empty CircularLinkedList.

    Returns
    -------
    CircularLinkedList
        An empty circular linked list.

    Examples
    --------
    >>> def test_example(empty_circular_list):
    ...     assert empty_circular_list.is_empty()
    ...     assert len(empty_circular_list) == 0
    """
    return CircularLinkedList()


@pytest.fixture
def populated_circular_list():
    """Provide a CircularLinkedList with elements [1, 2, 3, 4, 5].

    Returns
    -------
    CircularLinkedList
        A circular linked list containing integers 1 through 5.

    Examples
    --------
    >>> def test_example(populated_circular_list):
    ...     assert len(populated_circular_list) == 5
    ...     assert list(populated_circular_list) == [1, 2, 3, 4, 5]
    """
    cll = CircularLinkedList()
    for i in range(1, 6):
        cll.append(i)
    return cll


@pytest.fixture(
    params=[
        [],
        [1],
        [1, 2],
        [1, 2, 3],
        [1, 2, 3, 4, 5],
        ["a", "b", "c"],
        [3.14, 2.71, 1.41],
    ]
)
def list_data(request):
    """Provide various list data for parametrized tests.

    Parameters
    ----------
    request : pytest.FixtureRequest
        Pytest request object containing the parameter value.

    Returns
    -------
    list
        A list of values to populate test lists with.

    Notes
    -----
    This fixture is parametrized and will run tests multiple times,
    once for each data set.

    Examples
    --------
    >>> def test_example(list_data):
    ...     lst = LinkedList()
    ...     for item in list_data:
    ...         lst.append(item)
    ...     assert len(lst) == len(list_data)
    """
    return request.param


@pytest.fixture(params=[LinkedList, DoublyLinkedList, CircularLinkedList])
def list_class(request):
    """Provide list classes for parametrized tests.

    This fixture allows tests to run against all linked list implementations
    to ensure consistent behavior.

    Parameters
    ----------
    request : pytest.FixtureRequest
        Pytest request object containing the parameter value.

    Returns
    -------
    type
        Either LinkedList, DoublyLinkedList, or CircularLinkedList class.

    Examples
    --------
    >>> def test_example(list_class):
    ...     lst = list_class()
    ...     assert lst.is_empty()
    """
    return request.param


@pytest.fixture
def sample_values():
    """Provide a consistent set of sample values for testing.

    Returns
    -------
    list
        A list of various data types for testing.

    Examples
    --------
    >>> def test_example(sample_values):
    ...     lst = LinkedList()
    ...     for val in sample_values:
    ...         lst.append(val)
    """
    return [42, "hello", 3.14, None, [1, 2], {"key": "value"}]


# Queue fixtures
@pytest.fixture
def empty_queue():
    """Provide an empty Queue.

    Returns
    -------
    Queue
        An empty FIFO queue.
    """
    return Queue()


@pytest.fixture
def populated_queue():
    """Provide a Queue with elements [1, 2, 3] (1 at front).

    Returns
    -------
    Queue
        A FIFO queue with elements.
    """
    q = Queue()
    q.enqueue(1)
    q.enqueue(2)
    q.enqueue(3)
    return q


# Deque fixtures
@pytest.fixture
def empty_deque():
    """Provide an empty Deque.

    Returns
    -------
    Deque
        An empty double-ended queue.
    """
    return Deque()


@pytest.fixture
def populated_deque():
    """Provide a Deque with elements [1, 2, 3].

    Returns
    -------
    Deque
        A deque with elements.
    """
    dq = Deque()
    dq.add_rear(1)
    dq.add_rear(2)
    dq.add_rear(3)
    return dq


# PriorityQueue fixtures
@pytest.fixture
def empty_priority_queue():
    """Provide an empty PriorityQueue.

    Returns
    -------
    PriorityQueue
        An empty priority queue.
    """
    return PriorityQueue()


@pytest.fixture
def populated_priority_queue():
    """Provide a PriorityQueue with elements [5, 1, 3].

    Returns
    -------
    PriorityQueue
        A priority queue with elements (1 has highest priority).
    """
    pq = PriorityQueue()
    pq.enqueue(5)
    pq.enqueue(1)
    pq.enqueue(3)
    return pq


# Stack fixtures
@pytest.fixture
def empty_stack():
    """Provide an empty Stack.

    Returns
    -------
    Stack
        An empty LIFO stack.
    """
    return Stack()


@pytest.fixture
def populated_stack():
    """Provide a Stack with elements [3, 2, 1] (1 on top).

    Returns
    -------
    Stack
        A LIFO stack with elements.
    """
    stack = Stack()
    stack.push(3)
    stack.push(2)
    stack.push(1)
    return stack


@pytest.fixture
def simple_node():
    """Provide a simple Node with integer data."""
    return SimpleNode(42)


@pytest.fixture
def node_chain():
    """Provide a chain of 3 connected nodes: 1 -> 2 -> 3."""
    node3 = SimpleNode(3)
    node2 = SimpleNode(2, node3)
    node1 = SimpleNode(1, node2)
    return node1


@pytest.fixture
def simple_doubly_node():
    """Provide a simple DoublyNode with integer data."""
    return DoublyNode(42)


@pytest.fixture
def doubly_node_chain():
    """Provide a bidirectional chain of 3 nodes: 1 <-> 2 <-> 3."""
    node1 = DoublyNode(1)
    node2 = DoublyNode(2)
    node3 = DoublyNode(3)

    # Link forward
    node1.next = node2
    node2.next = node3

    # Link backward
    node2.prev = node1
    node3.prev = node2

    return node1


@pytest.fixture(
    params=[
        (0, int),
        (42, int),
        (-10, int),
        (3.14, float),
        ("hello", str),
        ("world", str),
        ([1, 2, 3], list),
        ({"key": "value"}, dict),
        ((1, 2), tuple),
        (None, NoneType),
    ]
)
def various_data_types(request):
    """Provide various data types for parametrized tests."""
    return request.param
