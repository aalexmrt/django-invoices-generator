from django.forms import ModelForm, inlineformset_factory, BaseInlineFormSet
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Div, HTML, Button, ButtonHolder, Field

from invoices.models import Customer, Invoice, OrderLine, Product


class InvoiceForm(ModelForm):
    customer = forms.ModelChoiceField(
        queryset=Customer.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(
                    'sequence', css_class='form-group col-lg-3 col-md-3 col-sm-2 mb-0'),
                Column(
                    'number', css_class='form-group col-lg-3 col-md-3 col-sm-2 mb-0'),
                Column('issued_date',
                       css_class='form-group col-lg-3 col-md-3 col-sm-3 mb-0'),
                Column(
                    'customer', css_class='form-group col-lg-3 col-md-3 col-sm-5 mb-0'),
                css_class='form-row'
            )
        )

    class Meta:
        model = Invoice
        fields = ['sequence', 'number', 'issued_date', 'customer']


class OrderLineForm(ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.all())

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
                    'quantity', css_class='form-group col-lg-3 col-md-3 col-sm-2 mb-0'),
                Column('unit_price',
                       css_class='form-group col-lg-3 col-md-3 col-sm-3 mb-0'),
                Div(
                    Div(
                        HTML("""<label class='empty-div form-label'>&nbsp</label>
                    <button type="button" class="buttonDynamic">Dynamic</button>""")
                    ), css_class="form-group col-lg-1 col-md-1 col-sm-1 mb-0"), css_class="formsetDynamic"
            )
        )

    class Meta:
        model = OrderLine
        fields = ['product', 'quantity', 'unit_price']


class BaseInlineOrderFormSet(BaseInlineFormSet):
    deletion_widget = forms.HiddenInput


OrderLineFormSet = inlineformset_factory(
    Invoice, OrderLine, form=OrderLineForm, formset=BaseInlineOrderFormSet, fields=('product', 'quantity', 'unit_price'), extra=1, can_delete=True)
