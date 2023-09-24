from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Div, HTML, Layout, Row
from django import forms
from django.forms import BaseInlineFormSet, inlineformset_factory, ModelForm
from django.forms.widgets import NumberInput

from invoices.models import Address, Company, Contact, Customer, Invoice, OrderLine, Product


class InvoiceForm(ModelForm):
    customer = forms.ModelChoiceField(
        queryset=Customer.objects.order_by('company'))
    issued_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(
                    'sequence', css_class='form-group col-lg-3 col-md-3 col-sm-6 mb-0'),
                Column(
                    'number', css_class='form-group col-lg-3 col-md-3 col-sm-6 mb-0'),
                Column('issued_date',
                       css_class='form-group col-lg-3 col-md-3 col-sm-3 mb-0'),
                Column(
                    'customer', css_class='form-group col-lg-3 col-md-3 col-sm-6 mb-0'),
                css_class='form-row'
            )
        )

    class Meta:
        model = Invoice
        fields = ['sequence', 'number', 'issued_date', 'customer']


class OrderLineForm(ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.order_by('name'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(

            Row(
                Column('id', type="hidden", css_class="d-none"),
                Column('DELETE', type="hidden", css_class="d-none"),
                Column(
                    'product', css_class='form-group col-lg-3 col-md-3 col-sm-5 mb-0'),
                Column(
                    'quantity', css_class='form-group col-lg-3 col-md-3 col-sm-3 mb-0'),
                Column('unit_price',
                       css_class='form-group col-lg-3 col-md-3 col-sm-3 mb-0'),
                Div(
                    HTML("""<label class='empty-div form-label'>&nbsp</label>
                    <button type="button" class="buttonDynamic">Dynamic</button>"""),
                     css_class="form-group col-lg-1 col-md-1 col-sm-1 mb-0 box-btn-add-product"), css_class="formsetDynamic"
            )
        )

    class Meta:
        model = OrderLine
        fields = ['product', 'quantity', 'unit_price']


class BaseInlineOrderFormSet(BaseInlineFormSet):
    deletion_widget = forms.HiddenInput


OrderLineFormSet = inlineformset_factory(
    Invoice, OrderLine, form=OrderLineForm, formset=BaseInlineOrderFormSet, fields=('product', 'quantity', 'unit_price'), extra=1, can_delete=True)


class ContactForm(ModelForm):
    prefix = 'contact'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(
                    'name', css_class='form-group col-lg-3 col-md-3 col-sm-5 mb-0'),
                Column(
                    'email', css_class='form-group col-lg-4 col-md-3 col-sm-3 mb-0'),
                Column(
                    'cc_email', css_class='form-group col-lg-12 col-md-3 col-sm-3 mb-0'),
            )
        )

    class Meta:
        model = Contact
        fields = ['name', 'email', 'cc_email']


class AddressForm(ModelForm):
    prefix = 'address'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(
                    'street', css_class='form-group col-lg-6 col-md-3 col-sm-5 mb-0'),
                Column(
                    'postal_code', css_class='form-group col-lg-3 col-md-3 col-sm-3 mb-0'),
                Column(
                    'city', css_class='form-group col-lg-3 col-md-3 col-sm-3 mb-0'),
            )
        )

    class Meta:
        model = Address
        fields = ['city', 'postal_code', 'street']


class CompanyForm(ModelForm):
    prefix = 'company'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer_information_file_number'].label = 'CIF'
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(
                    'name', css_class='form-group col-lg-3 col-md-3 col-sm-5 mb-0'),
                Column(
                    'customer_information_file_number', css_class='form-group col-lg-2 col-md-3 col-sm-3 mb-0'),
            )
        )

    class Meta:
        model = Company
        fields = ['name', 'customer_information_file_number']
