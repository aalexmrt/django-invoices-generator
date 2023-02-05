from django.shortcuts import render, redirect

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from invoices.models import Invoice, Client, Company, Product
from invoices.forms import InvoiceForm, ProductFormSet
import datetime
# from .models import Question


def index(request):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    invoices_list = Invoice.objects.all()

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
    print(invoice.client)
    if request.method == 'GET':
        invoice_form = InvoiceForm(instance=invoice)
        product_formset  = ProductFormSet(queryset=Product.objects.filter(invoice=invoice))
        # client_form = ClientSelectForm(initial_client=invoice.client)
        context['product_formset'] = product_formset
        context['invoice_form'] = invoice_form
        # context['client_form'] = client_form

        return render(request, 'invoices/form.html', context)
    if request.method == 'POST':
        product_formset = ProductFormSet(request.POST)
        invoice_form = InvoiceForm(request.POST, instance=invoice)

        # client_form = ClientSelectForm(request.POST, initial_client=invoice.client, instance=invoice)

        if invoice_form.is_valid:
            # client_form.save()
            invoice_form.save()

        if product_formset.is_valid:

            # product_formset.cleaned_data
            for product_form in product_formset:
                product = product_form.save(commit=False)
                if product_form.cleaned_data == {}:
                    continue
                product.invoice = invoice
                product.save()


            # for product_form in product_formset:
            #
            #

            #     product = product_form.save(commit=False)
            #     product.invoice = invoice
            #     product.save()

            return HttpResponseRedirect('/')

    return render(request, 'invoices/form.html', context)



# def add_invoice(request):
#     if request.method == 'POST':
#         client = request.POST['client']
#         company = request.POST['company']
#
#
#         form_invoice = InvoiceForm(request.POST)
#         form_invoice.fields['client'].queryset = Client.objects.filter(id=client)
#         form_invoice.fields['company'].queryset = Company.objects.filter(id=company)
#
#
#
#         if form_invoice.is_valid():
#
#             print(form_invoice.save())
#             return HttpResponseRedirect('/')
#
#
#
#     else:
#         form_invoice = InvoiceForm()
#         # form_products = ProductForm()
#
#         context = {
#             # 'form_products': form_products,
#             'form_invoice': form_invoice,
#         }
#
#
#     return render(request, 'invoices/form.html', context)
