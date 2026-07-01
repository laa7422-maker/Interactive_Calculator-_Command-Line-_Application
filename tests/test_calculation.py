from decimal import Decimal
from datetime import datetime
from app.calculation import Calculation


def test_result():
    assert Calculation("add", Decimal("2"), Decimal("3")).result == Decimal("5")


def test_roundtrip():
    c = Calculation("multiply", Decimal("3"), Decimal("4"))
    r = Calculation.from_dict(c.to_dict())
    assert r.result == Decimal("12")
    assert isinstance(r.timestamp, datetime)


def test_str():
    assert "add(1, 1) = 2" in str(Calculation("add", Decimal("1"), Decimal("1")))
