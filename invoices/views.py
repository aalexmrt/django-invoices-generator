from django.shortcuts import render, redirect
from django.core.files.base import ContentFile
from invoices.models import Invoice, Issuer, GlobalSettings, MailInfo, OrderLine, Product
from django.http import HttpResponseRedirect
from invoices.forms import InvoiceForm, OrderLineFormSet
from invoices.utils.send_email import *
from django_weasyprint.views import WeasyTemplateResponse
import environ

env = environ.Env()
environ.Env.read_env()


def index(request):

    if request.method == 'POST':
        print("form")
        print(request.POST)

    invoices_list = Invoice.objects.order_by('-created_at')
    context = {
        'invoices_list': invoices_list
    }

    return render(request, 'invoices/index.html', context)


def add_invoice(request):

    new_invoice = Invoice.objects.create()
    new_invoice.save()
    return redirect('make_invoice', new_invoice.id)


def make_invoice(request, id):

    invoice = Invoice.objects.get(pk=id)
    order_lines = OrderLine.objects.filter(invoice=invoice)

    if request.method == 'POST':
        invoice_form = InvoiceForm(request.POST, instance=invoice)
        order_formset = OrderLineFormSet(
            request.POST, instance=invoice, queryset=order_lines)

        if invoice_form.is_valid():
            invoice = invoice_form.save()
            invoice.issuer = Issuer.objects.filter(
                company__name='issuer').first()
            invoice.save()

        if order_formset.is_valid():
            invoice_orders = []
            for order_form in order_formset:
                order = order_form.save(commit=False)
                order.invoice = invoice
                try:
                    product = Product.objects.get(
                        pk=order_form.cleaned_data["product"].id)
                    order.product = product
                    order.save()
                    invoice_orders.append(order)
                except:
                    pass

            order_formset.save()
            invoice.calculate_totals(invoice_orders)
            invoice.save()
            save_invoice_pdf(request, id)

            return redirect('index')

    elif request.method == 'GET':  # GET request
        invoice_form = InvoiceForm(instance=invoice)
        order_formset = OrderLineFormSet(
            instance=invoice, queryset=order_lines)

    context = {
        'invoice': invoice,
        'invoice_form': invoice_form,
        'order_formset': order_formset,

    }
    return render(request, 'invoices/form.html', context)


def save_invoice_pdf(request, inv_id):

    invoice = Invoice.objects.get(pk=inv_id)
    order_lines = OrderLine.objects.filter(invoice=invoice)

    context = {}
    context['invoice'] = invoice
    context['order_lines'] = order_lines
    context['empty_rows'] = range(15 - len(order_lines))

    pdf_render = WeasyTemplateResponse(
        request=request, template='invoices/invoice_pdf.html', context=context).rendered_content
    pdf_file_name = "{}-{}_{}_{}.pdf".format(
        invoice.sequence, invoice.number, invoice.customer.company.name.replace(" ", "-"), invoice.issued_date)

    # Overwrite existing pdf with the new one
    invoice.pdf_document.delete()
    invoice.pdf_document.save(pdf_file_name, ContentFile(pdf_render))

    return True


def invoice_detail(request, id):
    invoice = Invoice.objects.get(pk=id)
    context = {}
    context['invoice'] = invoice

    return render(request, 'invoices/detail.html', context)


def send_email(request, id):
    GMAIL = env("GMAIL_ACCOUNT")
    GMAIL_PASSWORD = env("GMAIL_ACCOUNT_PWD")

    invoice = Invoice.objects.get(pk=id)

    # TODO add the part of the email cc
    todo_cc = ["", ""]

    mail_info = MailInfo.objects.create(invoice=invoice)
    if send_invoice_email(GMAIL, GMAIL_PASSWORD, invoice.company.name, invoice.client.primary_contact.email_account, invoice.client.primary_contact.name, todo_cc, invoice.pdf_document):
        mail_info.status = 'Delivered'
        mail_info.save()
    else:
        mail_info.status = 'Failed'
        mail_info.save()

    return HttpResponseRedirect('/')


# def send_all_invoices(request):
#     GMAIL = env("GMAIL_ACCOUNT")
#     GMAIL_PASSWORD = env("GMAIL_ACCOUNT_PWD")
#     # a little hardcoded
#     company = Company.objects.get(pk=1)

#     # This function gets all the invoices that hasn't been mailed and send them at once
#     invoices_query = Invoice.objects.filter(mailed=False).order_by('-client')

#     clients_list = []
#     invoices_list = []
#     # a little hardcoded again
#     todo_cc = ["", ""]
#     for invoice in invoices_query:
#         if invoice.client not in clients_list:
#             clients_list.append(invoice.client)

#     for client in clients_list:
#         pdf_query = DocumentPdf.objects.filter(
#             client=client).filter(invoice__mailed=False)

#         if send_invoice_email(GMAIL, GMAIL_PASSWORD, company.name,
#                               client.primary_contact.email_account, client.primary_contact.name, todo_cc, pdf_query):
#             for pdf in pdf_query:
#                 Invoice.objects.filter(id=pdf.invoice.id).update(mailed=True)

#     return HttpResponseRedirect('/')
