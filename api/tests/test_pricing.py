import pytest

from pricing import PricingError, discount, quote, subtotal


def test_subtotal_adds_price_times_quantity():
    assert subtotal([{"id": "latte", "qty": 2}, {"id": "espresso", "qty": 1}]) == 460


def test_unknown_item_is_rejected():
    with pytest.raises(PricingError):
        subtotal([{"id": "frappe", "qty": 1}])


def test_zero_quantity_is_rejected():
    with pytest.raises(PricingError):
        subtotal([{"id": "latte", "qty": 0}])


@pytest.mark.parametrize("amount, coupon, expected", [
    (460, None, 0),
    (460, "BREW10", 46),
    (460, "brew10", 46),
    (500, "FIRST20", 100),
    (190, "BREW10", 19),
])
def test_discount(amount, coupon, expected):
    assert discount(amount, coupon) == expected


def test_unknown_coupon_is_rejected():
    with pytest.raises(PricingError):
        discount(460, "FREECOFFEE")


def test_quote_small_order_pays_delivery():
    q = quote([{"id": "latte", "qty": 2}, {"id": "espresso", "qty": 1}], "BREW10")
    assert q == {"subtotal": 460, "discount": 46, "delivery": 40, "gst": 21, "total": 475}


def test_quote_free_delivery_from_500_after_discount():
    q = quote([{"id": "mocha", "qty": 3}])          # 630
    assert q["delivery"] == 0
    assert q["total"] == 630 + 32


def test_free_delivery_threshold_uses_amount_after_discount():
    q = quote([{"id": "cold-brew", "qty": 3}], "FIRST20")   # 570 - 114 = 456, below 500
    assert q["delivery"] == 40
