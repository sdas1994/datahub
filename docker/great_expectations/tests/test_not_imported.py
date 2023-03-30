import pytest

from great_expectations.util import NotImported


@pytest.fixture
def not_imported() -> NotImported:
    return NotImported("Please install foo")


def test_get_attr_on_not_installed(not_imported):
    with pytest.raises(ModuleNotFoundError, match=str(not_imported)):
        not_imported.thing


def test_set_attr_on_not_installed(not_imported):
    with pytest.raises(ModuleNotFoundError, match=str(not_imported)):
        not_imported.thing = 5


def test_calling_not_installed(not_imported):
    with pytest.raises(ModuleNotFoundError, match=str(not_imported)):
        not_imported()
