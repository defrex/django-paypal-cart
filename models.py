from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

class CartItemManager(models.Manager):
    def add_to_cart(self, object, user, amount, other):
        '''
        adds a new object to the cart. Usage:
        CartItem.objects.add_to_cart(model_instance, user_instance)
        '''
        ct = ContentType.objects.get_for_model(object)
        oid = object.id
        cart_item = CartItem(content_type=ct, object_id=oid, object=object, user=user, amount=amount)
        if other:
            cart_item.other = str(other)
        cart_item.save()
        return cart_item

class CartItem(models.Model):
    content_type = models.ForeignKey(ContentType, verbose_name=_('content type'))
    object_id = models.PositiveIntegerField(_('object id'), db_index=True)
    object = generic.GenericForeignKey('content_type', 'object_id')

    amount = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    user = models.ForeignKey(User)
    other = models.CharField(max_length=255, blank=True, null=True)

    objects = CartItemManager()
    
    def __unicode__(self):
        return 'user: %(user)s, object: %(obj)s, amount: %(amt)i'\
                    % {'user': self.user, 'obj': self.object, 'amt': self.amount}
    
