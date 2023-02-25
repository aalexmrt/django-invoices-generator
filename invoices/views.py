from django.shortcuts import render, redirect
from django.core.files.base import ContentFile
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Sum
from invoices.models import Invoice, Product, DocumentPdf
from invoices.forms import InvoiceForm, ProductFormSet
from django.views.generic import DetailView
from invoices.utils.send_email import *

from django_weasyprint.views import WeasyTemplateResponse


def index(request):
    invoices_list = Invoice.objects.order_by('-created_at')
    context = {
        'invoices_list': invoices_list
    }

    return render(request, 'invoices/index.html', context)


def create_invoice(request):
    # create a blank invoice ....
    newInvoice = Invoice.objects.create()
    newInvoice.save()

    inv = Invoice.objects.get(number=newInvoice.number)

    return redirect('create_build_invoice', inv.id)


def save_invoice_pdf(request, inv_id):

    invoice = Invoice.objects.get(id=inv_id)
    products = Product.objects.filter(invoice=invoice)

    context = {}
    context['invoice'] = invoice
    context['products'] = products
    context['empty_rows'] = range(15 - len(products))

    pdf_render = WeasyTemplateResponse(
        request=request, template='invoices/invoice_pdf.html', context=context).rendered_content
    pdf_file_name = "{}_{}_{}.pdf".format(
        invoice.number, invoice.client.name.replace(" ", "-"), invoice.date)

    created_file = DocumentPdf.objects.get_or_create(invoice=invoice)[0]

    created_file.invoice = invoice
    # Overwrite existing pdf with the new one
    created_file.file_pdf.delete()
    created_file.file_pdf.save(pdf_file_name, ContentFile(pdf_render))

    return True


def create_build_invoice(request, id):
   # fetch that invoice
    try:
        invoice = Invoice.objects.get(id=id)
        pass
    except:
        # TODO handle exception
        return redirect('invoices')

    products = Product.objects.filter(invoice=invoice)

    context = {}
    context['invoice'] = invoice
    context['products'] = products

    if request.method == 'GET':
        invoice_form = InvoiceForm(instance=invoice)
        product_formset = ProductFormSet(instance=invoice)
        context['product_formset'] = product_formset
        context['invoice_form'] = invoice_form
        return render(request, 'invoices/form.html', context)

    if request.method == 'POST':
        product_formset = ProductFormSet(request.POST, instance=invoice)
        invoice_form = InvoiceForm(request.POST, instance=invoice)

        if invoice_form.is_valid():
            invoice = invoice_form.save()

        if product_formset.is_valid():
            for product_form in product_formset:
                if not product_form.cleaned_data.get('name'):
                    continue
                product = product_form.save(commit=False)
                product.total = product.price * product.quantity
                product.invoice = invoice
                product.save()
            product_formset.save()

        # Perform all the operations to calculate taxes, discount and total of the invoice
        invoice.total_products = products.aggregate(Sum('total'))['total__sum']
        invoice.total_discount = invoice.invoice_settings.discount * invoice.total_products
        invoice.total_base = invoice.total_products + invoice.total_discount
        invoice.total_tax = invoice.total_base * invoice.invoice_settings.tax / 100
        invoice.total = invoice.total_tax + invoice.total_base
        invoice.save()

        save_invoice_pdf(request, id)

        return HttpResponseRedirect('/')

    return render(request, 'invoices/form.html', context)

# TODO merge with the create_build_invoice view


def invoice_detail(request, id):
    print(id)
    invoice = Invoice.objects.get(id=id)
    print(invoice)
    context = {}
    context['document_pdf'] = DocumentPdf.objects.filter(invoice=invoice)[0]

    return render(request, 'invoices/detail.html', context)


def send_email(request, id):

    invoice = Invoice.objects.get(id=id)
    files = DocumentPdf.objects.filter(invoice=invoice)

    send_invoice_mail(invoice.client, invoice.company,
                      files)

    print("succeded")

    return HttpResponseRedirect('/')
