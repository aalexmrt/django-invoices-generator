from django.forms import ModelForm, inlineformset_factory, BaseInlineFormSet
from django import forms


from invoices.models import Customer, Invoice, OrderLine, Product


class InvoiceForm(ModelForm):
    customer = forms.ModelChoiceField(queryset=Customer.objects.all())

    class Meta:
        model = Invoice
        fields = ['sequence', 'number', 'issued_date', 'customer']


class OrderLineForm(ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.all())

    class Meta:
        model = OrderLine
        fields = ['product', 'quantity', 'unit_price']


class BaseInlineOrderFormSet(BaseInlineFormSet):
    deletion_widget = forms.HiddenInput


OrderLineFormSet = inlineformset_factory(
    Invoice, OrderLine, form=OrderLineForm, formset=BaseInlineOrderFormSet, fields=('product', 'quantity', 'unit_price'), extra=1, can_delete=True)
