from django import forms
from django.utils.html import format_html

from .models import Address
from paypal.standard.forms import PayPalPaymentsForm


class ShippingAddressForm(forms.Form):
    class Meta:
        model = Address,
        fields = "[address, city, state, zipcode, country, phone]"
        widgets = {
            "address": forms.TextInput(attrs={
                "class": "tx-border tx-border-secondary tx-py-2.5 tx-px-4 tx-rounded-md tx-w-full tx-outline-none tx-font-new",
                "placeholder": "Address", "autofocus": "autofocus", "required": "required"}),
            "city": forms.TextInput(attrs={
                "class": "tx-border tx-border-secondary tx-py-2.5 tx-px-4 tx-rounded-md tx-w-full tx-outline-none tx-font-new",
                "placeholder": "City", "required": "required"}),
            "state": forms.TextInput(attrs={
                "class": "tx-border tx-border-secondary tx-py-2.5 tx-px-4 tx-rounded-md tx-w-full tx-outline-none tx-font-new",
                "placeholder": "State", "required": "required"}),
            "zipcode": forms.TextInput(attrs={
                "class": "tx-border tx-border-secondary tx-py-2.5 tx-px-4 tx-rounded-md tx-w-full tx-outline-none tx-font-new",
                "placeholder": "Zipcode", "required": "required"}),
            "country": forms.TextInput(attrs={
                "class": "tx-border tx-border-secondary tx-py-2.5 tx-px-4 tx-rounded-md tx-w-full tx-outline-none tx-font-new",
                "placeholder": "Country", "required": "required"}),
            "phone": forms.TextInput(attrs={
                "class": "tx-border tx-border-secondary tx-py-2.5 tx-px-4 tx-rounded-md tx-w-full tx-outline-none tx-font-new",
                "placeholder": "Phone", "required": "required"}),
        }


class ExtraPayPalForm(PayPalPaymentsForm):

    def get_image(self):
        # Get the rectangular PayPal button
        return "https://www.paypalobjects.com/webstatic/en_US/i/buttons/PP_logo_h_100x26.png"

    def render(self, *args, **kwargs):
        if not args and not kwargs:
            # `form.render` usage from template
            return format_html(
                """<form action="{0}" method="post" class="tx-w-full tx-flex tx-justify-center tx-items-center">
{1}
<input type="image" src="{2}" name="submit" alt="Buy it Now" class="tx-w-1/2 tx-flex tx-justify-center tx-items-center tw-px-20 tx-py-3 tx-bg-paypal-yellow tw-text-primary tx-transition-all hand" />
</form>""",
                self.get_login_url(),
                self.as_p(),
                self.get_image(),
            )
        else:
            # Need to delegate to super. This provides
            # support for `as_p` method and for `BoundField.label_tag`,
            # and perhaps others.
            return super().render(*args, **kwargs)


