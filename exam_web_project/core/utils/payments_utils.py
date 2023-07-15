def get_discounted_price(price, discount):
    return int((price - (price * (discount / 100))) * 100)


