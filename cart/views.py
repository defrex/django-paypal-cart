import simplejson
import logging
import sys
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from cart.models import CartItem
from cart.forms import CheckoutForm
from cart.signals import pp_ipn

@login_required
def checkout(request, template_name='cart/checkout.html', pp_urls=None, model=None):
    '''
    Renders a form ready to be submit to paypal. Passes PAYPAL_URL, which is
    taken from settings. Also passes total, which is the total amount
    of all the cart items
    '''
    items = CartItem.objects.filter(user=request.user)
    if model:
        print 'model:', model
        ct = ContentType.objects.get_for_model(model)
        items = items.filter(content_type=ct)
    print items
    form = CheckoutForm(items, pp_urls)
    total = 0
    for item in items:
        total += item.amount
    return render_to_response(template_name,{
            "form":form,
            "PAYPAL_URL": settings.PAYPAL_URL,
            "total": total,
            },context_instance=RequestContext(request))

def remove_from_cart(request, itemid):
    '''
    Meant for use with ajax. Pass an itemid and it will be deleted.
    Returns json with two keys, status, which will be "removed_from_cart"
    and total, which will be an updated total for the card after the deletion
    of the item.
    '''
    CartItem.objects.get(pk=itemid).delete()
    items = CartItem.objects.filter(user=request.user)
    total = 0
    for item in items:
        total += item.object.amount
    return HttpResponse(simplejson.dumps({
            "status":"removed_from_cart",
            "total": total,
            }))

def payment_successful(request):
    '''
    handles the "IPN" from paypal. That is, when there is a successful paypal
    transaction, paypal calls this url with some info. The most important
    value here is POST['custom'], which is a comma seperated list of CartItem
    ids (ending in ,) that have been paid for.
    
    sends a list of cart_items to cart.signals.pp_ipn
    '''
    logging.debug('handling paypal IPN:')
    if request.method == 'POST':
        logging.debug('is post')
        itemids = request.POST['custom'].split(',')
        logging.debug('itemids:')
        logging.debug(itemids)
        try:
            cart_items = CartItem.objects.in_bulk(itemids[:-1])
        except:
            logging.debug('item fail')
            logging.debug(sys.exc_info())
            raise
        logging.debug('cart items:')
        logging.debug(cart_items)
        logging.debug('sending signal')
        pp_ipn.send(sender=None, cart_items=cart_items)
        logging.debug('signal sent')
    return HttpResponse('OK')

