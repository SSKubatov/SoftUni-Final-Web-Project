def get_discounted_price_rounded_to_thousands(price, discount):
    if not discount or discount <= 0:
        return price
    return int((price - (price * (discount / 100))) * 100)


def get_discounted_price(price, discount):
    if not discount or discount <= 0:
        return price
    return int((price - (price * (discount / 100))))
