from django import template

register = template.Library()


@register.simple_tag
def price_after_discount(price, discount):
    if not discount or discount <= 0:
        return price

    discounted_price = (price - (price * (discount / 100)))

    return f"{discounted_price:.2f}"


@register.filter
def leva(price):
    return f"{price} лв."
