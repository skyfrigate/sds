import re

import pytest

from sds.core.exceptions import (
    DataStructureError,
    EmptyStructureError,
    FullStructureError,
    IndexStructureError,
    InvalidOperationError,
)


@pytest.mark.parametrize(
    "class_name, class_hierarchy, default_message",
    [
        (DataStructureError, [Exception], None),
        (
            EmptyStructureError,
            [Exception, DataStructureError],
            "Cannot perform operation on empty structure",
        ),
        (
            FullStructureError,
            [Exception, DataStructureError],
            "Cannot add to full structure",
        ),
        (InvalidOperationError, [Exception, DataStructureError], "Invalid operation"),
        (IndexStructureError, [Exception, DataStructureError], "Index out of range"),
    ],
)
def test_data_structure_exception(class_name, class_hierarchy, default_message):
    e = class_name()

    for class_category in class_hierarchy:
        assert isinstance(e, class_category)

    if default_message is not None:
        assert re.escape(e.message) == re.escape(default_message)


@pytest.mark.parametrize(
    "class_name, class_hierarchy, default_message, other_message",
    [
        (DataStructureError, [Exception], None, None),
        (
            EmptyStructureError,
            [Exception, DataStructureError],
            "Cannot perform operation on empty structure",
            "Impossible de réaliser cette action",
        ),
        (
            FullStructureError,
            [Exception, DataStructureError],
            "Cannot add to full structure",
            "Impossible d'ajout à la structure",
        ),
        (
            InvalidOperationError,
            [Exception, DataStructureError],
            "Invalid operation",
            "Operation interdite",
        ),
        (
            IndexStructureError,
            [Exception, DataStructureError],
            "Index out of range",
            "N'est pas dans le segment d'index",
        ),
    ],
)
def test_data_structure_exception_with_message(
    class_name, class_hierarchy, default_message, other_message
):
    if other_message is not None:
        e = class_name(other_message)
    else:
        e = class_name()

    for class_category in class_hierarchy:
        assert isinstance(e, class_category)

    if default_message is not None:
        assert re.escape(e.message) != re.escape(default_message)
        assert re.escape(e.message) == re.escape(other_message)
