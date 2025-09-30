from django import template
register = template.Library()

@register.filter(name='get_quantity')
def get_cart_quantity(cart, movie_id):
    return cart[str(movie_id)]

@register.filter(name='mul')
def multiply(value, arg):
    """Multiply the value by the argument."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0