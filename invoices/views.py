from django.shortcuts import render, redirect

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from invoices.models import Invoice, Client, Company, Product
from invoices.forms import InvoiceForm, ProductFormSet
import datetime
# from .models import Question


def index(request):
    invoices_list = Invoice.objects.order_by('-created_at')
    context = {
        'invoices_list': invoices_list
    }

    return render(request, 'invoices/index.html', context)


def create_invoice(request):
    #create a blank invoice ....
    newInvoice = Invoice.objects.create()
    newInvoice.save()

    inv = Invoice.objects.get(number=newInvoice.number)

    return redirect('create_build_invoice', inv.id)

def create_build_invoice(request, id):
   #fetch that invoice
    try:
        invoice = Invoice.objects.get(id=id)
        pass
    except:
        messages.error(request, 'Something went wrong')
        return redirect('invoices')

    products = Product.objects.filter(invoice=invoice)

    context = {}
    context['invoice'] = invoice
    context['products'] = products

    if request.method == 'GET':
        invoice_form = InvoiceForm(instance=invoice)
        product_formset  = ProductFormSet(instance=invoice)
        context['product_formset'] = product_formset
        context['invoice_form'] = invoice_form
        return render(request, 'invoices/form.html', context)

    if request.method == 'POST':
        product_formset = ProductFormSet(request.POST, instance=invoice)
        invoice_form = InvoiceForm(request.POST, instance=invoice)

        # client_form = ClientSelectForm(request.POST, initial_client=invoice.client, instance=invoice)

        if invoice_form.is_valid():
            invoice_form.save()

        if product_formset.is_valid():
            for product_form in product_formset:
                if product_form.cleaned_data == {}:
                    continue
                product = product_form.save(commit=False)
                product.invoice = invoice
                product.save()

            return HttpResponseRedirect('/')

    return render(request, 'invoices/form.html', context)
