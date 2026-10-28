"""Order pricing for BrewCart. Prices are in whole rupees."""

MENU = {
    "espresso": {"name": "Espresso", "price": 120},
    "cappuccino": {"name": "Cappuccino", "price": 180},
    "latte": {"name": "Latte", "price": 170},
    "cold-brew": {"name": "Cold Brew", "price": 190},
    "mocha": {"name": "Mocha", "price": 210},
}

COUPONS = {"BREW10": 10, "FIRST20": 20}   # percent off
GST_PERCENT = 5
FREE_DELIVERY_FROM = 500                   # subtotal after discount
DELIVERY_FEE = 40


class PricingError(ValueError):
    pass


def subtotal(items):
    """items: list of {"id": "latte", "qty": 2}"""
    total = 0
    for line in items:
        item = MENU.get(line.get("id"))
        if item is None:
            raise PricingError(f"unknown item: {line.get('id')}")
        qty = int(line.get("qty", 1))
        if qty < 1:
            raise PricingError("quantity must be at least 1")
        total += item["price"] * qty
    return total


def discount(amount, coupon=None):
    if not coupon:
        return 0
    percent = COUPONS.get(coupon.upper())
    if percent is None:
        raise PricingError(f"unknown coupon: {coupon}")
    return round(amount * percent / 100)


def quote(items, coupon=None):
    sub = subtotal(items)
    off = discount(sub, coupon)
    after = sub - off
    delivery = 0 if after >= FREE_DELIVERY_FROM else DELIVERY_FEE
    gst = round(after * GST_PERCENT / 100)
    return {"subtotal": sub, "discount": off, "delivery": delivery, "gst": gst, "total": after + delivery + gst}
