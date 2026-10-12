import re

import pytest

from sds.core.exceptions import (
    DataStructureError,
    DuplicateElementError,
    ElementNotFoundError,
    EmptyStructureError,
    FullStructureError,
    IndexStructureError,
    InvalidOperationError,
    InvalidParameterError,
    StructureTypeError,
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
        (
            ElementNotFoundError,
            [Exception, DataStructureError, ValueError],
            "Element not found in structure",
        ),
        (
            DuplicateElementError,
            [Exception, DataStructureError, ValueError],
            "Element already exists in structure",
        ),
        (
            InvalidParameterError,
            [Exception, DataStructureError, ValueError],
            "Invalid parameter",
        ),
        (
            StructureTypeError,
            [Exception, DataStructureError, TypeError],
            "Invalid type for this structure",
        ),
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
        (
            ElementNotFoundError,
            [Exception, DataStructureError, ValueError],
            "Element not found in structure",
            "Élément introuvable",
        ),
        (
            DuplicateElementError,
            [Exception, DataStructureError, ValueError],
            "Element already exists in structure",
            "Élément déjà présent",
        ),
        (
            InvalidParameterError,
            [Exception, DataStructureError, ValueError],
            "Invalid parameter",
            "Paramètre invalide",
        ),
        (
            StructureTypeError,
            [Exception, DataStructureError, TypeError],
            "Invalid type for this structure",
            "Type invalide",
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


@pytest.mark.parametrize(
    "class_name, native",
    [
        (ElementNotFoundError, ValueError),
        (DuplicateElementError, ValueError),
        (InvalidParameterError, ValueError),
        (StructureTypeError, TypeError),
    ],
)
def test_extended_exception_caught_as_native(class_name, native):
    """Each extended exception is caught by the built-in it replaces."""
    with pytest.raises(native):
        raise class_name()
    with pytest.raises(DataStructureError):
        raise class_name()


@pytest.mark.parametrize(
    "class_name",
    [EmptyStructureError, FullStructureError, InvalidOperationError],
)
def test_structure_state_exceptions_are_not_value_errors(class_name):
    """State errors are not ValueError: the structure, not the value, is at fault."""
    assert not issubclass(class_name, ValueError)
