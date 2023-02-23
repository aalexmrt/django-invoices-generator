from django.forms import ModelForm, inlineformset_factory, BaseInlineFormSet
from django import forms
from invoices.models import Invoice, Product, Client


class InvoiceForm(ModelForm):
    client = forms.ModelChoiceField(queryset=Client.objects.all())

    class Meta:
        model = Invoice
        fields = ['number', 'date', 'client']


class ProductForm(ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'quantity', 'price']


class BaseInlineProductFormSet(BaseInlineFormSet):
    deletion_widget = forms.HiddenInput


ProductFormSet = inlineformset_factory(
    Invoice, Product, formset=BaseInlineProductFormSet, fields=('name', 'quantity', 'price'),  extra=1, can_delete=True)
