from django.shortcuts import render, redirect
from django.core.files.base import ContentFile
from django.http import HttpResponseRedirect

from invoices.models import Invoice, Product, DocumentPdf
from invoices.forms import InvoiceForm, ProductFormSet

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
    empty_rows = 15 - len(products)
    context = {}
    context['invoice'] = invoice
    context['products'] = products
    context['empty_rows'] = range(empty_rows)
    pdf_render = WeasyTemplateResponse(
        request=request, template='invoices/invoice_pdf.html', context=context).rendered_content
    document_name = "{}_{}_{}.pdf".format(
        invoice.number, invoice.client.name.replace(" ", "-"), invoice.date)
    created_file = DocumentPdf.objects.get_or_create(
        file_name=document_name)[0]
    created_file.invoice = invoice
    created_file.file_pdf.delete()
    created_file.file_pdf.save(document_name, ContentFile(pdf_render))

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
            invoice_form.save()

        if product_formset.is_valid():
            for product_form in product_formset:
                if not product_form.cleaned_data.get('name'):
                    continue
                product = product_form.save(commit=False)
                product.invoice = invoice
                product.save()
            product_formset.save()

        save_invoice_pdf(request, id)

        return HttpResponseRedirect('/')

    return render(request, 'invoices/form.html', context)

# TODO merge with the create_build_invoice view


def invoice_pdf(request, invoice, products):

    empty_rows = 15 - len(products)

    context = {}
    context['invoice'] = invoice
    context['products'] = products
    context['empty_rows'] = range(empty_rows)

    pdf_render = WeasyTemplateResponse(
        request=request, template='invoices/invoice_pdf.html', context=context).rendered_content
    document_name = "{}_{}_{}.pdf".format(
        invoice.number, invoice.date, invoice.client)
    created_file = DocumentPdf.objects.get_or_create(
        file_name=document_name)[0]
    created_file.invoice = invoice
    created_file.file_pdf.delete()
    created_file.file_pdf.save(document_name, ContentFile(pdf_render))

    return render(request, 'invoices/invoice_pdf.html', context)


def send_email(request, id):
    # TODO
    return "hello"
