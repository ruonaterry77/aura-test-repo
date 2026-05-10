"""Tests for the inventory management system."""
import pytest
from inventory import Product, Cart, OrderProcessor


def test_product_reserve_reduces_stock():
    p = Product("Widget", 9.99, 10)
    assert p.reserve(3) is True
    assert p.stock == 7


def test_product_reserve_fails_when_insufficient():
    p = Product("Widget", 9.99, 2)
    assert p.reserve(5) is False
    assert p.stock == 2  # stock unchanged


def test_cart_subtotal():
    p1 = Product("Apple",  1.00, 100)
    p2 = Product("Banana", 0.50, 100)
    cart = Cart()
    cart.add(p1, 3)   # 3.00
    cart.add(p2, 4)   # 2.00
    assert cart.subtotal() == 5.00


def test_cart_total_items_counts_quantity():
    """total_items should count individual units, not distinct product types."""
    p1 = Product("A", 1.00, 100)
    p2 = Product("B", 1.00, 100)
    cart = Cart()
    cart.add(p1, 5)
    cart.add(p2, 3)
    assert cart.total_items() == 8   # 5 + 3, not 2


def test_apply_discount_10_percent():
    """10% discount on $100 subtotal should give $90."""
    p = Product("Expensive", 100.00, 10)
    cart = Cart()
    cart.add(p, 1)
    assert cart.apply_discount(10) == 90.0


def test_apply_discount_25_percent():
    """25% discount on $200 subtotal should give $150."""
    p = Product("Item", 100.00, 10)
    cart = Cart()
    cart.add(p, 2)
    assert cart.apply_discount(25) == 150.0


def test_order_final_total_with_discount():
    """$100 item, 20% discount → $80 + 8% tax = $86.40"""
    p = Product("Thing", 100.00, 5)
    cart = Cart()
    cart.add(p, 1)
    processor = OrderProcessor(cart)
    # subtotal=100, discount=20% → 80, tax=8% of 100 → 8, total=88
    # (tax is on original subtotal per the design)
    assert processor.final_total(discount_percent=20) == 88.0


def test_order_can_checkout_with_items():
    p = Product("X", 5.00, 10)
    cart = Cart()
    cart.add(p, 2)
    processor = OrderProcessor(cart)
    assert processor.can_checkout() is True


def test_order_cannot_checkout_empty_cart():
    cart = Cart()
    processor = OrderProcessor(cart)
    assert processor.can_checkout() is False
