from django.forms import ModelForm, modelformset_factory
from django import forms
from invoices.models import Invoice, Product, Client, Company

class InvoiceForm(ModelForm):
    client = forms.ModelChoiceField(queryset=Client.objects.all())
    class Meta:
        model = Invoice
        fields = ['number', 'date', 'client']


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price']

ProductFormSet = modelformset_factory(Product, fields=('name', 'price'), extra=15)

# class ClientSelectForm(ModelForm):
#
#     def __init__(self, *args, **kwargs):
#         self.initial_client = kwargs.pop('initial_client')
#         self.CLIENT_LIST = Client.objects.all()
#         self.CLIENT_CHOICES = [('-----', '--Select a Client--')]
#
#         for client in self.CLIENT_LIST:
#             d_t = (client.id, client.name)
#             self.CLIENT_CHOICES.append(d_t)
#
#         super(ClientSelectForm, self).__init__(*args, **kwargs)
#
#         self.fields['client'] = forms.ChoiceField(
#             label='Client',
#             choices=self.CLIENT_CHOICES,
#             widget=forms.Select(attrs={'class': 'form-control mb-3'}),)
#
#     class Meta:
#         model = Invoice
#         fields = ['client']
#
#     def clean_client(self):
#         c_client = self.cleaned_data['client']
#         if c_client == '-----':
#             return self.initial_client
#         else:
#             return Client.objects.get(id=c_client)
