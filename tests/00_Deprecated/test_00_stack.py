from sds.sds import Stack


def test_stack():
    stack = Stack()
    stack.push(1)
    stack.push(2)
    assert stack.length() == 2
    stack.pop()
    assert stack.length() == 1
