import pytest
from decimal import Decimal
from app.operations import OperationFactory
from app.exceptions import OperationError, ValidationError


@pytest.mark.parametrize("name,a,b,expected", [
    ("add", "2", "3", Decimal("5")),
    ("subtract", "5", "3", Decimal("2")),
    ("multiply", "4", "3", Decimal("12")),
    ("divide", "10", "2", Decimal("5")),
    ("modulus", "10", "3", Decimal("1")),
    ("int_divide", "7", "2", Decimal("3")),
    ("abs_diff", "3", "8", Decimal("5")),
    ("percent", "50", "200", Decimal("25")),
])
def test_basic(name, a, b, expected):
    assert OperationFactory.create(name).execute(Decimal(a), Decimal(b)) == expected


def test_power():
    assert OperationFactory.create("power").execute(Decimal("2"), Decimal("3")) == Decimal("8")


def test_root():
    assert OperationFactory.create("root").execute(Decimal("9"), Decimal("2")) == Decimal("3")


@pytest.mark.parametrize("name", ["divide", "modulus", "int_divide", "percent", "root"])
def test_zero_errors(name):
    with pytest.raises(OperationError):
        OperationFactory.create(name).execute(Decimal("1"), Decimal("0"))


def test_even_root_negative():
    with pytest.raises(OperationError):
        OperationFactory.create("root").execute(Decimal("-4"), Decimal("2"))


def test_unknown():
    with pytest.raises(ValidationError):
        OperationFactory.create("nope")


def test_available():
    assert len(OperationFactory.available_operations()) == 10
