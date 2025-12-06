import re

from sds.core.exceptions import DataStructureError, EmptyStructureError


def test_data_structure_exception():
    e = DataStructureError()
    assert isinstance(e, DataStructureError)
    assert isinstance(e, Exception)


def test_empty_structure_exception():
    e = EmptyStructureError()
    assert isinstance(e, EmptyStructureError)
    assert isinstance(e, DataStructureError)
    assert isinstance(e, Exception)
    assert re.escape(e.message) == re.escape(
        "Cannot perform operation on empty structure"
    )
