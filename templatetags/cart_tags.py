from django import template
from cart.models import CartItem

register = template.Library()

@register.inclusion_tag('cart/inline.html', takes_context=True)
def render_inline_cart(context, user):
    items = CartItem.objects.filter(user=user)
    total = 0
    for item in items:
        total += item.object.amount
    return{'items':items, 'total':total, 'MEDIA_URL':context['MEDIA_URL']}

