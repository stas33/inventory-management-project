from django import template
from products.models import Product

register = template.Library()

@register.filter(name='is_in_cart')
def is_in_cart(product, cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == product.id:
            return True
    return False

@register.filter(name='cart_quantity')
def cart_quantity(product, cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == product.id:
            return cart.get(id)
    return 0


# @register.filter(name='current_quantity')
# def current_quantity(item, cart):
#     keys = cart.keys()
#     for id in keys:
#         if int(id) == item.id:
#             return cart.get(id)
#     return 0

@register.filter(name='total_price')
def total_price(product, cart):
    return product.price * cart_quantity(product, cart)

@register.filter(name='total_cart_price')
def total_cart_price(product, cart):
    sum = 0
    for i in product:
        sum += total_price(i, cart)
    return sum

@register.filter(name='currency')
def currency(price):
    return "€" + str(price)

@register.filter(name="multiply")
def multiply(n1, n2):
    return n1 * n2