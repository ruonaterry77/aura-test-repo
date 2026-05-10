"""
Inventory management system.
Tracks stock levels and calculates order costs.
"""

class Product:
    def __init__(self, name: str, price: float, stock: int):
        self.name  = name
        self.price = price
        self.stock = stock

    def is_available(self, qty: int) -> bool:
        return self.stock >= qty

    def reserve(self, qty: int) -> bool:
        """Reserve stock for an order. Returns False if not enough stock."""
        if not self.is_available(qty):
            return False
        self.stock -= qty
        return True


class Cart:
    def __init__(self):
        self.items: list[tuple[Product, int]] = []

    def add(self, product: Product, qty: int) -> bool:
        """Add qty of product to cart. Returns False if not enough stock."""
        if not product.reserve(qty):
            return False
        self.items.append((product, qty))
        return True

    def subtotal(self) -> float:
        """Sum of (price * qty) for each item."""
        return sum(p.price * q for p, q in self.items)

    def apply_discount(self, percent: float) -> float:
        """Return subtotal after applying a percentage discount (0-100)."""
        return self.subtotal() * (1 - percent / 100)

    def total_items(self) -> int:
        """Return total number of individual items in the cart."""
        return sum(q for p, q in self.items)


class OrderProcessor:
    TAX_RATE = 0.08  # 8% tax

    def __init__(self, cart: Cart):
        self.cart = cart

    def calculate_tax(self) -> float:
        return round(self.cart.subtotal() * self.TAX_RATE, 2)

    def final_total(self, discount_percent: float = 0) -> float:
        if not isinstance(discount_percent, (int, float)):
            raise ValueError("Discount percentage must be a number")
        if discount_percent < 0:
            raise ValueError("Discount percentage cannot be negative")
        subtotal = self.cart.apply_discount(discount_percent)
        tax = self.calculate_tax()
        return round(subtotal + tax, 2)

    def can_checkout(self) -> bool:
        return self.cart.total_items() > 0