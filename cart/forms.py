from django import forms
from django.conf import settings
from django.contrib.sites.models import Site

class PayPalForm(forms.Form):
    business = forms.CharField(widget=forms.HiddenInput(), initial=settings.PAYPAL_RECEIVER_EMAIL)

    charset = forms.CharField(widget=forms.HiddenInput(), initial="utf-8")
    currency_code = forms.CharField(widget=forms.HiddenInput(), initial=settings.PAYPAL_CURRENCY_CODE)
    no_shipping = forms.CharField(widget=forms.HiddenInput(), initial="1")

    def __init__(self, pp_urls, *args, **kwargs):
        super(PayPalForm, self).__init__(*args, **kwargs)
        site = Site.objects.get(id=settings.SITE_ID)
        default_pp_urls = {'notify':"http://"+site.domain+"/cart/ipn/",
                    'cancel':"http://"+site.domain+"/cart/cancel/",
                    'return':"http://"+site.domain+"/cart/success/",}
        if pp_urls is not None:
            if not 'notify' in pp_urls:
                pp_urls['notify'] = default_pp_urls['notify']
            if not 'cancel' in pp_urls:
                pp_urls['cancel'] = default_pp_urls['cancel']
            if not 'return' in pp_urls:
                pp_urls['return'] = default_pp_urls['return']
        else:
            pp_urls = default_pp_urls
        self.fields['notify_url'] = forms.CharField(widget=forms.HiddenInput(),
                                                    initial=pp_urls['notify'])
        self.fields['cancel_return'] = forms.CharField(widget=forms.HiddenInput(),
                                                    initial=pp_urls['cancel'])
        self.fields['return_url'] = forms.CharField(widget=forms.HiddenInput(),
                                                    initial=pp_urls['return'])

class CheckoutForm(PayPalForm):
    cmd = forms.CharField(widget=forms.HiddenInput(), initial="_cart")
    upload = forms.CharField(widget=forms.HiddenInput(), initial="1")

    def __init__(self, items, pp_urls=None, *args, **kwargs):
        super(CheckoutForm, self).__init__(pp_urls, *args, **kwargs)
        custom_val = ''
        for i, item in enumerate(items):
            custom_val = custom_val+str(item.id)+','
            self.fields['amount_'+str(i+1)] = forms.CharField(
                                                        widget=forms.HiddenInput(),
                                                        initial=str(item.amount))
            self.fields['item_name_'+str(i+1)] = forms.CharField(
                                                        widget=forms.HiddenInput(),
                                                        initial=str(item.object))
        self.fields['custom'] = forms.CharField(widget=forms.HiddenInput(), initial=custom_val)







