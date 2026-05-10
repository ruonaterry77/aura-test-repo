"""Tests for shipping calculator."""
import pytest
from shipping import calculate_shipping, cheapest_method


def test_standard_under_1kg():
    assert calculate_shipping(0.5, "standard") == 5.99


def test_standard_over_1kg():
    # 2kg standard: 5.99 base + (1 * 0.50) surcharge = 6.49
    assert calculate_shipping(2.0, "standard") == 6.49


def test_express_over_1kg():
    # 3kg express: 12.99 + (2 * 0.50) = 13.99
    assert calculate_shipping(3.0, "express") == 13.99


def test_unknown_method_raises():
    with pytest.raises(ValueError):
        calculate_shipping(1.0, "teleport")


def test_cheapest_method_light_package():
    # For light packages standard is always cheapest
    assert cheapest_method(0.5) == "standard"


def test_cheapest_method_heavy_package():
    # Even for heavy packages standard stays cheapest
    assert cheapest_method(10.0) == "standard"
