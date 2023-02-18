from django.forms import ModelForm, inlineformset_factory
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
        fields = ['name', 'price']


ProductFormSet = inlineformset_factory(
    Invoice, Product, fields=('name', 'price'), extra=15)
