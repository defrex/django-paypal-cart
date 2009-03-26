## Overview
django-paypal-cart is a pretty simple shopping cart that submits to paypal.
It was designed to be used with ajax, so most of the views return json or
html snippets (with no <html> and such).

## Basic Usage
### setup
1. Add the cart app to INSTALLED_APPS in your settings.py.
2. Add cart to your urls

    (r'^cart/', include('cart.urls')),
    
3. Run manage.py syncdb
4. in settings.py set PAYPAL_URL and PAYPAL_EMAIL. PAYPAL_URL is where the
paypal form is submit, and PAYPAL_EMAIL is for the account that will receive
the money.

### Add to cart
There is no real UI included in this app. You add items to the cart by creating
a CartItem object. CartItems contain a GenericForeignKey, a user, and amount, 
and an "other" field for you to store whatever. The CartItemManager gives you 
the handy add_to_cart method. like so: add_to_cart(object, user, amount, other)

    from cart.models import CartItem
    from myapp.models import MyObject
    
    def my_view(response):
        my_object = MyObject.objects.get(pk=1)
        
        CartItem.objects.add_to_cart(my_object, request.user, my_object.price)

### Remove from cart
In order to remove an item from the cart, you can either just delete the 
CartItem:
    from cart.models import CartItem
    
    cart_item = CartItem.objects.get(pk=1)
    cart_item.delete()

Or you can call reverse('cart_item', args=[item_id]) (probably 
/cart/remove/(id)). This view is really meant for ajax. It returns json in the 
form:
    {
        "status":"removed_from_cart",
        "total": current_total_for_cart,
    }

### Checkout
Checkout is again meant for ajax. It's at reverse('cart_checkout') and it
returns an html snippet with a form, made up of entirely hidden fields
ready for submission to PayPal. The point of this is so you can retrieve the 
form append it to the current page and submit it right away. It will be 
properly formed for paypal to check out your cart properly.

#### A couple considerations: 
* The name of the item on the paypal page will be str() wrapped around whatever
model instance you passed to object. So you probably want to def __unicode__ 
on that.
* Because return is a reserved word in python, and because PayPal wants one of
the most important fields to be named return, you have to do a little work
in JavaScript before you submit the form. In jQuery:

    $('input[@name="return_url"]').attr('name', 'return');

### Instant Payment Notification
PayPal calls it IPN. This is basically PayPal's way of letting you know when a 
payment has gone through. django-paypal-cart conveniently provides a signal
for you to attach to in order to handle this.
    from cart.signals import pp_ipn
    def ipn_handler(sender, **kwargs):
        cart_items = kwargs['cart_items']
        # do what you will with the cart_item objects
    pp_ipn.connect(ipn_handler)

## Advanced Usage
Read the source if you're so damn advanced. :p

