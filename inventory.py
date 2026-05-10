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
        # BUG 1: should be (1 - percent/100) but divides by 10 instead of 100
        return self.subtotal() * (1 - percent / 10)

    def total_items(self) -> int:
        """Return total number of individual items in the cart."""
        # BUG 2: counts product types, not qty
        return len(self.items)


class OrderProcessor:
    TAX_RATE = 0.08  # 8% tax

    def __init__(self, cart: Cart):
        self.cart = cart

    def calculate_tax(self) -> float:
        return round(self.cart.subtotal() * self.TAX_RATE, 2)

    def final_total(self, discount_percent: float = 0) -> float:
        """Discounted subtotal + tax."""
        discounted = self.cart.apply_discount(discount_percent)
        return round(discounted + self.calculate_tax(), 2)

    def can_checkout(self) -> bool:
        """Cart must have at least one item to check out."""
        # BUG 3: off-by-one — should be > 0 but uses >= 1... actually fine
        # Real bug: uses total_items() which is broken (counts types not qty)
        return self.cart.total_items() > 0
