from django.dispatch import Signal

pp_ipn = Signal(providing_args=["cart_items"])
