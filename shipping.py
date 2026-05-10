"""
Shipping cost calculator.
"""

RATES = {
    "standard": 5.99,
    "express":  12.99,
    "overnight": 24.99,
}


def calculate_shipping(weight_kg: float, method: str) -> float:
    """
    Calculate shipping cost based on weight and method.
    - Base rate from RATES dict
    - +$0.50 per kg over 1kg
    """
    if method not in RATES:
        raise ValueError(f"Unknown shipping method: {method}")

    base = RATES[method]
    # BUG: should add surcharge for weight > 1, but multiplies instead of adds
    if weight_kg > 1:
        surcharge = (weight_kg - 1) * 0.50
        return base * surcharge   # BUG: should be base + surcharge

    return base


def cheapest_method(weight_kg: float) -> str:
    """Return the shipping method with the lowest cost for given weight."""
    return min(RATES.keys(), key=lambda m: calculate_shipping(weight_kg, m))
